# ricodebug - A GDB frontend which focuses on visually supported
# debugging using data structure graphs and SystemC features.
#
# Copyright (C) 2011  The ricodebug project team at the
# Upper Austrian University Of Applied Sciences Hagenberg,
# Department Embedded Systems Design
#
# This file is part of ricodebug.
#
# ricodebug is free software: you can redistribute it and/or modify
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further information see <http://syscdbg.hagenberg.servus.at/>.

from functools import wraps
import inspect

__CLASSNAME__ = None
__CALLBACK__ = None

def setClassName(c):
    global __CLASSNAME__
    __CLASSNAME__ = c

def setCallback(c):
    global __CALLBACK__
    __CALLBACK__ = c

def _quote(x):
    if isinstance(x, str):
        return '"%s"' % x
    else:
        return x


def trace(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        fa = inspect.getcallargs(fn, *args, **kwargs)
        arglist = ("%s=%s" % (k, _quote(v)) for k, v in fa.items() if k != "self")
        __CALLBACK__("%s.%s(%s)" % (__CLASSNAME__, fn.__name__, ", ".join(arglist)))

        return fn(*args, **kwargs)
    return wrapper
