#!/usr/bin/env python3

# trimlight.py script for interfacing with Trimlight Select systems
# Copyright (C) 2021 Ethan Dye
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from optparse import OptionParser, OptionGroup
from datetime import datetime
from random import randint
from enum import Enum
import socket
import math
import sys
import re

class Trim(Enum):
    PORT = 8189
    START = 90
    END = 165
    CONN = 12
    MODE = 13
    SET_NAME = 14
    QUERY_PATTERN = 22
    UPDATE_PATTERN = 5
    DISP = 3

class Mode(Enum):
    TIMER = 0
    MANUAL = 1

# You may need to do some research / experimentation to figure out what your
# patterns correspond to. Custom patterns can also be accessed using this same
# format, they just come after the builtin patterns.
class Pattern(Enum):
    NEW_YEARS = 1
    VALENTINES = 2
    ST_PATRICKS = 3
    MOTHERS_DAY = 4
    INDEPENDENCE_DAY = 5
    DEFAULT = 6
    HALLOWEEN = 7
    THANKSGIVING = 8
    CHRISTMAS = 9

class Animation(Enum):
    STATIC = 0
    CHASE_FORWARD = 1
    CHASE_BACKWARD = 2
    MIDDLE_TO_OUT = 3
    OUT_TO_MIDDLE = 4
    STROBE = 5
    FADE = 6
    COMET_FORWARD = 7
    COMET_BACKWARD = 8
    WAVE_FORWARD = 9
    WAVE_BACKWARD = 10
    SOLID_FADE = 11

def randByte():
    while True:
        b = randint(0, 255)
        if ((b != Trim.START.value) and (b != Trim.END.value)):
             break
    return b

def formatConnMsg():
    pad1 = randByte()
    pad2 = randByte()
    pad3 = randByte()
    date = datetime.now()
    year = int(date.strftime("%y"))
    month = int(date.strftime("%m"))
    day = int(date.strftime("%d"))
    wkday = int(date.strftime("%w")) + 1 # Python zero indexes from Sunday for week day
    hour = int(date.strftime("%H"))
    minute = int(date.strftime("%M"))
    second = int(date.strftime("%S"))
    date = bytes([pad1, pad2, pad3, year, month, day, wkday, hour, minute, second])
    length = bytes([len(date) >> 8, len(date)])
    return bytes([Trim.START.value, Trim.CONN.value]) + length + date + bytes([Trim.END.value])

def formatModeMsg(m):
    mode = bytes([Mode.MANUAL.value]) if m == 'manual' else bytes([Mode.TIMER.value])
    length = bytes([len(mode) >> 8, len(mode)])
    return bytes([Trim.START.value, Trim.MODE.value]) + length + mode + bytes([Trim.END.value])

def formatDispMsg(p):
    if (p in Pattern.__members__):
        pattern = bytes([Pattern[p].value])
    else:
        pattern = bytes([int(p)])
    length = bytes([len(pattern) >> 8, len(pattern)])
    return bytes([Trim.START.value, Trim.DISP.value]) + length + pattern + bytes([Trim.END.value])

def formatNameMsg(n):
    name = bytearray(n, "ASCII")
    length = bytes([len(name) >> 8, len(name)])
    return bytes([Trim.START.value, Trim.SET_NAME.value]) + length + name + bytes([Trim.END.value])

def formatQueryPatternMsg(p):
    pattern = bytes([int(p)])
    length = bytes([len(pattern) >> 8, len(pattern)])
    return bytes([Trim.START.value, Trim.QUERY_PATTERN.value]) + length + pattern + bytes([Trim.END.value])

def formatUpdatePatternMsg(trimSocket, options):
    trimSocket.sendall(formatQueryPatternMsg(options.update))
    queryData = trimSocket.recv(1024)
    if (re.match(b'\x5a\xff.*\xff\xa5', queryData)):
        print('Pattern number to update does not exist!')
        return

    request = bytearray(queryData[1:59])
    if (options.patName is not None):
        request[1:25] = bytearray(options.patName.ljust(24, '\0'), "ASCII")
    if (options.animation is not None):
        request[27:28] = bytes([Animation[options.animation].value])
    if (options.speed is not None):
        request[28:29] = bytes([options.speed])
    if (options.brightness is not None):
        request[29:30] = bytes([options.brightness])
    if (options.count_one is not None):
        request[30:31] = bytes([options.count_one])
    if (options.count_two is not None):
        request[31:32] = bytes([options.count_two])
    if (options.count_three is not None):
        request[32:33] = bytes([options.count_three])
    if (options.count_four is not None):
        request[33:34] = bytes([options.count_four])
    if (options.count_five is not None):
        request[34:35] = bytes([options.count_five])
    if (options.count_six is not None):
        request[35:36] = bytes([options.count_six])
    if (options.count_seven is not None):
        request[36:37] = bytes([options.count_seven])
    if (options.color_one is not None):
        request[37:40] = bytes(options.color_one)
    if (options.color_two is not None):
        request[40:43] = bytes(options.color_two)
    if (options.color_three is not None):
        request[43:46] = bytes(options.color_three)
    if (options.color_four is not None):
        request[46:49] = bytes(options.color_four)
    if (options.color_five is not None):
        request[49:52] = bytes(options.color_five)
    if (options.color_six is not None):
        request[52:55] = bytes(options.color_six)
    if (options.color_seven is not None):
        request[55:58] = bytes(options.color_seven)
    length = bytes([len(request) >> 8, len(request)])

    return bytes([Trim.START.value, Trim.UPDATE_PATTERN.value]) + length + request + bytes([Trim.END.value])

def main() -> int:
    parser = OptionParser()
    parser.add_option("-i", "--ip", help = "IP address to connect to")
    parser.add_option("-m", "--mode", help = "set trimlight to mode: timer, or manual")
    parser.add_option("-p", "--pattern", default = "DEFAULT", help = f"set trimlight to pattern: {', '.join([p.name for p in Pattern])} (also accepts custom values in the form of integers representing the pattern number) [default: %default]")
    parser.add_option("-n", "--set-name", dest = "name", help = "set trimlight device name (< 25 characters)")
    parser.add_option("-q", "--query-pattern", dest = "query", help = "query trimlight for information about pattern number")
    parser.add_option("-v", "--verbose", action = "store_true", default=False, help = "make lots of noise [default: %default]")

    group = OptionGroup(parser, "Update Pattern", "update a trimlight pattern number to match your liking")
    group.add_option("--update-pattern", dest = "update", help = "pattern number N to update", metavar="N")
    group.add_option("--name", dest = "patName", help = "set pattern name (< 25 characters)")
    group.add_option("--animation", dest = "animation", help = f"set animation style: {', '.join([a.name for a in Animation])}")
    group.add_option("--speed", dest = "speed", type="int", help = "set animation speed [0-255]")
    group.add_option("--brightness", dest = "brightness", type="int", help = "set brightness [0-255]")
    group.add_option("--color-one", nargs=3, type="int", help="set 'R G B' integer values for color index one", metavar="R G B")
    group.add_option("--color-two", nargs=3, type="int", help="set 'R G B' integer values for color index two", metavar="R G B")
    group.add_option("--color-three", nargs=3, type="int", help="set 'R G B' integer values for color index three", metavar="R G B")
    group.add_option("--color-four", nargs=3, type="int", help="set 'R G B' integer values for for color index four", metavar="R G B")
    group.add_option("--color-five", nargs=3, type="int", help="set 'R G B' integer values for color index five", metavar="R G B")
    group.add_option("--color-six", nargs=3, type="int", help="set 'R G B' integer values for color index six", metavar="R G B")
    group.add_option("--color-seven", nargs=3, type="int", help="set 'R G B' integer values for color index seven", metavar="R G B")
    group.add_option("--count-one", type="int", help="set color index one to repeat N times [0-30]", metavar="N")
    group.add_option("--count-two", type="int", help="set color index two to repeat N times [0-30]", metavar="N")
    group.add_option("--count-three", type="int", help="set color index three to repeat N times [0-30]", metavar="N")
    group.add_option("--count-four", type="int", help="set color index four to repeat N times [0-30]", metavar="N")
    group.add_option("--count-five", type="int", help="set color index five to repeat N times [0-30]", metavar="N")
    group.add_option("--count-six", type="int", help="set color index six to repeat N times [0-30]", metavar="N")
    group.add_option("--count-seven", type="int", help="set color index seven to repeat N times [0-30]", metavar="N")
    parser.add_option_group(group)

    (options, args) = parser.parse_args()
    if (options.ip == None):
        parser.print_help()
        return 0

    trimSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to trimlight
    trimSocket.connect((options.ip, Trim.PORT.value))
    trimSocket.sendall(formatConnMsg())
    connData = trimSocket.recv(1024)

    nameLen = connData[3] + 4
    pixCntStart = nameLen + 2 # Skip padding after Device name
    pixCntEnd = nameLen + 4 # Pixel count is represented as two bytes in hex

    deviceName = connData[4:nameLen].decode("ASCII")
    pixelCount = int.from_bytes(connData[pixCntStart:pixCntEnd], 'big')

    if (options.verbose == True):
        print('Recieved:', connData.hex())
        print('Device Name:', deviceName)
        print('Pixel Count:', pixelCount)

    if (options.name is not None):
        trimSocket.sendall(formatNameMsg(options.name))
    elif (options.query is not None):
        trimSocket.sendall(formatQueryPatternMsg(options.query))
        queryData = trimSocket.recv(1024)
        if (re.match(b'\x5a\xff.*\xff\xa5', queryData)):
            print('Pattern number invalid!')
        else:
            if (options.verbose == True):
                print('Recieved:', queryData.hex())
            print('Pattern Name:', queryData[2:26].decode("ASCII"))
            print('Animation:', Animation(queryData[28]))
            print('Speed:', int(queryData[29]))
            print('Brightness:', int(queryData[30]))
            print('Dot Repetition:', int(queryData[31]), '|', int(queryData[32]), '|', int(queryData[33]), '|', int(queryData[34]), '|', int(queryData[35]), '|', int(queryData[36]), '|', int(queryData[37]))
            print('Dot RGB hex:', queryData[38:41].hex(), '|', queryData[41:44].hex(), '|', queryData[44:47].hex(), '|', queryData[47:50].hex(), '|', queryData[50:53].hex(), '|', queryData[53:56].hex(), '|', queryData[56:59].hex())
    elif (options.update is not None):
        message = formatUpdatePatternMsg(trimSocket, options)
        if (message is not None):
            trimSocket.sendall(message)
    if (options.pattern is not None):
        trimSocket.sendall(formatDispMsg(options.pattern))
    if (options.mode is not None):
        trimSocket.sendall(formatModeMsg(options.mode))

    trimSocket.close()
    return 0

if __name__ == '__main__':
    sys.exit(main())
