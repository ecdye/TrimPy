# TrimPy: A basic API implementation for Trimlight Select systems,
# Copyright (C) 2021-2025 Ethan Dye
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

import TrimPy


def parseOptions(options, trimSocket):  # noqa: C901
    if (options.mode is not None):
        trimSocket.sendall(TrimPy.formatModeMsg(options.mode))
    if (options.pattern is not None):
        trimSocket.sendall(TrimPy.formatDispMsg(options.pattern.upper()))
    if (options.name is not None):
        trimSocket.sendall(TrimPy.formatNameMsg(options.name))
    if (options.query is not None):
        queryData = TrimPy.checkPatternNumber(trimSocket, options.query, options.verbose)
        parseQueryData(queryData)
    if (options.preview is not False):
        message = TrimPy.formatPreviewPatternMsg(trimSocket, options)
        if (message is not None):
            trimSocket.sendall(TrimPy.formatModeMsg('manual'))
            trimSocket.sendall(message)
    elif (options.dest is not None):
        message = TrimPy.formatUpdatePatternMsg(trimSocket, options)
        if (message is not None):
            trimSocket.sendall(message)
    if (options.delete is not None):
        trimSocket.sendall(TrimPy.formatDeletePatternMsg(options.delete))
    if (options.count is not None):
        trimSocket.sendall(TrimPy.formatDotMsg(options.count))


def parsePatternOptions(options, request):
    request[0:1] = bytes([TrimPy.Animation[options.animation].value]) if (options.animation is not None) else request[0:1]
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


def parseQueryData(queryData):
    pattern_name = queryData[2:26].decode("ASCII").strip()
    animation = TrimPy.Animation(queryData[28])
    speed = int(queryData[29])
    brightness = int(queryData[30])
    dot_repetition = [str(int(b)) for b in queryData[31:38]]
    dot_colors = [queryData[i: i + 3].hex() for i in range(38, 57, 3)]

    print("Pattern Name:", pattern_name)
    print("Animation:", animation)
    print("Speed:", speed)
    print("Brightness:", brightness)
    print("Dot Repetition:", " | ".join(dot_repetition))
    print("Dot RGB hex:", " | ".join(dot_colors))
