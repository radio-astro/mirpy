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
__all__ = ["mir_commands"]
import os

def mir_commands():
    """Get a filter list of miriad commands in the miriad bin directory"""
    mir = which('miriad')
    if mir is None:
        raise OSError('miriad is not available. Check your PATH.')
    mirpath = os.path.split(mir)[0]
    return [ cmd for cmd in os.listdir(mirpath) \
                 if not (cmd.startswith('mir') or cmd.startswith('doc')
                     or cmd.startswith('pg') or cmd.endswith('.exe')) ]



def which(program='miriad'):
    """Equivalent of unix 'which' command"""
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)
    if program:
        fpath, fname = os.path.split(program)
    else:
        return None
    if fpath and is_exe(program):
        return program
    else:
        if "PATH" in os.environ:
           for path in os.environ["PATH"].split(os.pathsep):
               path = os.path.expandvars(os.path.expanduser(path))
               exe_file = os.path.join(path, program)
               if is_exe(exe_file):
                   return exe_file
    return None
