#!/usr/bin/env python2

from __future__ import print_function
import platform
print('Python version', platform.python_version())

import optparse, sys, os
import subprocess

import Tkinter

# having problems creating a zoom that fits in the menu bars of the
# window manager` - long story
# this is what "works for me"(TM)

# 1) open a canvas
C = Tkinter.Canvas()

# 2) get the dimensions of the display
screen_w = C.master.winfo_screenwidth()
screen_h = C.master.winfo_screenheight()

# 3) set the geometry to the full screen
geom_str = "{0}x{1}+0+0".format(screen_w,screen_h)
C.master.wm_geometry(geom_str)
C.update_idletasks()

# 4) get the unobstructed geometry available to the canvas, that is,
#    after the canvas title bar and window manager menu bar are in place
zoom_w = C.master.winfo_width()
zoom_h = C.master.winfo_height()

# A better way would be nice
C.master.destroy()


from Tkinter import *
from PIL import Image, ImageTk
#import ttk

#from cdisplay import NameList, Coordinate
#from cdisplay import IterButton, ResizingCanvas
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


#-------------------------------------------------------------

#	tk = Tkinter.Tk()

#	SortDisplay(tk,pargs,zoom_w,zoom_h,keep_dir,delete_dir).mainloop()

