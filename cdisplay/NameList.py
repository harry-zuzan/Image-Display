
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

