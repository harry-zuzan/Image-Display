#!/usr/bin/env python2

from __future__ import print_function

import optparse, sys, os
import subprocess

import platform

print('Python version', platform.python_version())


import glob

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



#class CryoDisplay(Frame):
#	def __init__(self,img_names):
#		Frame.__init__(self)
#		self.pack(expand=YES, fill=BOTH)
#		self.master.title('CryoEM Image Display')
#		self.master.iconname('CDISP')

#		self.name_list = NameList(img_names)

#		iter_frame = Frame(self)
#		iter_frame.pack(side=TOP, expand=NO, fill=BOTH)

#		self.prev_button = IterButton(iter_frame, text='<')
#		self.prev_button.pack(side=LEFT,expand=NO,fill=BOTH)
#		self.prev_button.bind('<Button-1>', self.display_prev_image)

#		self.next_button = IterButton(iter_frame, text='>')
#		self.next_button.pack(side=LEFT,expand=NO,fill=BOTH)
#		self.next_button.bind('<Button-1>', self.display_next_image)

#		self.resize_buttonmx = IterButton(iter_frame, text='-')
#		self.resize_buttonmx.pack(side=LEFT,expand=NO,fill=BOTH)

#		self.resize_buttonpx = IterButton(iter_frame, text='+')
#		self.resize_buttonpx.pack(side=LEFT,expand=NO,fill=BOTH)

#		self.quit_button = IterButton(iter_frame,text='Quit',command=self.quit)
#		self.quit_button.pack(side=LEFT,expand=NO, fill=BOTH)

#		self.filler = IterButton(iter_frame,text='',state=DISABLED,relief=FLAT)
#		self.filler.pack(side=LEFT,expand=YES, fill=BOTH)

#		self.canvas = self.create_canvas()

#		self.resize_buttonmx.bind('<Button-1>',
#				func=lambda x: self.canvas.resize_image(-1))
#		self.resize_buttonpx.bind('<Button-1>',
#				func=lambda x: self.canvas.resize_image(1))

#		self.display_current_image()


#	def create_canvas(self):
#		canvas = ResizingCanvas(self,width=128,height=128)
#		canvas.pack(side=LEFT,anchor=NW,fill=BOTH)

#		canvas.image_id = None
#		canvas.scale = 1

#		return canvas


#	def display_current_image(self):
#		image_name = self.name_list.current()
#		image = Image.open(image_name)
#		self.canvas.display_image(image)

#	def display_next_image(self,event):
#		img_name = self.name_list.next()
#		image = Image.open(img_name)

#		self.canvas.display_image(image)

#		return

#	def display_prev_image(self,event):
#
#		img_name = self.name_list.prev()
#		image = Image.open(img_name)

#		self.canvas.display_image(image)



if __name__ == '__main__':

	parser = parse_options()
	options,pargs = parser.parse_args()

	if not len(pargs):
		parser.print_help()
		sys.exit()


	CryoDisplay(pargs).mainloop()

