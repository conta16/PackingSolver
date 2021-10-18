class utility:

	def __init__(self):
		self._max = 0
		self._sum = 0

	def compute_max_height(self,size):
		self._max = 0 #avoid wrong computation if function call is mistankenly repeated
		for i in range(len(size)):
			if (size[i][1] > self._max):
				self._max = size[i][1]
		return self._max

	def compute_sum_height(self,size):
		self._sum = 0 #avoid wrong computation if function call is mistakenly repeated
		for i in range(len(size)):
			self._sum += size[i][1]
		return self._sum

	def get_max_height(self):
		return self._max

	def get_sum_height(self):
		return self._sum

	def height_needed(self,ph,pos):
		if pos == self._sum-self._max:
			return pos
		elif ph[pos] != ph[pos+1]:
			return pos
		else:
			 return height_needed(ph,pos+1)
