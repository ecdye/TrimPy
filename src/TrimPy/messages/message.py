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
from TrimPy import Trim, Pattern, Animation, Mode
from .helpers import randByte
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
    pattern = bytes([int(p)])
    length = bytes([len(pattern) >> 8, len(pattern)])
    return bytes([Trim.START.value, Trim.QUERY_PATTERN.value]) + length + pattern + bytes([Trim.END.value])


def formatUpdatePatternMsg(trimSocket, options):
    trimSocket.sendall(formatQueryPatternMsg(options.update))
    queryData = trimSocket.recv(1024)

    if (((options.patName is None) or (options.animation is None) or
       (options.speed is None) or (options.brightness is None) or
       (options.count_one is None) or (options.count_two is None) or
       (options.count_three is None) or (options.count_four is None) or
       (options.count_five is None) or (options.count_six is None) or
       (options.count_seven is None) or (options.color_one is None) or
       (options.color_two is None) or (options.color_three is None) or
       (options.color_four is None) or (options.color_five is None) or
       (options.color_six is None) or (options.color_seven is None)) and
       (match(b'\x5a\xff.*\xff\xa5', queryData))):
        print('Pattern number to update does not exist!')
        print('To create a new pattern, all options must be provided.')
        return

    request = formatPattern(options, bytearray(queryData[28:59]))
    request = (bytes(options.update) +
               bytearray(options.patName.ljust(24, '\0'), "ASCII") if (options.patName is not None) else queryData[2:26] +
               request)
    length = bytes([len(request) >> 8, len(request)])
    cmd = Trim.CREATE_PATTERN.value if match(b'\x5a\xff.*\xff\xa5', queryData) else Trim.UPDATE_PATTERN.value

    return bytes([Trim.START.value, cmd]) + length + request + bytes([Trim.END.value])


def formatPreviewPatternMsg(options):
    if ((options.patName is None) or (options.animation is None) or
       (options.speed is None) or (options.brightness is None) or
       (options.count_one is None) or (options.count_two is None) or
       (options.count_three is None) or (options.count_four is None) or
       (options.count_five is None) or (options.count_six is None) or
       (options.count_seven is None) or (options.color_one is None) or
       (options.color_two is None) or (options.color_three is None) or
       (options.color_four is None) or (options.color_five is None) or
       (options.color_six is None) or (options.color_seven is None)):
        print('To test a new pattern, all options must be provided.')
        return

    request = formatPattern(options, bytearray(32))
    length = bytes([len(request) >> 8, len(request)])
    return bytes([Trim.START.value, Trim.PREVIEW_PATTERN.value]) + length + request + bytes([Trim.END.value])


def formatPattern(options, request):
    request[0:1] = bytes([Animation[options.animation].value]) if (options.animation is not None) else request[0:1]
    request[1:2] = bytes([options.speed]) if (options.speed is not None) else request[1:2]
    request[2:3] = bytes([options.brightness]) if (options.brightness is not None) else request[2:3]
    request[3:4] = bytes([options.count_one]) if (options.count_one is not None) else request[3:4]
    request[4:5] = bytes([options.count_two]) if (options.count_two is not None) else request[4:5]
    request[5:6] = bytes([options.count_three]) if (options.count_three is not None) else request[5:6]
    request[6:7] = bytes([options.count_four]) if (options.count_four is not None) else request[6:7]
    request[7:8] = bytes([options.count_five]) if (options.count_five is not None) else request[7:8]
    request[8:9] = bytes([options.count_six]) if (options.count_six is not None) else request[8:9]
    request[9:10] = bytes([options.count_seven]) if (options.count_seven is not None) else request[9:10]
    request[10:13] = bytes(options.color_one) if (options.color_one is not None) else request[10:13]
    request[13:16] = bytes(options.color_two) if (options.color_two is not None) else request[13:16]
    request[16:19] = bytes(options.color_three) if (options.color_three is not None) else request[16:19]
    request[19:22] = bytes(options.color_four) if (options.color_four is not None) else request[19:22]
    request[22:25] = bytes(options.color_five) if (options.color_five is not None) else request[22:25]
    request[25:28] = bytes(options.color_six) if (options.color_six is not None) else request[25:28]
    request[28:31] = bytes(options.color_seven) if (options.color_seven is not None) else request[28:31]

    return request


def formatDeletePatternMsg(p):
    pattern = bytes([p])
    length = bytes([len(pattern) >> 8, len(pattern)])
    return bytes([Trim.START.value, Trim.DELETE_PATTERN.value]) + length + pattern + bytes([Trim.END.value])


def formatDotMsg(c):
    count = c.to_bytes(2, 'big')
    length = bytes([len(count) >> 8, len(count)])
    return bytes([Trim.START.value, Trim.DOT_COUNT.value]) + length + count + bytes([Trim.END.value])
