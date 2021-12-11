from sys import exit
import lxml.etree
import numpy as np

class data:

	def __init__(self,path):
		with open(path) as f:
			lines = f.readlines()
		lines = '\n'.join(lines)
		root = lxml.etree.fromstring(lines)

		self._width = int(root.xpath('//app/width/text()')[0])+1
		self._num_of_circuits = int(root.xpath('//app/numcircuits/text()')[0])
		self._size = []
		for i in range(1,self._num_of_circuits+1):
			tmp = np.array(root.xpath('//app/size/row'+str(i)+'/cell/text()'), dtype='int').tolist()
			self._size.append(tmp)

	def get_width(self):
		return self._width

	def get_num_of_circuits(self):
		return self._num_of_circuits

	def get_size(self):
		return self._size
