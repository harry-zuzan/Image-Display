from Tkinter import Button, Canvas, Frame
from Tkinter import NW, TOP, LEFT, YES, NO, BOTH
from Tkinter import DISABLED, FLAT
from PIL import Image, ImageTk

from DispUtils import Coordinate, NameList

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
		self.pack()
		self.focus_set()
		self.parent = parent
#		self.height = self.winfo_reqheight()
#		self.width = self.winfo_reqwidth()

		self.bind('<Left>', self.parent.display_prev_image)
		self.bind('<Right>', self.parent.display_next_image)
		self.bind('<Up>', self.parent.display_first_image)
		self.bind('<Down>', self.parent.display_last_image)
		self.bind('q', self.parent.exit_mainloop)

		self.bind('<Button-1>',self.scroll_start)
		self.bind('<B1-Motion>',self.scroll_move)

		# shift image by 1 pixel
		self.bind('<Shift-Up>',
			func=lambda crd: self.scroll_from_keyboard(Coordinate( 0,-1)))
		self.bind('<Shift-Down>',
			func=lambda crd: self.scroll_from_keyboard(Coordinate( 0, 1)))
		self.bind('<Shift-Left>',
			func=lambda crd: self.scroll_from_keyboard(Coordinate(-1, 0)))
		self.bind('<Shift-Right>',
			func=lambda crd: self.scroll_from_keyboard(Coordinate( 1, 0)))

		# shift image by 8 pixels
		self.bind('<Control-Up>',
			func=lambda crd: self.scroll_from_keyboard(Coordinate( 0,-8)))
		self.bind('<Control-Down>',
			func=lambda crd: self.scroll_from_keyboard(Coordinate( 0, 8)))
		self.bind('<Control-Left>',
			func=lambda crd: self.scroll_from_keyboard(Coordinate(-8, 0)))
		self.bind('<Control-Right>',
			func=lambda crd: self.scroll_from_keyboard(Coordinate( 8, 0)))

	# the next two work together to slide the image around the canvas
	# using the mouse or track pad
	def scroll_start(self, event):
		self.scan_mark(event.x, event.y)

	def scroll_move(self, event):
		self.scan_dragto(event.x, event.y, gain=1)

	# and this scrolls the image by a displacment of pixels using the
	# arrow keys or whatever key is mapped to the method 
	def scroll_from_keyboard(self,displace):
		self.scan_mark(0,0)
		self.scan_dragto(displace.x,displace.y,1)


	def resize_image(self,rescale):
		if self.scale == 1 and rescale < 0: return
		self.scale = self.scale + rescale
		width,height = self.image_store.size
		width,height = width*self.scale,height*self.scale
		image = self.image_store.resize((width,height),Image.NEAREST)
#		image = self.image_store.resize((height,width),Image.NEAREST)
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
		width,height = self.image_store.size
		if self.scale != 1:
			width,height = self.scale*width,self.scale*height
			image = image.resize((width,height),Image.NEAREST)

		self.config(width=width, height=height)

		self.image_display = image
		self.imagetk = ImageTk.PhotoImage(image)

		if self.image_id: self.delete(self.image_id)

		self.image_id = \
			self.create_image(0,0,anchor=NW,image=self.imagetk)
		self.image_id = \
			self.create_image(0,0,anchor=NW,image=self.imagetk)

		self.parent.master.update_idletasks()
		print(self.parent.master.winfo_geometry())
		print(self.parent.master.geometry())
		print(self.parent.master.wm_geometry())


	def report_position(self,event):
		self.scan_mark(0,0)
		self.scan_dragto(1,1,1)



class CryoDisplay(Frame):
	def __init__(self,img_names):
		Frame.__init__(self)
		self.pack(expand=YES, fill=BOTH)
		self.master.title('CryoEM Image Display')
		self.master.iconname('CDISP')
		self.focus_set()

		self.name_list = NameList(img_names)

		iter_frame = Frame(self)
		iter_frame.pack(side=TOP, expand=NO, fill=BOTH)
		iter_frame.focus_set()

		self.prev_button = IterButton(iter_frame, text='<')
		self.prev_button.pack(side=LEFT,expand=NO,fill=BOTH)
		self.prev_button.bind('<Button-1>', self.display_prev_image)


		self.next_button = IterButton(iter_frame, text='>')
		self.next_button.pack(side=LEFT,expand=NO,fill=BOTH)
		self.next_button.bind('<Button-1>', self.display_next_image)

		self.resize_buttonmx = IterButton(iter_frame, text='-')
		self.resize_buttonmx.pack(side=LEFT,expand=NO,fill=BOTH)

		self.resize_buttonpx = IterButton(iter_frame, text='+')
		self.resize_buttonpx.pack(side=LEFT,expand=NO,fill=BOTH)

		self.quit_button = IterButton(iter_frame,text='Quit',command=self.quit)
		self.quit_button.pack(side=LEFT,expand=NO, fill=BOTH)

		self.filler = IterButton(iter_frame,relief=FLAT,overrelief=FLAT)
		filler_background = self.filler.cget("background")
		self.filler.configure(activebackground=filler_background)

#  uncomment to look at the keys available in a button
#		for key in self.filler.keys(): print key, '=', self.filler.cget(key)

		self.filler.pack(side=LEFT,expand=YES, fill=BOTH)

		self.canvas = self.create_canvas()

		self.display_current_image()

		self.resize_buttonmx.bind('<Button-1>',
				func=lambda x: self.canvas.resize_image(-1))
		self.resize_buttonpx.bind('<Button-1>',
				func=lambda x: self.canvas.resize_image(1))

		self.canvas.bind('+', func=lambda x: self.canvas.resize_image(1))
		self.canvas.bind('-', func=lambda x: self.canvas.resize_image(-1))



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
		filler_fmt = "{0}/{1} - {2}"
		filler_string = filler_fmt.format(
			self.name_list.position() + 1,
			self.name_list.size(),
			image_name.split('/')[-1])

		self.filler['text'] = filler_string

	def display_prev_image(self,event):
		self.name_list.prev()
		self.display_current_image()


	def display_next_image(self,event):
		self.name_list.next()
		self.display_current_image()


	def display_first_image(self,event):
		img_name = self.name_list.first()
		image = Image.open(img_name)

		self.canvas.display_image(image)

		return

	def display_last_image(self,event):
		img_name = self.name_list.last()
		image = Image.open(img_name)

		self.canvas.display_image(image)

		return

	def exit_mainloop(self,event):
		self.quit()

#from Tkinter import Canvas
#from Tkinter import NW, YES, BOTH
#
#from PIL import Image, ImageTk
#
#from DispUtils import NameList
#
#
#import os,subprocess
#
#class SortDisplay(Canvas):
#	def __init__(self, master,img_names,zoom_width,zoom_height,
#			keep_dir,delete_dir):
#
#		Canvas.__init__(self,master)
#		self.pack(expand=YES, fill=BOTH)
#		self.master.title('Image Sort')
#		self.master.iconname('S-DISP')
#		self.focus_set()
#		self.master.config(highlightthickness=0)
#		self.configure(highlightthickness=0)
#
#		self.name_list = NameList(img_names)
#		self.zoom_width = zoom_width
#		self.zoom_height = zoom_height
#		self.keep_dir = keep_dir
#		if not self.keep_dir[-1] == '/': self.keep_dir += '/'
#		self.delete_dir = delete_dir
#		if not self.delete_dir[-1] == '/': self.delete_dir += '/'
#
#		self.image_id = None
#		self.is_fullscreen=False
#		self.is_zoomed=False
#
#		self.scroll_start_x=0
#		self.scroll_start_y=0
#		self.off_centre_x=0
#		self.off_centre_y=0
#
#
#		self.bind('<Left>', self.display_prev_image)
#		self.bind('<Right>', self.display_next_image)
#		self.bind('<Up>', self.display_first_image)
#		self.bind('<Down>', self.display_last_image)
#		self.bind('<space>', self.display_next_image)
#
#		self.bind('<Button-1>',self.scroll_start)
#		self.bind('<ButtonRelease-1>',self.scroll_stop)
#		self.bind('<B1-Motion>',self.scroll_move)
#
#		self.bind('f', self.fullscreen)
#		self.bind('z', self.zoom)
#		self.bind('c', self.recentre)
#
#		self.bind('k', self.move_to_keep)
#		self.bind('d', self.move_to_delete)
#
#		self.bind('q', self.exit_mainloop)
#
#		self.display_current_image()
#
#
#	# the next two work together to slide the image around the canvas
#	# using the mouse or track pad
#
#	def scroll_start(self, event):
#		self.scan_mark(event.x, event.y)
#		self.scroll_start_x = event.x
#		self.scroll_start_y = event.y
#
#	def scroll_stop(self, event):
#		self.off_centre_x += event.x - self.scroll_start_x
#		self.off_centre_y += event.y - self.scroll_start_y
#
#	def scroll_move(self, event):
#		self.scan_dragto(event.x, event.y, gain=1)
#
#	def recentre(self,event):
#		self.scan_mark(0, 0)
#		self.scan_dragto(-self.off_centre_x,-self.off_centre_y,gain=1)
#		self.off_centre_x = 0
#		self.off_centre_y = 0
#
#	def display_current_image(self):
#		image_name = self.name_list.current()
#		image = Image.open(image_name)
#		title_fmt = "ISD {0}/{1} - {2}"
#		title_string = title_fmt.format(
#			self.name_list.position() + 1,
#			self.name_list.size(),
#			image_name.split('/')[-1])
#
#		self.master.title(title_string)
#
#		if self.is_fullscreen:
#			self.display_image_fullscreen(image)
#			return
#
#		if self.is_zoomed:
#			self.display_image_zoomed(image)
#			return
#
#		self.display_image_small(image)
#
#
#	def display_prev_image(self,event=None):
#		self.name_list.prev()
#		self.display_current_image()
#
#	def display_next_image(self,event):
#		self.name_list.next()
#		self.display_current_image()
#
#	def display_first_image(self,event):
#		self.name_list.first()
#		self.display_current_image()
#
#	def display_last_image(self,event):
#		self.name_list.last()
#		self.display_current_image()
#
#	def redisplay_image(self):
#		self.name_list.current()
#		self.display_current_image()
#
#	def display_image_small(self,image):
#		width,height = image.size
#		width = min(width,self.master.winfo_screenwidth() - 4)
#		height = min(height,self.master.winfo_screenheight() - 4)
#
#		geom = "{0}x{1}+0+0".format(width,height)
##		geom = "{0}x{1}".format(width,height)
#		self.master.geometry(geom)
#		self.master.update_idletasks()
#
#		imgtk = ImageTk.PhotoImage(image)
#		self.imagetk = imgtk
#
#		old_image_id = self.image_id
#
#		self.image_id = \
#			self.create_image(0,0,anchor=NW,image=self.imagetk)
#
#		if self.image_id: self.delete(old_image_id)
#
#
#
#	def display_image_fullscreen(self,image):
#		width,height = image.size
#
#		width,height,dw,dh = self.fit_to_fullscreen(width,height)
#		image = image.resize((width,height),Image.LANCZOS)
#
#		self.master.update_idletasks()
#
#		imgtk = ImageTk.PhotoImage(image)
#		self.imagetk = imgtk
#
#		old_image_id = self.image_id
#
#		self.image_id = \
#			self.create_image(dw,dh,anchor=NW,image=self.imagetk)
#
#		if self.image_id: self.delete(old_image_id)
#
#
#	def display_image_zoomed(self,image):
#		width,height = image.size
#
#		width,height,dx,dy = self.fit_to_zoom(*image.size)
#		image = image.resize((width,height),Image.LANCZOS)
#		geom = "{0}x{1}+{2}+{3}".format(width,height,dx,dy)
#		self.master.geometry(geom)
#		self.master.update_idletasks()
#
#		imgtk = ImageTk.PhotoImage(image)
#		self.imagetk = imgtk
#
#		old_image_id = self.image_id
#
#		self.image_id = \
#			self.create_image(0,0,anchor=NW,image=self.imagetk)
#
#		if self.image_id: self.delete(old_image_id)
#
#
#	def zoom(self,event=None):
#		self.is_zoomed = not self.is_zoomed
#		if self.is_fullscreen:
#			self.is_fullscreen = False
#			self.master.attributes('-fullscreen', False)
#
#
#		self.display_current_image()
#
#
#	def fullscreen(self,event=None):
#		self.is_fullscreen = not self.is_fullscreen
#		self.master.attributes('-fullscreen', self.is_fullscreen)
#		self.display_current_image()
#
#
#	def fit_to_zoom(self,width,height):
#		scale_w = float(self.zoom_width)/float(width)
#		scale_h = float(self.zoom_height)/float(height)
#		scale = min(scale_w,scale_h)
#
#		width,height = int(scale*width), int(scale*height)
#		shift_w = (self.zoom_width - width)/2
#		shift_h = (self.zoom_height - height)/2
#
#		return (width,height,shift_w,shift_h)
#
#
#	def fit_to_fullscreen(self,width,height):
#		screen_w = self.master.winfo_screenwidth()
#		screen_h = self.master.winfo_screenheight()
#
#		scale_w = float(screen_w)/float(width)
#		scale_h = float(screen_h)/float(height)
#		scale = min(scale_w,scale_h)
#
#		width,height = int(scale*width), int(scale*height)
#		shift_w = (screen_w - width)/2
#		shift_h = (screen_h - height)/2
#
#		return (width,height,shift_w,shift_h)
#
#	def check_that_dir_exists(self,dir_name):
#		if os.path.exists(dir_name): return
#
#		status = subprocess.call(['mkdir',dir_name])
#		if not status: return
#
#		print('error creating directory', dir_name)
#		self.exit_mainloop()
#
#
#	def move_to_keep(self, event):
#		img_name_from = self.name_list.current()
#		full_img_name = self.get_destination_name(img_name_from, self.keep_dir)
#
#		if not full_img_name:
#			self.exit_mainloop()
#			return
#
#		call_list = ['mv', img_name_from, full_img_name]
#		subprocess.call(call_list)
#		self.name_list.remove_current()
#		if not len(self.name_list):
#			self.exit_mainloop()
#			return
#		self.display_current_image()
#
#
#	def move_to_delete(self, event):
#		img_name_from = self.name_list.current()
#		full_img_name = self.get_destination_name(img_name_from,self.delete_dir)
#
#		if not full_img_name:
#			self.exit_mainloop()
#			return
#
#		call_list = ['mv', img_name_from, full_img_name]
#		subprocess.call(call_list)
#		self.name_list.remove_current()
#		if not len(self.name_list):
#			self.exit_mainloop()
#			return
#		self.display_current_image()
#
#
#	def get_destination_name(self, img_name, destination_dir,max_attempts=10):
#		self.check_that_dir_exists(destination_dir)
#
#		attempts = 0
#		while 1:
#			attempts += 1
#			if attempts > max_attempts:
#				return None
#
#			full_img_name = destination_dir + img_name
#			if not os.path.exists(full_img_name):
#				return full_img_name
#
#			img_name_pieces = img_name.split('.')
#			img_name_pieces[-2] += '0'
#			img_name = '.'.join(img_name_pieces)
#
#	def exit_mainloop(self,event=None):
#		self.quit()
#
#
