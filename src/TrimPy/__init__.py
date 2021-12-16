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

from .enum.pattern import Pattern
from .enum.trim import Trim
from .enum.mode import Mode
from .enum.animation import Animation
from .message import *

__version__ = '0.2.0'