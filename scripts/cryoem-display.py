#!/usr/bin/env python2

from __future__ import print_function

import optparse, sys, os
import subprocess

import platform

print('Python version', platform.python_version())

from Tkinter import *
from PIL import Image, ImageTk
#import ttk

from cdisplay import NameList, Coordinate
from cdisplay import IterButton, ResizingCanvas
from cdisplay import CryoDisplay


def parse_options():
	usage = "usage: %prog [options] image-files"

	parser = optparse.OptionParser(usage=usage)

	return parser



if __name__ == '__main__':

	parser = parse_options()
	options,pargs = parser.parse_args()

	if not len(pargs):
		parser.print_help()
		sys.exit()


	CryoDisplay(pargs).mainloop()

