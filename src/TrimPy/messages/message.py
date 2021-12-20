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


def formatConnMsg():
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

    request = formatPattern(options, bytearray(queryData[1:59]))
    print(request)
    exit(0)
    length = bytes([len(request) >> 8, len(request)])
    cmd = Trim.CREATE_PATTERN.value if match(b'\x5a\xff.*\xff\xa5', queryData) else Trim.UPDATE_PATTERN.value

    return bytes([Trim.START.value, cmd]) + length + request + bytes([Trim.END.value])


def formatPattern(options, request):
    request[1:25] = bytearray(options.patName.ljust(24, '\0'), "ASCII") if (options.patName is not None) else request[1:25]
    request[27:28] = bytes([Animation[options.animation].value]) if (options.animation is not None) else request[27:28]
    request[28:29] = bytes([options.speed]) if (options.speed is not None) else request[28:29]
    request[29:30] = bytes([options.brightness]) if (options.brightness is not None) else request[29:30]
    request[30:31] = bytes([options.count_one]) if (options.count_one is not None) else request[30:31]
    request[31:32] = bytes([options.count_two]) if (options.count_two is not None) else request[31:32]
    request[32:33] = bytes([options.count_three]) if (options.count_three is not None) else request[32:33]
    request[33:34] = bytes([options.count_four]) if (options.count_four is not None) else request[33:34]
    request[34:35] = bytes([options.count_five]) if (options.count_five is not None) else request[34:35]
    request[35:36] = bytes([options.count_six]) if (options.count_six is not None) else request[35:36]
    request[36:37] = bytes([options.count_seven]) if (options.count_seven is not None) else request[36:37]
    request[37:40] = bytes(options.color_one) if (options.color_one is not None) else request[37:40]
    request[40:43] = bytes(options.color_two) if (options.color_two is not None) else request[40:43]
    request[43:46] = bytes(options.color_three) if (options.color_three is not None) else request[43:46]
    request[46:49] = bytes(options.color_four) if (options.color_four is not None) else request[46:49]
    request[49:52] = bytes(options.color_five) if (options.color_five is not None) else request[49:52]
    request[52:55] = bytes(options.color_six) if (options.color_six is not None) else request[52:55]
    request[55:58] = bytes(options.color_seven) if (options.color_seven is not None) else request[55:58]

    return request


def formatDeletePatternMsg(p):
    pattern = bytes([p])
    length = bytes([len(pattern) >> 8, len(pattern)])
    return bytes([Trim.START.value, Trim.DELETE_PATTERN.value]) + length + pattern + bytes([Trim.END.value])


def formatDotMsg(c):
    count = c.to_bytes(2, 'big')
    length = bytes([len(count) >> 8, len(count)])
    return bytes([Trim.START.value, Trim.DOT_COUNT.value]) + length + count + bytes([Trim.END.value])
