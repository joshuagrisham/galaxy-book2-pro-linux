#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EGIS 1C7A:0582 Match-on-Chip fingerprint reader driver PoC with support for SDCP (VERY WIP!!).

Usage:
    ARGV0 -h | --help
    ARGV0 info
    ARGV0 verify
    ARGV0 enroll
    ARGV0 wipe

Options:
-h, --help         Show help

Commands:
info               Get device info
verify             Verify finger
enroll             Enroll a new finger
wipe               Wipe all enrolled fingers
"""

import sys
from docopt import docopt

import usb.core
import usb.util

import re
import secrets
import struct
import time

import hashlib
import hmac
from ecdsa import ECDH, NIST256p
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.kbkdf import (
   CounterLocation, KBKDFHMAC, Mode
)

# find our device
dev = usb.core.find(idVendor=0x1c7a, idProduct=0x0582)
if dev is None:
	raise ValueError('Device not found')

# USB URB Device IDs for 1c7a:0582 device
USB_BULK_OUT = 0x02
USB_BULK_IN = 0x81
USB_INTERRUPT_IN = 0x83

# Number of partial enrollments needed in order to store a print
NUM_ENROLL_STAGES = 10

# Reading/Writing to the bulk in/out seems to have this kind of payload structure:
#  1) 8 bytes hard-coded prefix depending on out vs in (see below)
#  2) 2 bytes which are a kind of "check bytes" for the payload
#  3) hardcoded "00 00 00"
#  4) 2 bytes that seem to be some kind of type/subtype for different processes/events
#  5) then it seems to vary a bit more with additional payload data depending on different type of events; either some kind of payload directly or more "type" kind of stuff either before or after the payload

# TODO: Probably better/easier/nicer to move to the struct package for building payloads, but for now we will do it all super-hard-coded with bytes...

## Setup for SDCP (https://github.com/Microsoft/SecureDeviceConnectionProtocol)

## supposed to use NIST P256 curve per https://github.com/Microsoft/SecureDeviceConnectionProtocol/wiki/Secure-Device-Connection-Protocol#cryptographic-algorithms
#host_signing_key = SigningKey.generate(curve=NIST256p, hashfunc=hashlib.sha256)
#host_verifying_key = host_signing_key.verifying_key
#host_private_key = host_signing_key.to_string() # 32-byte private key for signing
#host_public_key = host_verifying_key.to_string() # 64-byte public key for verifying
## signature = host_signing_key.sign(b"message")

host_ecdh = ECDH(curve=NIST256p)
host_private_key = host_ecdh.generate_private_key()
host_public_key = host_ecdh.get_public_key()
host_random = secrets.token_bytes(32)

SEC1_UNCOMPRESSED_POINT_HEADER = b'\x04'

def egismoc_sdcp_connect():
	connect_cmd_prefix = b'\x6b\x50\x57\x01\x00\x00\x00\x62\x20'
	connect_cmd_suffix = b'\x00\x00'
	connect_cmd = connect_cmd_prefix + host_random + SEC1_UNCOMPRESSED_POINT_HEADER + host_public_key.to_string() + connect_cmd_suffix
	write(connect_cmd)
	connect_response = read()
	return connect_response

class SdcpConnectResponse:
	r_d: bytes
	cert_m: bytes
	pk_d: bytes
	pk_f: bytes
	def __init__(self):
		pass

def parse_sdcp_connect_response(value):
	value_len = len(value.tobytes())
	if value[value_len-2:value_len].tobytes() != b'\x90\x00':
		raise ValueError("device indicated failure instead of sending valid SDCP ConnectResponse")

	result = SdcpConnectResponse()
	
	# get r_d:
	result.r_d = value[15:15+32].tobytes()
	pos = 15+32

	# Next there always seems to be \x30\x27 on this device; not sure what that is?? but for now we skip it
	pos += 2


	# get cert_m:
	if value[pos:pos+2].tobytes() == b'\x30\x82':
		pos += 2
		len_pos = pos
		cert_m_len = 0
		while len_pos < value_len:
			if value[len_pos:len_pos + 1].tobytes() == b'\x30': # end of length, next sequence starting
				if len_pos == pos:
					raise ValueError("cert_m length missing from SDCP ConnectResponse")
				cert_m_len = int.from_bytes(value[pos:len_pos].tobytes(), "big")
				break
			else:
				len_pos += 1
		if cert_m_len <= 0:
			raise ValueError("cert_m length <= 0 from SDCP ConnectResponse")
		result.cert_m = value[pos-2:len_pos+cert_m_len].tobytes() # from start of \x30\x82 through cert_m_len
		# check cert_m to be sure it is a valid x509 DER certificate
		cert_m = x509.load_der_x509_certificate(result.cert_m)
		print("-----")
		print("SDCP Device Certificate:")
		print(f"  Subject:          {cert_m.subject}")
		print(f"  Issuer:           {cert_m.issuer.rdns}")
		print(f"  Serial number:    {cert_m.serial_number}")
		print(f"  Not valid before: {cert_m.not_valid_before}")
		print(f"  Not valid after:  {cert_m.not_valid_after}")
		print(f"  Extensions:       {cert_m.extensions}")
		print("-----")
		pos += (len_pos - pos) + cert_m_len
	else:
		raise ValueError("Could not parse cert_m from SDCP ConnectResponse")
	
	# get pk_d
	# Check the byte at pos is an ECDH public key
	if value[pos:pos+1].tobytes() != b'\x04':
		raise ValueError("Could not parse pk_d from SDCP ConnectResponse")
	result.pk_d = value[pos:pos+65].tobytes() # 0x04 + 64 bytes
	pos += 65

	# get pk_f
	# Check the byte at pos is an ECDH public key
	if value[pos:pos+1].tobytes() != b'\x04':
		raise ValueError("Could not parse pk_f from SDCP ConnectResponse")
	result.pk_f = value[pos:pos+65].tobytes() # 0x04 + 64 bytes

	# TODO: per: https://github.com/Microsoft/SecureDeviceConnectionProtocol/wiki/Secure-Device-Connection-Protocol#secure-connection-protocol
	# At this point we need to use the above-parsed fields and do the following:
	#
	# Performs key agreement:
	# 	a <- KeyAgreement(sk_h, pk_f)
	# Derives master secret:
	# 	ms <- KDF(a, "master secret", r_h||r_d)
	# Derives MAC secret, s, and symmetric key, k:
	# 	(s, k) <- KDF(ms, "application keys")
	#
	# "s" will then be used when actually creating Commit IDs later (new_finger_id)

	return result


# Bytes prefix for every payload sent to and from device
WRITE_PREFIX = b'EGIS\x00\x00\x00\x01'
READ_PREFIX = b'SIGE\x00\x00\x00\x01'

# Derive the 2 "check bytes" for write payloads
# 32-bit big-endian sum of all 16-bit words (including check bytes) MOD 0xFFFF should be 0
def get_check_bytes(payload):
    full_payload = WRITE_PREFIX + b'\x00\x00\x00\x00\x00' + payload
    full_payload_h_be_ints = []
    # Combine every 2 bytes (32 bits) into 2-byte big-endian "words"
    # Example: '0x53 0x49' should become '0x4953'
    i = 0
    while i < len(full_payload):
        if i+1 >= len(full_payload):
            full_payload_h_be_ints.append(struct.unpack('>H', full_payload[i].to_bytes(length=1) + b'\x00')[0])
        else:
            full_payload_h_be_ints.append(struct.unpack('>H', full_payload[i:i+2])[0])
        i += 2
    # we can derive the "first occurence" of possible check bytes as `0xFFFF - (sum_of_32bit_words % 0xFFFF)`
    # and then pack it so it is split into 2 individual bytes and in the right order
    return struct.pack('>H', 0xFFFF - (sum(full_payload_h_be_ints) % 0xFFFF))

# Standard method to make it easier to write to USB_BULK_OUT
# This method will create and send a "full" payload which looks like this:
#   E G I S 00 00 00 01 {cb1} {cb2} 00 00 00 {payload}
# (where cb1 and cb2 are some check bytes generated by the get_check_bytes() method and payload is what is passed via the parameter)
def write(payload):
	full_payload = WRITE_PREFIX + get_check_bytes(payload) + b'\x00\x00\x00' + payload
	print(f"Sending: {full_payload.hex(' ')}")
	return dev.write(USB_BULK_OUT, full_payload)

# Standard method to make it easier to read from USB_BULK_IN
def read(length=4096, timeout=5000):
	return dev.read(USB_BULK_IN, length, timeout)

# Standard method to make it easier to read from USB_INTERRUPT_IN (wait for response from fingerprint on physical device)
def wait_for_finger(length=64, timeout=10000): # 10s default timeout to put finger on sensor
	start = time.time()
	while True:
		if (time.time() - start) > timeout/1000:
			break
		response = dev.read(USB_INTERRUPT_IN, length, timeout)
		print(f"Wait read: {response.tobytes().hex(' ')}")
		if (response[:4].tobytes() == b'SIGE' and response[-4:].tobytes() == b'\x90\x00\x90\x00'):
			return response
			# TODO: add this new logic to driver (loop-read interrupt until response starts with 'SIGE' and last four bytes are 90 00 90 00 before continuing, instead of just reading once and continuing)

### Setup ###

# required every time before the device is used; the Windows driver seems to work that the driver is always running in the background so this setup is only done once on Windows startup

# Put the identifier for each fingerprint in an array in case it is helpful later? We can also use len(fingers_enrolled) to see how many fingerprints are enrolled
fingers_enrolled = []

def setup():
	# Reset the device in case it was not closed out properly last time
	dev.reset()

	# set the active configuration. With no arguments, the first
	# configuration will be the active one
	dev.set_configuration(1)

	# get an endpoint instance
	cfg = dev.get_active_configuration()
	intf = cfg[(0,0)]

	## Initialization sequence (attempting to match from traces) ##

	# First send some control transfers
	print(dev.ctrl_transfer(0xc0, 32, 0x0000, 4, 16).tobytes().hex(' '))
	print(dev.ctrl_transfer(0xc0, 32, 0x0000, 4, 40).tobytes().hex(' '))
	print(dev.ctrl_transfer(0x80, 0, 0x0000, 0, 2).tobytes().hex(' '))
	print(dev.ctrl_transfer(0x80, 0, 0x0000, 0, 2).tobytes().hex(' '))
	print(dev.ctrl_transfer(0xc0, 82, 0x0000, 0, 8).tobytes().hex(' '))

	cfg = dev.get_active_configuration()
	intf = cfg[(0,0)]

	# Then send a series of "initilization" packets
	write(b'\x07\x50\x7f\x00\x00\x00\x00\x0c')
	print(f"Read: {read().tobytes().hex(' ')}")

	write(b'\x07\x50\x43\x00\x00\x00\x00\x04')
	print(f"Read: {read().tobytes().hex(' ')}")

	write(b'\x07\x50\x07\x00\x02\x00\x00\x1d')
	# this response seems to have slightly different payload if there are fingers regd already vs not? not sure logic, but for now we can instead use the next sequence instead for this detection?
	print(f"Read: {read().tobytes().hex(' ')}")

	write(b'\x07\x50\x19\x04\x00\x00\x01\x40')
	# This response seems to return a payload with an identifier/signature of all fingers registered, so we can use it to know if we are ready to verify or not and provide other info
	# The payload portion of this packet (listed as #5 in description above) seems to be composed like this:
	#   - 32 bytes per finger
	#     - seem to be some kind of identifier/hash of the finger?
	#     - The 32 byte block sequences can come in different order when fingers are added/removed?
	#   - then 2 bytes "90 00"

	fingers_enrolled_response = read()
	print(f"Read: {fingers_enrolled_response.tobytes().hex(' ')}")

	if len(fingers_enrolled_response) >= 48:
		for i in range(int((len(fingers_enrolled_response) - 16) / 32)):
			fingers_enrolled.append(fingers_enrolled_response[14+(i*32):14+(i*32)+32])

	print(f"Device initialization is complete. Number of fingers already enrolled: {len(fingers_enrolled)}")

# Payload that needs to be built for multiple methods below (both enroll and verify)
def fingers_enrolled_payload():
	# This payload needs to be built based on existing registered fingerprints and seems to be used in multiple different processes

	# ("num fingers regd * 20" + "9") # TODO based on this logic does it mean only max 7 fingers per user?
	payload = (((len(fingers_enrolled) + 1) * 0x20) + 0x09).to_bytes()
	# then 50 17 03 00 00 00
	payload += b'\x50\x17\x03\x00\x00\x00'
	# then ("num fingers regd * 20") # TODO based on this logic does it mean only max 7 fingers per user?
	payload += ((len(fingers_enrolled) + 1) * 0x20).to_bytes()
	# Then hard-coded 32 x 00s
	payload += b'\x00\x00\x00\x00\x00\x00\x00\x00'
	payload += b'\x00\x00\x00\x00\x00\x00\x00\x00'
	payload += b'\x00\x00\x00\x00\x00\x00\x00\x00'
	payload += b'\x00\x00\x00\x00\x00\x00\x00\x00'
	# Then each of finger identifiers already registered
	for f in reversed(fingers_enrolled): #TODO not sure if reversed is required? but seems to be so in trace anyway
		payload += f
	# then 00 40
	payload += b'\x00\x40'

	return payload


### End Setup ###



# Different methods for performing different operations: info, enroll, verify, and wipe

### INFO ###

def info():
	print("Device information:")
	print(dev)
	print(f"Number of fingers enrolled: {len(fingers_enrolled)}")



### ENROLL ###

# Sensor read response checks during enrollment

# TODO: In the Windows driver they seem to be able to tell difference between Move Lower / Higher / Left / Right but could not find any difference in payload for each of these conditions (it was all the same payload pattern for these "not in center" conditions)
# also as a "hack" python has trouble if the byte is 0x0a because it interprets this as a linebreak (char 0a) and will sometimes not match this as "any character" (".") so will use a hack (.|\n) as the placeholder to pick up just in case the byte is 0x0a
FINGER_NOT_YET_ENROLLED_REGEX = re.compile(READ_PREFIX + b'(.|\n){0,}\x90\x04')

# TODO: Driver to be updated with this new logic below for partial read failures!!

# if len-2 byte is 0x64 then it is always a partial read failure
PARTIAL_READ_FAILED_REGEX               = re.compile(READ_PREFIX + b'(.|\n){0,}\x64(.|\n)')
# if prefix is 0x00 0x00 0x00 0x04 then the "reason" of partial read failure is "off center"
PARTIAL_READ_FAILED_NOT_IN_CENTER_REGEX = re.compile(READ_PREFIX + b'(.|\n)(.|\n)\x00\x00\x00\x04(.|\n){0,}')
# if prefix is 0x00 0x00 0x00 0x02 then the "reason" of partial read failure is "sensor is dirty"
PARTIAL_READ_FAILED_SENSOR_DIRTY_REGEX  = re.compile(READ_PREFIX + b'(.|\n)(.|\n)\x00\x00\x00\x02(.|\n){0,}')
# otherwise still mark it as "partial read failure" with unknown "reason"

# TODO: Update driver to only care about 0x90 0x00 suffix for partial read success and don't worry about prefix
PARTIAL_READ_SUCCESS_REGEX = re.compile(READ_PREFIX + b'(.|\n){0,}\x90\x00') # Maybe we don't need to care about this one? also some bytes seem to increment/decrement based on which valid_read this is, we could use this if we did not want to keep track of read number in our code

# TODO: Also check 0x90 0x00 after committing to ensure that print was successfully committed
# What this will mean is to create and add a new callback function at line 1117 which checks the result payload with suffix 0x90 0x00
# https://gitlab.freedesktop.org/libfprint/libfprint/-/blob/master/libfprint/drivers/egismoc/egismoc.c#L1117

def enroll():

	# In the trace it seems like the Windows driver actually kicks off a read to the INTERRUPT IN in a background thread much earlier in the process and it always "stays on" in the background
	# Then you can sort of control what will be done using different commands to the BULK OUT and read results using the BULK IN
	# But here as a temporary test, we will instead just have a single thread where we kick off the read of the sensor (the INTERRUPT IN) only when we need it instead of this read always running/waiting in the background

	# Setup to read a print

	write(b'\x04\x50\x1a\x00\x00')
	print(f"Read: {read().tobytes().hex(' ')}")

	write(b'\x04\x50\x17\x01\x00')
	print(f"Read: {read().tobytes().hex(' ')}")

	print("Waiting for fingerprint on sensor. Please touch the power button...")
	wait_for_finger()
	print("Fingerprint detected!")

	write(b'\x04\x50\x17\x02\x00')
	print(f"Read: {read().tobytes().hex(' ')}")

	# Next payload from existing registered fingerprints
	write(fingers_enrolled_payload())

	# this packet returns specific hard-coded bytes if this is a good new finger to add, or some kind of longer payload if it is not
	new_finger_response = read()
	print(f"Read: {new_finger_response.tobytes().hex(' ')}")
	if not FINGER_NOT_YET_ENROLLED_REGEX.fullmatch(new_finger_response):
		raise ValueError('That fingerprint is already enrolled. Try a different finger.')

	# TODO: if this result then it is considered a bad packet payload from fingers_enrolled_payload() (bad CRC etc?)?
	#b'\xf5\x8c\x00\x00\x00\x02\x6f\xe1'

	# perform a sdcp_connect
	connect_response_raw = egismoc_sdcp_connect()
	print(f"egismoc SDCP ConnectResponse: {connect_response_raw.tobytes().hex(' ')}")
	# parse the connect response so the various fields can be used later
	connect_response = parse_sdcp_connect_response(connect_response_raw)
	host_ecdh.load_received_public_key_bytes(connect_response.pk_f)
	key_agreement = host_ecdh.generate_sharedsecret_bytes()

	# "derive master secret"
	# take key_agreement as "key"
	# label = "master secret"
	# context = "random"; 64-byte long concat of r_h + r_d
	# I *think* that it should be to kdf.derive(key_agreement) using above params for kdf
	kdf_master_secret = KBKDFHMAC(
		algorithm=hashes.SHA256(),
		mode=Mode.CounterMode,
		length=32,
		rlen=4,
		llen=4,
		location=CounterLocation.BeforeFixed,
		label=b'master secret\x00', # hard-coded label to use for Master Secret as-specified in SDCP
		context=host_random + connect_response.r_d, # context is concat of r_h + r_d as per SDCP
		fixed=None,
	)
	master_secret = kdf_master_secret.derive(key_agreement)

	kdf_application_keys = KBKDFHMAC(
		algorithm=hashes.SHA256(),
		mode=Mode.CounterMode,
		length=32,
		rlen=4,
		llen=4,
		location=CounterLocation.BeforeFixed,
		label=b'application keys\x00', # hard-coded label to use for Application Leys as-specified in SDCP
		context=None, # no context for Application Keys as per SDCP
		fixed=None,
	)
	# application_keys is what SDCP calls the "MAC secret `s`, and symmetric key `k`"
	application_keys = kdf_application_keys.derive(master_secret)

	write(b'\x07\x50\x16\x01\x00\x00\x00\x20')
	enrollment_nonce_response = read()
	print(f"Read: {enrollment_nonce_response.tobytes().hex(' ')}")
	enrollment_nonce = enrollment_nonce_response[14:14+32].tobytes() # enrollment_nonce is 32 bytes starting at position 14

	# new_finger_id should be `MAC(s, b'enroll' + enrollment_nonce)` according to the spec: https://github.com/Microsoft/SecureDeviceConnectionProtocol/wiki/Secure-Device-Connection-Protocol#enrollment
	# but what is `s` ? It should be a secret that is created from the connect_response + some kind of host keys??
	
	new_finger_id = hmac.new(key=application_keys, msg=b'enroll' + enrollment_nonce + b'\x00', digestmod=hashlib.sha256).digest()
	#new_finger_id = hmac.new(key=application_keys, msg=b'enroll\x00' + enrollment_nonce, digestmod=hashlib.sha256).digest()
	## new_finger_id = hmac.new(key=enrollment_nonce, msg=b'enroll\x00', digestmod=hashlib.sha256).digest()

	write(b'\x04\x50\x1a\x00\x00')
	print(f"Read: {read().tobytes().hex(' ')}")

	write(b'\x04\x50\x16\x02\x01')
	print(f"Read: {read().tobytes().hex(' ')}")

	read_prompt = "Began registration of a new fingerprint. Please touch the sensor again..."

	valid_reads = 0
	while valid_reads < NUM_ENROLL_STAGES:
		print(read_prompt)
		wait_for_finger()
		print("Fingerprint detected!")

		# TODO: Add below pre-sensor read command quirk for 0588 
		write(b'\x07\x50\x7a\x00\x00\x00\x00\x80')
		print(f"Read: {read().tobytes().hex(' ')}")

		write(b'\x07\x50\x16\x02\x02\x00\x00\x02')

		finger_read_response = read()
		print(f"Read: {finger_read_response.tobytes().hex(' ')}")

		# Check read success; retry failures without incrementing valid_reads
		is_valid = False
		# TODO: Update driver logic to work like this for partial read failures
		if PARTIAL_READ_FAILED_REGEX.fullmatch(finger_read_response):
			if PARTIAL_READ_FAILED_NOT_IN_CENTER_REGEX.fullmatch(finger_read_response):
				read_prompt = "Finger was not centered on the sensor. Please try to move to the center and try again..." #TODO how does Windows driver tell difference between higher/lower/left/right?
			elif PARTIAL_READ_FAILED_SENSOR_DIRTY_REGEX.fullmatch(finger_read_response):
				read_prompt = "The sensor appears dirty or cannot recognize you, please try again..."
			else:
				read_prompt = "Failed to read print with unknown reason. Please try again..."
		elif not PARTIAL_READ_SUCCESS_REGEX.fullmatch(finger_read_response):
			raise ValueError("Unknown response from partial read.")
		else:
			is_valid = True

		if valid_reads < (NUM_ENROLL_STAGES - 1) or not is_valid:
			write(b'\x04\x50\x1a\x00\x00')
			print(f"Read: {read().tobytes().hex(' ')}")

			write(b'\x04\x50\x16\x02\x01')
			print(f"Read: {read().tobytes().hex(' ')}")
		else:
			write(b'\x07\x50\x16\x05\x00\x00\x00\x20')
			print(f"Read: {read().tobytes().hex(' ')}")

			# Build new enrolled fingerprint identifier payload
			# first is a hardcoded string of bytes
			payload = b'\x27\x50\x16\x03\x00\x00\x00\x20'
			# Then the rest is actually the "identifier" for the fingerprint (which is sent back from device later) - how should this be generated?
			# I think the driver is actually creating and assigning these here? Not sure how it is generated, maybe start with just generating a new 32 byte token?
			# new_finger_id = secrets.token_bytes(32) # TODO: Now this is generated above using SDCP
			payload += new_finger_id

			# new_finger_hmac = hmac.new(key=host_random, msg=b'enroll\x00', digestmod=hashlib.sha256)
			# new_finger_id = new_finger_hmac.digest()
			# payload = b'\x27\x50\x16\x03\x00\x00\x00\x20' + new_finger_hmac.digest()
			# write(payload)
			# print(f"Read: {read().tobytes().hex(' ')}")

			#print(f"--- TRYING DIFFERENT FINGERPRINT ID COMBINATIONS: ---")

			# payload = b'\x27\x50\x16\x03\x00\x00\x00\x20' + enrollment_nonce
			# write(payload)
			# print(f"Read: {read().tobytes().hex(' ')}")

			def try_write_new_finger(hmac: hmac.HMAC):
				global new_finger_id
				new_finger_id = hmac.digest()
				global payload
				payload = b'\x27\x50\x16\x03\x00\x00\x00\x20' + new_finger_id
				write(payload)
				print(f"Read: {read().tobytes().hex(' ')}")
			
			def hm(key, msg):
				return hmac.new(key=key, msg=msg, digestmod=hashlib.sha256)

#			try_write_new_finger(hm(application_keys, b'enroll\x00nroll\x00roll\x00oll\x00ll\x00l\x00\x00'))
			try_write_new_finger(hm(enrollment_nonce, b'enroll\x00nroll\x00roll\x00oll\x00ll\x00l\x00'))
#			try_write_new_finger(hm(enrollment_nonce, b'enroll\x00'))
#			try_write_new_finger(hm(connect_response.pk_d, b'enroll\x00'))
#			try_write_new_finger(hm(connect_response.pk_f, b'enroll\x00'))
#			try_write_new_finger(hm(connect_response.r_d, b'enroll\x00'))
#			try_write_new_finger(hm(host_random, b'enroll\x00'))
#			try_write_new_finger(hm(host_public_key.to_string(), b'enroll\x00'))

			# TODO: Here we should check the read payload to see if it was actually success or not
			# TODO: In theory this should be "per user" e.g. per os.getlogin() and then that these IDs per user are saved somewhere like a file or database?
			fingers_enrolled.append(new_finger_id)
			print("Success! New fingerprint added.")

		if is_valid:
			valid_reads += 1
			read_prompt = f"Great job! Please touch the sensor again... ({valid_reads}/{NUM_ENROLL_STAGES})"



### VERIFY ###

# Sensor read response checks during verification

# "Verified" seems to be a prefix of 2 bytes (?), then "00 00 00 00 42", then 32 bytes of "something?" (is this the user ID?), then a 32 byte id of the fingerprint which was verified, then "90 00"
# So I assume you can figure out which user is associated with the verification based on which users has this fingerprint ID
VERIFIED_REGEX     = re.compile(READ_PREFIX + b'(.|\n)(.|\n)\x00\x00\x00\x42(.|\n){32}((.|\n){32})\x90\x00') # TODO: think this is still not working exactly right to capture the ID?

# If "not verified," instead of matching the above pattern it seems like it is usually a hardcoded byte string on the same read?
NOT_VERIFIED_REGEX = re.compile(READ_PREFIX + b'\xd5\x69\x00\x00\x00\x02\x90\x04')

def verify():

	if len(fingers_enrolled) == 0:
		raise ValueError('No fingers are enrolled!')

	# setup to read a print - in the trace this seems to be done after the read is kicked off on INTERRUPT IN but is it ok to do single-threaded like this?
	write(b'\x04\x50\x17\x01\x01')
	print(f"Read: {read().tobytes().hex(' ')}")

	print("Waiting for fingerprint on sensor. Please touch the power button...")
	wait_for_finger()
	print("Fingerprint detected!")

	# post-processing of some kind?
	write(b'\x04\x50\x17\x02\x00')
	print(f"Read: {read().tobytes().hex(' ')}")

	# Next payload from existing registered fingerprints
	write(fingers_enrolled_payload())
	verify_finger_payload = read()
	print(f"Read: {verify_finger_payload.tobytes().hex(' ')}")

	result = False
	mtch = VERIFIED_REGEX.match(verify_finger_payload)
	if not mtch:
		result = False
		print('Your fingerprint could not be recognized. Please try a different finger.')
	else:
		result = True
		print("Matched fingerprint! TODO: capture ID and match vs user")

	## TODO: This capture / check may not be needed but also seems to be an issue with the regex/logic -- comment out for now...
	#finger_id = mtch.group(4) # needs to be 4 due to workaround with (.|\n), so the finger ID is the 5th capture group we can get from the match
	#if finger_id in fingers_enrolled:
	#	print(f"Found and matched fingerprint {finger_id} !")
	#else:
	#	raise ValueError('Fingerprint seemed to be valid but could not be found in existing list of enrolled prints; what happened???')

	write(b'\x04\x50\x1a\x00\x00')
	print(f"Read: {read().tobytes().hex(' ')}")

	write(b'\x04\x50\x17\x01\x01')
	print(f"Read: {read().tobytes().hex(' ')}")

	write(b'\x04\x50\x04\x01\x00')
	print(f"Read: {read().tobytes().hex(' ')}")

	# Get a response from the sensor a second time - why?
	print("Getting second response from sensor...")
	second_finger_response = wait_for_finger()
	# TODO: does this need to be checked for valid/invalid ?
	print("Second response detected!")
	print(f"Read: {second_finger_response.tobytes().hex(' ')}")

	write(b'\x04\x50\x04\x02\x00')
	print(f"Read: {read().tobytes().hex(' ')}")

	return result



### WIPE ###

def wipe():

	if len(fingers_enrolled) == 0:
		raise ValueError('No fingers are enrolled!')

	# Build the full payload for the packet

	# ("num fingers regd * 20" + "7")
	payload = (((len(fingers_enrolled)) * 0x20) + 0x07).to_bytes()
	# then 50 18 04 00 00 00
	payload += b'\x50\x18\x04\x00\x00\x00'
	# then ("num fingers regd * 20")
	payload += ((len(fingers_enrolled)) * 0x20).to_bytes()
	# Then the fingerprint IDs from above
	for f in reversed(fingers_enrolled):
		payload += f

	write(payload)
	print(f"Read: {read().tobytes().hex(' ')}") # TODO check for success? is this always READ_PREFIX + '\xd5\x6d\x00\x00\x00\x02\x90\x00' when success?

	# TODO: how to know it was "valid" or not? The read() above seems to throw a device I/O exception if there was a failure, maybe that is good enough?
	print("Wipe successful!")
	return True



def main(args):
	if args["info"]:
		setup()
		info()
	if args["enroll"]:
		setup()
		enroll()
	if args["verify"]:
		setup()
		verify()
	if args["wipe"]:
		setup()
		wipe()

if __name__ == '__main__':
	#args = docopt(__doc__.replace("ARGV0", sys.argv[0]))
	#main(args)
	setup()
	#verify()
	enroll()