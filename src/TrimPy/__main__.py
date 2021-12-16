# TrimPy a tool for interfacing with Trimlight Select systems
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
from TrimPy import *
import socket
import sys
import re

def main() -> int:
    parser = OptionParser(usage = "Usage: TrimPy [options]")
    parser.add_option("-i", "--ip", help = "IP address to connect to")
    parser.add_option("-m", "--mode", help = "set trimlight to mode: timer, or manual")
    parser.add_option("-p", "--pattern", default = "DEFAULT", help = f"set trimlight to pattern: {', '.join([p.name for p in Pattern])} (also accepts custom values in the form of integers representing the pattern number) [default: %default]")
    parser.add_option("-n", "--set-name", dest = "name", help = "set trimlight device name (< 25 characters)")
    parser.add_option("-d", "--dot-count", dest = "count", type="int", help = "set trimlight device dot count (< 4096 dots)", metavar = "N")
    parser.add_option("-q", "--query-pattern", dest = "query", help = "query trimlight for information about pattern number")
    parser.add_option("-v", "--verbose", action = "store_true", default=False, help = "make lots of noise [default: %default]")
    parser.add_option("-V", "--version", action = "store_true", default=False, help = "print version and exit")

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
    if (options.version == True):
        print("TrimPy", __version__)
        print('Copyright (C) 2021 Ethan Dye')
        print('License GPLv3: GNU GPL version 3 <https://gnu.org/licenses/gpl.html>.')
        print('This is free software: you are free to change and redistribute it.')
        print('There is NO WARRANTY, to the extent permitted by law.')
        print()
        print('Written by Ethan Dye; see')
        print('<https://github.com/ecdye/TrimPy/graphs/contributors>.')
        return 0
    elif (options.ip == None):
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
    elif (options.count is not None):
        trimSocket.sendall(formatDotMsg(options.count))
    if (options.pattern is not None):
        trimSocket.sendall(formatDispMsg(options.pattern))
    if (options.mode is not None):
        trimSocket.sendall(formatModeMsg(options.mode))

    trimSocket.close()
    return 0

if __name__ == '__main__':
    sys.exit(main())
