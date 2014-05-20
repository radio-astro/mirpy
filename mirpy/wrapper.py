# Copyright (c) 2009-2014 CSIRO
# Australia Telescope National Facility (ATNF)
# Commonwealth Scientific and Industrial Research Organisation (CSIRO)
# PO Box 76, Epping NSW 1710, Australia
# atnf-enquiries@csiro.au
#
# This file is part of the ASKAP software distribution.
#
# The ASKAP software distribution is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the License
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA.
#
from __future__ import print_function
__all__ = ["MiriadError", "Miriad"]

import re
import subprocess
import warnings
from mirpy.commands import mir_commands

class MiriadError(Exception):
    """An exception class for errors in miriad calls"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

def match_in(key):
    """Is the key  the 'in' keyword"""
    rx = re.compile("^_?([iI][nN])_?$")
    match = rx.match(key)
    if match:
        return True
    return False

def to_args(kw):
    """Turn a key dictionary into a list of k=v command-line arguments."""
    out = []
    for k,v in kw.items():
        if match_in(k):
            k = "in"
        if isinstance(v, list) or isinstance(v, tuple):
            v = ",".join([str(i) for i in v])
        out.append("%s=%s" % (k,v))
    return out

def mir_func(f, thefilter):
    """Wrapper around miriad system calls"""
    def func(*args, **kw):
        if len(args) == 1:
            kw["_in"] = args[0]
        args = to_args(kw)
        proc = subprocess.Popen([f]+args, shell=False, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        lines = stderr.split('\n')
        warns = []
        errors = []
        for l in lines:
            wpfx = "### Warning: "
            epfx = "### Fatal Error: "
            if l.startswith(wpfx):
                warns.append(l[len(wpfx):])
            elif l.startswith(epfx):
                errors.append(l[len(epfx)+1:])
            else:
                errors.append(l)
        if warns:
            msg = "'%s': " % f
            msg += "\n".join(warns)
            warnings.warn(msg)

        if proc.returncode != 0:
            raise MiriadError("\n".join(errors))
        out = stdout.strip()
        if thefilter is not None:
            return thefilter(out)
        return out
    return func

class Miriad(object):
    """A wrapper for miriad commands.
    Miriad commands are truned into python functions, e.g.
    
        fits in=example.uv out=example.fits op=uvout

    would be
    
        miriad.fits(_in="example.uv", out="blah.fits", op="uvout")


    NOTE!!! All miriad keys are turned into the same key name in python
    EXECEPT 'in' which is can't be used in python. The python function accepts
    any of 'In', 'IN', '_in', or 'in_' instead.

    """
    def __init__(self):
        self._common = mir_commands()
        self._filters = {}

    def __dir__(self):
        return self._common + ['set_filter']

    def set_filter(self, funcname, ffunc):
        """Set a filter function to filter stdout for a miriad command.
        Example:
        
             def uselessfilter(output):
                 return output.split('\\n')
             miriad.set_filter('uvindex', uselessfilter)
             
        Executing miriad.uvindex will nor return a list of strings (the lines
        in the stdout output.
        This can of course be used for useful filtering.
        """
        assert funcname in self._common
        self._filters[funcname] = ffunc
        
    def __getattr__(self, k):
        if k in self._common:
            thefilter = self._filters.get(k, None)
            fn = mir_func(k, thefilter)
            fn.__doc__ = self._help(k)
            fn.__name__ = k
            return fn 
        else:
            return object.__getattribute__(self, k)

    def _help(self, taskname):
        p = subprocess.Popen('miriad', shell=True, stdin=subprocess.PIPE, 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.stdin.write("{} {}\n{}\n".format("help", taskname, "exit")
                      .encode('utf-8'))
        stdout = p.communicate()[0]
        return str(stdout)

    
