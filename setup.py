# Copyright (c) 2009-2015 CSIRO
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
import os
from setuptools import setup
from setuptools import find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name = 'mirpy',
      version = 'trunk',
      description = 'Pure-python miriad CLI wrapper.',
      author = 'Malte Marquarding',
      author_email = 'Malte.Marquarding@csiro.au',
      url = 'https://github.com/radio-astro/mirpy',
      keywords = ['miriad', 'astronomy', 'radio astronomy'],
      long_description = read("README"),
      packages = find_packages(exclude=['tests', 'examples']),
      license = 'GPL',
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],

      zip_safe = 1,
      #test_suite = "nose.collector",
)
