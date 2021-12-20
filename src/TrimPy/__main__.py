# TrimPy: A basic API implementation for Trimlight Select systems,
# Copyright (C) 2021 Ethan Dye
#
# TrimPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# TrimPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TrimPy. If not, see <https://www.gnu.org/licenses/>.

from optparse import OptionParser, OptionGroup
import TrimPy
import socket
import sys


def main() -> int:
    parser = OptionParser(usage="Usage: TrimPy [options]")
    parser.add_option("-i", "--ip", help="IP address to connect to (required)")
    parser.add_option("-m", "--mode", help="set trimlight to mode: timer, or manual")
    parser.add_option("-p", "--pattern", help=f"set trimlight to pattern: {', '.join([p.name for p in TrimPy.Pattern])} "
                      "(also accepts custom values in the form of integers representing the pattern number)")
    parser.add_option("-n", "--set-name", dest="name", help="set trimlight device name (< 25 characters)")
    parser.add_option("-d", "--dot-count", dest="count", type="int", help="set trimlight device dot count to N (< 4096 dots)",
                      metavar="N")
    parser.add_option("-q", "--query-pattern", dest="query", help="query trimlight for information about pattern number N",
                      metavar="N")
    parser.add_option("-D", "--delete-pattern", dest="delete", type="int", help="delete pattern number N", metavar="N")
    parser.add_option("-v", "--verbose", action="store_true", default=False, help="make lots of noise [default: %default]")
    parser.add_option("-V", "--version", action="store_true", default=False, help="print version and exit")

    group = OptionGroup(parser, "Create/Update Pattern", "create/update a trimlight pattern number to match your liking")
    group.add_option("--update-pattern", dest="update", help="pattern number N to update or create", metavar="N")
    group.add_option("--name", dest="patName", help="set pattern name (< 25 characters)")
    group.add_option("--animation", dest="animation", help="set animation style: "
                     f"{', '.join([a.name for a in TrimPy.Animation])}")
    group.add_option("--speed", dest="speed", type="int", help="set animation speed [0-255]")
    group.add_option("--brightness", dest="brightness", type="int", help="set brightness [0-255]")
    group.add_option("--color-one", nargs=3, type="int", help="set 'R G B' integer values for color index one",
                     metavar="R G B")
    group.add_option("--color-two", nargs=3, type="int", help="set 'R G B' integer values for color index two",
                     metavar="R G B")
    group.add_option("--color-three", nargs=3, type="int", help="set 'R G B' integer values for color index three",
                     metavar="R G B")
    group.add_option("--color-four", nargs=3, type="int", help="set 'R G B' integer values for for color index four",
                     metavar="R G B")
    group.add_option("--color-five", nargs=3, type="int", help="set 'R G B' integer values for color index five",
                     metavar="R G B")
    group.add_option("--color-six", nargs=3, type="int", help="set 'R G B' integer values for color index six",
                     metavar="R G B")
    group.add_option("--color-seven", nargs=3, type="int", help="set 'R G B' integer values for color index seven",
                     metavar="R G B")
    group.add_option("--count-one", type="int", help="set color index one to repeat N times [0-30]", metavar="N")
    group.add_option("--count-two", type="int", help="set color index two to repeat N times [0-30]", metavar="N")
    group.add_option("--count-three", type="int", help="set color index three to repeat N times [0-30]", metavar="N")
    group.add_option("--count-four", type="int", help="set color index four to repeat N times [0-30]", metavar="N")
    group.add_option("--count-five", type="int", help="set color index five to repeat N times [0-30]", metavar="N")
    group.add_option("--count-six", type="int", help="set color index six to repeat N times [0-30]", metavar="N")
    group.add_option("--count-seven", type="int", help="set color index seven to repeat N times [0-30]", metavar="N")
    parser.add_option_group(group)

    (options, args) = parser.parse_args()
    if (options.version is True):
        print("TrimPy", TrimPy.__version__)
        print('Copyright (C) 2021 Ethan Dye')
        print('License GPLv3: GNU GPL version 3 <https://gnu.org/licenses/gpl.html>.\n')
        print('TrimPy is free software: you are free to change and redistribute it.')
        print('There is NO WARRANTY, to the extent permitted by law.')
        return 0
    elif (options.ip is None):
        parser.print_help()
        return 0

    trimSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to trimlight
    trimSocket.connect((options.ip, TrimPy.Trim.PORT.value))
    trimSocket.sendall(TrimPy.formatConnMsg())
    connData = trimSocket.recv(1024)

    nameLen = connData[3] + 4
    pixCntStart = nameLen + 2  # Skip padding after Device name
    pixCntEnd = nameLen + 4  # Pixel count is represented as two bytes in hex

    deviceName = connData[4:nameLen].decode("ASCII")
    pixelCount = int.from_bytes(connData[pixCntStart:pixCntEnd], 'big')

    if (options.verbose is True):
        print('Recieved:', connData.hex())
        print('Device Name:', deviceName)
        print('Pixel Count:', pixelCount)

    TrimPy.parseOptions(options, trimSocket)

    trimSocket.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
