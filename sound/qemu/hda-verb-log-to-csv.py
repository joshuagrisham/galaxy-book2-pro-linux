# Cleans log from my patched QEMU (see https://github.com/joshuagrisham/galaxy-book2-pro-linux/tree/main/sound/qemu) and reformats the output into CSV

import re
import sys

try:
    src = open(sys.argv[1], "r")
except Exception as e:
    print(str(e))
    exit()

print(','.join([
    "datetime",
    "datetime_ms",
    "readwrite",
    "caddr",
    "nid",
    "control",
    "param",
    "response",
]))

for line in src.readlines():
    values = re.search(r'^([A-z]{3} [A-z]{3} [0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9] [0-9]{4})\s\[([0-9]{0,})\]:\s(read|write).+caddr:(0x[0-9A-Fa-f]+) nid:(0x[0-9A-Fa-f]+) control:(0x[0-9A-Fa-f]+) param:(0x[0-9A-Fa-f]+)( response:(0x[0-9A-Fa-f]+)|)', line)
    if values != None and values.group() != None:
        if values.group(3) == "read":
            print(','.join([
                values.group(1),
                values.group(2),
                values.group(3),
                values.group(4),
                values.group(5),
                values.group(6),
                values.group(7),
                values.group(9),
            ]))
        if values.group(3) == "write":
            print(','.join([
                values.group(1),
                values.group(2),
                values.group(3),
                values.group(4),
                values.group(5),
                values.group(6),
                values.group(7),
                "",
            ]))

src.close()
