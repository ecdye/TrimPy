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

from TrimPy import Trim
from random import randint


def randByte():
    while True:
        b = randint(0, 255)
        if ((b != Trim.START.value) and (b != Trim.END.value)):
            break
    return b


def validatePatternOptions(options, querySrc):
    if (((options.patName is None) or (options.animation is None) or
       (options.speed is None) or (options.brightness is None) or
       (options.count_one is None) or (options.count_two is None) or
       (options.count_three is None) or (options.count_four is None) or
       (options.count_five is None) or (options.count_six is None) or
       (options.count_seven is None) or (options.color_one is None) or
       (options.color_two is None) or (options.color_three is None) or
       (options.color_four is None) or (options.color_five is None) or
       (options.color_six is None) or (options.color_seven is None)) and
       (querySrc is None)):
        print('All pattern options must be provided, or a pattern number must be provided to copy values from.')
        return False
    return True
