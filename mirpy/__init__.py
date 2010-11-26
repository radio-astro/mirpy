"""
A miriad CLI wrapper module.
"""
import sys
from mirpy.wrapper import Miriad
# create default instance
miriad = Miriad()
# inject all methods into moudle as functions.
for i in miriad._common:
    setattr(sys.modules[__name__], i, getattr(miriad,i))
# expose them to 'from mirpy import *'
__all__ = ['miriad'] + miriad._common
