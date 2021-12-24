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

from datetime import datetime
from TrimPy import Trim, Pattern, Mode
from .helpers import randByte, validatePatternOptions
from .parser import parsePatternOptions
from re import match


def formatConnMsg(verbose):
    pad1 = randByte()
    pad2 = randByte()
    pad3 = randByte()
    date = datetime.now()
    year = int(date.strftime("%y"))
    month = int(date.strftime("%m"))
    day = int(date.strftime("%d"))
    wkday = int(date.strftime("%w")) + 1  # Python zero indexes from Sunday for week day
    hour = int(date.strftime("%H"))
    minute = int(date.strftime("%M"))
    second = int(date.strftime("%S"))
    date = bytes([pad1, pad2, pad3, year, month, day, wkday, hour, minute, second])
    length = bytes([len(date) >> 8, len(date)])
    n = (pad3 << 5 | pad1 >> 3 & 31 & pad2).to_bytes(2, 'big')
    if (verbose is True):
        print('Verify byte:', n[1:2].hex())
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
    pattern = bytes([p])
    length = bytes([len(pattern) >> 8, len(pattern)])
    return bytes([Trim.START.value, Trim.QUERY_PATTERN.value]) + length + pattern + bytes([Trim.END.value])


def formatUpdatePatternMsg(trimSocket, options):
    querySrc = checkPatternNumber(trimSocket, options.src, options.verbose)
    queryDst = checkPatternNumber(trimSocket, options.dest, options.verbose)
    if (not validatePatternOptions(options, querySrc)):
        return

    p1 = bytearray([int(options.dest)])
    p2 = bytearray(options.patName.ljust(24, '\0'), "ASCII") if (options.patName is not None) else querySrc[2:26]
    p3 = querySrc[26:28] + parsePatternOptions(options, bytearray(querySrc[28:59]))
    request = p1 + p2 + p3
    length = bytes([len(request) >> 8, len(request)])
    cmd = Trim.CREATE_PATTERN.value if (queryDst is None) else Trim.UPDATE_PATTERN.value

    return bytes([Trim.START.value, cmd]) + length + request + bytes([Trim.END.value])


def formatPreviewPatternMsg(trimSocket, options):
    querySrc = checkPatternNumber(trimSocket, options.src, options.verbose)
    if (not validatePatternOptions(options, querySrc)):
        return

    request = (querySrc[26:28] + parsePatternOptions(options, bytearray(querySrc[28:59]))
               if (querySrc is not None) else parsePatternOptions(options, bytearray(32)))
    length = bytes([len(request) >> 8, len(request)])
    return bytes([Trim.START.value, Trim.PREVIEW_PATTERN.value]) + length + request + bytes([Trim.END.value])


def formatDeletePatternMsg(p):
    pattern = bytes([p])
    length = bytes([len(pattern) >> 8, len(pattern)])
    return bytes([Trim.START.value, Trim.DELETE_PATTERN.value]) + length + pattern + bytes([Trim.END.value])


def formatDotMsg(c):
    count = c.to_bytes(2, 'big')
    length = bytes([len(count) >> 8, len(count)])
    return bytes([Trim.START.value, Trim.DOT_COUNT.value]) + length + count + bytes([Trim.END.value])


def checkPatternNumber(trimSocket, num, verbose):
    if (num is not None):
        trimSocket.sendall(formatQueryPatternMsg(num))
        queryData = trimSocket.recv(1024)
        if verbose:
            print('Recieved:', queryData.hex())
        if (match(b'\x5a\xff.*\xff\xa5', queryData)):
            print('Pattern number provided does not exist!')
            return
        return queryData
