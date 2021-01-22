import sys
import os
__working_dir = str(os.getcwd()).split(os.sep)
if 'PYCM' in __working_dir:
	if 'Client' in os.path.split(os.getcwd()):
		os.chdir('..')
	sys.path.append('.')