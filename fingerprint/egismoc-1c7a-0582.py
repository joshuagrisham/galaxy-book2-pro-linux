#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EGIS 1C7A:0582 Match-on-Chip fingerprint reader driver PoC.

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

# find our device
dev = usb.core.find(idVendor=0x1c7a, idProduct=0x0582)
if dev is None:
	raise ValueError('Device not found')

# USB URB Device IDs for 1c7a:0582 device
USB_BULK_OUT = 0x02
USB_BULK_IN = 0x81
USB_INTERRUPT_IN = 0x83

# Number of partial enrollments needed in order to store a print
NUM_ENROLL_STAGES = 20

# Reading/Writing to the bulk in/out seems to have this kind of payload structure:
#  1) 8 bytes hard-coded prefix depending on out vs in (see below)
#  2) 2 bytes which are a kind of "check bytes" for the payload
#  3) hardcoded "00 00 00"
#  4) 2 bytes that seem to be some kind of type/subtype for different processes/events
#  5) then it seems to vary a bit more with additional payload data depending on different type of events; either some kind of payload directly or more "type" kind of stuff either before or after the payload

# TODO: Probably better/easier/nicer to move to the struct package for building payloads, but for now we will do it all super-hard-coded with bytes...

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
	return dev.read(USB_INTERRUPT_IN, length, timeout)


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

	# TODO: skip this for now and see if it works without it? otherwise wonder if this might have something to do with associated the current current user to these enrollments?
	## If first time a new finger is being enrolled for this device session, thenn some kind of client info is exchanged? not sure but will just copy what was in the trace for now...
	#if len(fingers_enrolled) == 0:
	#	# TODO is this next payload hardcoded or same every time?
	#	payload  = b'\x6b\x50\x57'
	#	payload += b'\x01\x00\x00\x00\x62\x20\x76\x6b'
	#	payload += b'\x30\x62\xb2\xc1\xc7\x18\x55\xeb'
	#	payload += b'\x3a\xf3\x90\x70\xf9\x7f\x8b\x8b'
	#	payload += b'\xda\x93\x10\xa8\x87\xc8\x75\xa0'
	#	payload += b'\xe9\x73\xbf\x70\x31\x8f\x04\xc5'
	#	payload += b'\x00\xbf\x04\x77\xe8\xd3\x09\x0f'
	#	payload += b'\x5f\xa3\x1a\x20\x23\x60\x43\x78'
	#	payload += b'\x39\xf5\x73\x49\xbd\x25\xe2\x7c'
	#	payload += b'\xe3\xa9\xc9\x07\x18\xb5\x62\xb1'
	#	payload += b'\xa5\x2b\x83\x97\x84\x17\x43\x4b'
	#	payload += b'\xd1\x1a\x47\x5b\x94\x82\xa7\x3e'
	#	payload += b'\x7d\x26\xc0\xab\x38\x57\x59\xb3'
	#	payload += b'\x0d\x86\x59\x00\xb3\x6d\xe6\x00'
	#	payload += b'\x00'
	#	write(payload)
	#	print(f"Read: {read().tobytes().hex(' ')}") # TODO this response is quite larger and seems to have a bit of Windows / device / cert info with it?

	write(b'\x07\x50\x16\x01\x00\x00\x00\x20')
	print(f"Read: {read().tobytes().hex(' ')}") # TODO this response has some kind of identifier in it? not sure what it is used for (is this the user ID?)

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
			new_finger_id = secrets.token_bytes(32)
			payload += new_finger_id
			write(payload)
			print(f"Read: {read().tobytes().hex(' ')}")
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
	args = docopt(__doc__.replace("ARGV0", sys.argv[0]))
	main(args)
