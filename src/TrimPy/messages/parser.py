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

from re import match
import TrimPy


def parseOptions(options, trimSocket):
    if (options.name is not None):
        trimSocket.sendall(TrimPy.formatNameMsg(options.name))
    if (options.query is not None):
        trimSocket.sendall(TrimPy.formatQueryPatternMsg(options.query))
        queryData = trimSocket.recv(1024)
        TrimPy.parseQueryData(queryData, options.verbose)
    if (options.update is not None):
        message = TrimPy.formatUpdatePatternMsg(trimSocket, options)
        if (message is not None):
            trimSocket.sendall(message)
    if (options.delete is not None):
        trimSocket.sendall(TrimPy.formatDeletePatternMsg(options.delete))
    if (options.count is not None):
        trimSocket.sendall(TrimPy.formatDotMsg(options.count))
    if (options.pattern is not None):
        trimSocket.sendall(TrimPy.formatDispMsg(options.pattern.upper()))
    if (options.mode is not None):
        trimSocket.sendall(TrimPy.formatModeMsg(options.mode))


def parseQueryData(queryData, verbose):
    if (verbose is True):
        print('Recieved:', queryData.hex())
    if (match(b'\x5a\xff.*\xff\xa5', queryData)):
        print('Pattern number invalid!')
    else:
        print('Pattern Name:', queryData[2:26].decode("ASCII"))
        print('Animation:', TrimPy.Animation(queryData[28]))
        print('Speed:', int(queryData[29]))
        print('Brightness:', int(queryData[30]))
        print('Dot Repetition:', int(queryData[31]), '|', int(queryData[32]), '|', int(queryData[33]), '|',
              int(queryData[34]), '|', int(queryData[35]), '|', int(queryData[36]), '|', int(queryData[37]))
        print('Dot RGB hex:', queryData[38:41].hex(), '|', queryData[41:44].hex(), '|', queryData[44:47].hex(), '|',
              queryData[47:50].hex(), '|', queryData[50:53].hex(), '|', queryData[53:56].hex(), '|',
              queryData[56:59].hex())
