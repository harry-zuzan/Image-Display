from collections import namedtuple


Coordinate = namedtuple('Coordinate',['x','y'])

# not actually using this but it would be nice to have it working
# to get around using the lambda function
class Command:
	def __init__(self, func, *args, **kw):
		self.func = func
		self.args = args
		self.kw = kw

	def __call__(self, *args, **kw):
		args = self.args + args
		kw.update(self.kw)
		apply(self.func, args, kw)
