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

from enum import Enum

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
