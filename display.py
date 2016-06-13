#!/usr/bin/env python2

import glob

from Tkinter import *
from PIL import Image, ImageTk
#import ttk

from NameList import NameList
from DispUtils import Command


class IterButton(Button):
	def __init__(self,root,**kwargs):
		Button.__init__(self,root,**kwargs)

		self.store_initial_state()

	def store_initial_state(self):
		self.initial_state = dict()
		for key in self.keys(): self.initial_state[key] = self.cget(key)

	def restore_initial_state(self):
		for key,value in self.initial_state: self.configure(key=value)


class ResizingCanvas(Canvas):
	def __init__(self,parent,**kwargs):
		Canvas.__init__(self,parent,**kwargs)
#		self.height = self.winfo_reqheight()
#		self.width = self.winfo_reqwidth()

#		self.bind('<Button-1>',self.report_position)
		self.bind('<B1-Motion>',self.report_position)


	def resize_image(self,scale):
		if self.scale == scale: return
		self.scale = scale
		height,width = self.image_store.size
		height,width = height*scale,width*scale
		image = self.image_store.resize((width,height),Image.NEAREST)
		self.imagetk = ImageTk.PhotoImage(image)
		self.image_display = image

		self.delete(self.image_id)

		self.config(width=width, height=height)

		self.delete(self.image_id)
		self.image_id = \
			self.create_image(0,0,anchor=NW,image=self.imagetk)

		self.pack()



	def display_image(self,image):
		self.image_store = image
		height,width = image.size
		if self.scale != 1:
			height,width = self.scale*height,self.scale*width
			image = image.resize((width,height),Image.NEAREST)

		self.config(width=width, height=height)

		self.image_display = image
		self.imagetk = ImageTk.PhotoImage(image)

		if self.image_id: self.delete(self.image_id)

		self.image_id = \
			self.create_image(0,0,anchor=NW,image=self.imagetk)


	def report_position(self,event):
		print 'yeah got an event'




class CryoDisplay(Frame):
	def __init__(self,img_names):
		Frame.__init__(self)
		self.pack(expand=YES, fill=BOTH)
		self.master.title('CryoEM Image Display')
		self.master.iconname('CDISP')

		self.name_list = NameList(img_names)

		iter_frame = Frame(self)
		iter_frame.pack(side=TOP, expand=NO, fill=BOTH)

		self.prev_button = IterButton(iter_frame, text='<')
		self.prev_button.pack(side=LEFT,expand=NO,fill=BOTH)
		self.prev_button.bind('<Button-1>', self.display_prev_image)

		self.next_button = IterButton(iter_frame, text='>')
		self.next_button.pack(side=LEFT,expand=NO,fill=BOTH)
		self.next_button.bind('<Button-1>', self.display_next_image)

		self.resize_button1x = IterButton(iter_frame, text='1X')
		self.resize_button1x.pack(side=LEFT,expand=NO,fill=BOTH)

		self.resize_button2x = IterButton(iter_frame, text='2X')
		self.resize_button2x.pack(side=LEFT,expand=NO,fill=BOTH)

		self.resize_button3x = IterButton(iter_frame, text='3X')
		self.resize_button3x.pack(side=LEFT,expand=NO,fill=BOTH)

		self.quit_button = IterButton(iter_frame,text='Quit',command=self.quit)
		self.quit_button.pack(side=LEFT,expand=NO, fill=BOTH)

		self.filler = IterButton(iter_frame,text='',state=DISABLED,relief=FLAT)
		self.filler.pack(side=LEFT,expand=YES, fill=BOTH)

		self.canvas = self.create_canvas()

		self.resize_button1x.bind('<Button-1>',
				func=lambda x: self.canvas.resize_image(1))
		self.resize_button2x.bind('<Button-1>',
				func=lambda x: self.canvas.resize_image(2))
		self.resize_button3x.bind('<Button-1>',
				func=lambda x: self.canvas.resize_image(3))

		self.display_current_image()


	def create_canvas(self):
		canvas = ResizingCanvas(self,width=128,height=128)
		canvas.pack(side=LEFT,anchor=NW,fill=BOTH)

		canvas.image_id = None
		canvas.scale = 1

		return canvas



	def display_current_image(self):
		image_name = self.name_list.current()
		image = Image.open(image_name)
		self.canvas.display_image(image)




	def display_next_image(self,event):

		img_name = self.name_list.next()
		image = Image.open(img_name)

		self.canvas.display_image(image)

		return


	def display_prev_image(self,event):

		img_name = self.name_list.prev()
		image = Image.open(img_name)

		self.canvas.display_image(image)



if __name__ == '__main__':
	import glob

	images = glob.glob('images/*png')
	CryoDisplay(images).mainloop()

