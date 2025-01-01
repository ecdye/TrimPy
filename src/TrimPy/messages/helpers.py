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

from TrimPy import Trim
from random import randint


def randByte():
    while True:
        b = randint(0, 255)
        if ((b != Trim.START.value) and (b != Trim.END.value)):
            break
    return b


def validatePatternOptions(options, querySrc):
    fields = [
        options.patName, options.animation, options.speed, options.brightness,
        options.count_one, options.count_two, options.count_three, options.count_four,
        options.count_five, options.count_six, options.count_seven,
        options.color_one, options.color_two, options.color_three,
        options.color_four, options.color_five, options.color_six,
        options.color_seven
    ]
    if any(f is None for f in fields) and querySrc is None:
        print('All pattern options must be provided, or a pattern number must be provided to copy values from.')
        return False
    return True
