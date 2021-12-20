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

from .enum.pattern import Pattern
from .enum.trim import Trim
from .enum.mode import Mode
from .enum.animation import Animation
from .messages.message import formatConnMsg, formatModeMsg, formatDispMsg, formatNameMsg, formatQueryPatternMsg
from .messages.message import formatUpdatePatternMsg, formatDeletePatternMsg, formatDotMsg
from .messages.parser import parseOptions, parseQueryData

__all__ = ['Pattern', 'Trim', 'Mode', 'Animation', 'formatConnMsg', 'formatModeMsg', 'formatDispMsg', 'formatNameMsg',
           'formatQueryPatternMsg', 'formatUpdatePatternMsg', 'formatDeletePatternMsg', 'formatDotMsg', 'parseOptions',
           'parseQueryData', '__version__']
__version__ = '0.6.0'
