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

from enum import Enum


class Trim(Enum):
    PORT = 8189
    START = 90
    END = 165
    CONN = 12
    MODE = 13
    SET_NAME = 14
    QUERY_PATTERN = 22
    CREATE_PATTERN = 6
    UPDATE_PATTERN = 5
    DELETE_PATTERN = 4
    DISP = 3
    DOT_COUNT = 18
