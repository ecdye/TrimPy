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
