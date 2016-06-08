#!/usr/bin/env python2

import glob

from Tkinter import *
from PIL import Image, ImageTk
#import ttk


class NameList:
	def __init__(self,names):
		self.names = list(names)
		self.posn = 0

	def __len__(self):
		return len(self.names)

	def current(self):
		return self.names[self.posn]

	def prev(self):
		if self.posn > 0: self.posn -= 1
		return self.names[self.posn]

	def next(self):
		if self.posn < (len(self) - 1): self.posn += 1
		return self.names[self.posn]

	def at_begin(self):
		if self.posn == 0: return True
		return False

	def at_end(self):
		if self.posn == (len(self) - 1): return True
		return False

	def at_middle(self):
		return not (self.at_begin() or self.at_end())




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


	def resize_image(self,event):
		height,width = self.image.size
		height1,width1 = 2*height,2*width

		self.image = self.image.resize((width1,height1),Image.NEAREST)

		self.delete(self.image_id)

		self.imagetk = ImageTk.PhotoImage(self.image)

		self.config(width=width1, height=height1)

		self.image_id = \
			self.create_image(0,0,anchor=NW,image=self.imagetk)

		self.pack()

		print '****', self.image.size



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

		self.resize_button1 = IterButton(iter_frame, text='1X')
		self.resize_button1.pack(side=LEFT,expand=NO,fill=BOTH)
		self.resize_button1.bind('<Button-1>', self.resize1)

		self.resize_button2 = IterButton(iter_frame, text='2X')
		self.resize_button2.pack(side=LEFT,expand=NO,fill=BOTH)
		self.resize_button2.bind('<Button-1>', self.resize2)

		self.resize_button3 = IterButton(iter_frame, text='3X')
		self.resize_button3.pack(side=LEFT,expand=NO,fill=BOTH)
		self.resize_button3.bind('<Button-1>', self.resize3)

		self.quit_button = IterButton(iter_frame,text='Quit',command=self.quit)
		self.quit_button.pack(side=LEFT,expand=NO, fill=BOTH)

		self.dummy = IterButton(iter_frame,text='',state=DISABLED,relief=FLAT)
		self.dummy.pack(side=LEFT,expand=YES, fill=BOTH)


		self.canvas = self.display_first_image()


	def display_first_image(self):
		image_name = self.name_list.current()

		image = Image.open(image_name)
		canvas = ResizingCanvas(self,width=image.width,height=image.height)
#			borderwidth=1,highlightthickness=1)
		canvas.pack(side=LEFT,anchor=NW,fill=BOTH)

		canvas.image = image
		canvas.imagetk = ImageTk.PhotoImage(canvas.image)

		canvas.image_id = canvas.create_image(0,0,
							anchor=NW,image=canvas.imagetk)

		return canvas


	def display_next_image(self,event):

		img_name = self.name_list.next()

		self.canvas.image = Image.open(img_name)
		self.canvas.imagetk = ImageTk.PhotoImage(self.canvas.image)

		self.canvas.delete(self.canvas.image_id)
		self.canvas.image_id = \
			self.canvas.create_image(0,0,anchor=NW,image=self.canvas.imagetk)


	def display_prev_image(self,event):

		img_name = self.name_list.prev()

		self.canvas.image = Image.open(img_name)
		self.canvas.imagetk = ImageTk.PhotoImage(self.canvas.image)

		self.canvas.image_id = \
			self.canvas.create_image(0,0,anchor=NW,image=self.canvas.imagetk)


	def resize1(self,event): self.resize(1)
	def resize2(self,event): self.resize(2)
	def resize3(self,event): self.resize(3)

	def resize(self,size_mult):
		print 'resize value =', size_mult
#		self.canvas.resize(size_mult)

	
	def calc(self, display):
		try: display.set(`eval(display.get())`)
		except ValueError: display.set("ERROR")


if __name__ == '__main__':
	import glob

	images = glob.glob('images/*png')
	CryoDisplay(images).mainloop()

