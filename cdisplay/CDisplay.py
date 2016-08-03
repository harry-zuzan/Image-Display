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

		self.filler = IterButton(iter_frame,text='',
			state=DISABLED,relief=FLAT)
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

