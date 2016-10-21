from collections import namedtuple

Coordinate = namedtuple('Coordinate',['x','y'])


class NameList:
	def __init__(self,names):
		self.names = list(names)
		self.posn = 0

	def __len__(self):
		return len(self.names)

	def position(self):
		return self.posn

	def size(self):
		return len(self.names)

	def current(self):
		return self.names[self.posn]

	def prev(self):
		if self.posn > 0: self.posn -= 1
		return self.names[self.posn]

	def next(self):
		if self.posn < (len(self) - 1): self.posn += 1
		return self.names[self.posn]

	def first(self):
		self.posn = 0
		return self.names[self.posn]

	def last(self):
		self.posn = len(self) - 1
		return self.names[self.posn]

# need to figure out whether or not to throw an exception if the
# NameList/queue is empty.  For now they are not needed so leave them
#	def at_middle(self):
#		return not (self.at_begin() or self.at_end())
#
#	def at_begin(self):
#		if not len(self): return True
#		if self.posn == 0: return True
#		return False

#	def at_end(self):
#		if not len(self): return True
#		if self.posn == (len(self) - 1): return True
#		return False

	def remove_current(self,event):
		if not len(self): return
		self.names.pop(self.posn)
		if not len(self): return
		if self.posn == len(self): self.posn -= 1
