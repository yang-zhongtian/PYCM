import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class ScreenDiff(object):
	image_buffer = None
	image_shape = None
	scan_step = None
	def __init__(self, step=5):
		self.scan_step = step
	def __compare(self, current):
		if self.image_shape != current.shape:
			return None
		result = []
		current_line = 1
		first_equal = True
		pos_start_line = pos_start_column = pos_end_line = pos_end_column = 0
		while current_line <= current.shape[0]:
			diff_found = False
			for current_column in range(current.shape[1]):
				if np.any(self.image_buffer[current_line][current_column] != current[current_line][current_column]):
					diff_found = True
					if first_equal:		
						pos_start_line = pos_end_line = current_line
						pos_start_column = pos_end_column = current_column
						first_equal = False
					else:
						pos_start_column = min(pos_start_column, current_column)
						pos_end_line = max(pos_end_line, current_line)
						pos_end_column = max(pos_end_column, current_column)
			if not (diff_found or first_equal):
				pos_start_line = max(0, pos_start_line - self.scan_step)
				pos_start_column = max(0, pos_start_column - self.scan_step)
				pos_end_line = min(current.shape[0], pos_end_line + self.scan_step)
				pos_end_column = min(current.shape[1], pos_end_column + self.scan_step)
				result.append(np.array([np.array([pos_start_line, pos_start_column]), np.array([pos_end_line, pos_end_column])]))
				pos_start_line = pos_start_column = pos_end_line = pos_end_column = 0
				first_equal = True
			current_line += self.scan_step
		return result
	def __update(self, current):
		self.image_buffer = current
		self.image_shape = current.shape
	def diff(self, current):
		current_array = np.array(current)
		result = []
		if self.image_buffer is None:
			self.__update(current_array)
			result.append((np.array([np.array([0,0]),np.array([current_array.shape[0],current_array.shape[1]])]), current_array))
			return result
		else:
			compare_result = self.__compare(current_array)
			for pair in compare_result:
				result.append((pair, current_array[pair[0][0]:pair[1][0], pair[0][1]:pair[1][1]]))
			self.__update(current_array)
			return result

def DEBUG(result):
	print('\n## DEBUG ##')
	for i, obj in enumerate(result):
		print()
		area = list(map(list, obj[0]))
		image = obj[1]
		print(f'* RESULT ID: {i}')
		print(f'* AREA INFO {area}')
		plt.imshow(image)
		plt.show()
	print('\n###########')

if __name__ == '__main__':
	A = ScreenDiff()
	DEBUG(A.diff(Image.open('1.bmp')))
	# plt.show()
	DEBUG(A.diff(Image.open('2.bmp')))
	# plt.show()
