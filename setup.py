from distutils.core import setup
from distutils.extension import Extension
#from Cython.Build import cythonize

#import numpy

#numpy_inc = numpy.get_include()

py_scripts=['scripts/cryoem-display.py']

setup(
    name = "Cryo-Electron Microscopy Image Display",
	scripts=py_scripts,
	packages=['cdisplay'],
)


#from distutils.core import setup
#from distutils.extension import Extension
#from Cython.Build import cythonize
#
#import numpy
#
#numpy_inc = numpy.get_include()
#
#extensions = [
#    Extension("cryoem.polar_image_ft", ["cryoem/polar_image_ft.pyx"],
#        include_dirs = [numpy_inc],
#		),
##    Extension("cryoem.polar_image_pcode", ["cryoem/polar_image_pcode.py"]
##		)
#	]
#
#py_scripts=[
#	'scripts/cryoem-composite-mrc-to-hdf5.py',
#	'scripts/cryoem-compute-fft2D.py',
#	'scripts/cryoem-compute-polar-ft-pwr.py',
#	'scripts/cryoem-compute-shrink2D.py',
#	'scripts/cryoem-compute-shrink2D-redescend.py',
#	'scripts/cryoem-write-image-power.py',
#	'scripts/cryoem-write-image-real.py']
#
#
#setup(
#    name = "Cryo-Electron Microscopy Utilities",
#    ext_modules = cythonize(extensions),
#	scripts=py_scripts,
#	packages=['cryoem'],
#)
#

