from z3 import *
from data import data
from utility import utility

class solver:

	def __init__(self,path):
		self._d = data(path)
		self._u = utility()
		self._s = Optimize()
		tmp_ncirc = self._d.get_num_of_circuits()
		tmp_width = self._d.get_width()

		max_height = self._u.compute_max_height(self._d.get_size())
		sum_height = self._u.compute_sum_height(self._d.get_size())

		self._lr = [ [ Bool("lr_%s_%s" % (i+1, j+1)) for j in range(tmp_ncirc) ] for i in range(tmp_ncirc) ]
		self._ud = [ [ Bool("ud_%s_%s" % (i+1, j+1)) for j in range(tmp_ncirc) ] for i in range(tmp_ncirc) ]
		self._px = [ [ Bool("px_%s_%s" % (i+1, j+1)) for j in range(tmp_ncirc) ] for i in range(tmp_width+1) ]
		self._py = [ [ Bool("py_%s_%s" % (i+1, j+1)) for j in range(tmp_ncirc) ] for i in range(sum_height+1) ]
		self._ph = [ Bool("ph_%s" % (i+1)) for i in range(max_height,sum_height+1) ]

		self._final_height = 0

	def debug(self):
		print(self._d.get_width())
		print(self._d.get_num_of_circuits())
		print(self._d.get_size())

	def constraints(self):
		tmp_ncirc = self._d.get_num_of_circuits()
		tmp_width = self._d.get_width()
		tmp_size = self._d.get_size()

		max_height = self._u.get_max_height()
		sum_height = self._u.get_sum_height()

		#order encoding

		for i in range(tmp_ncirc):
			self._s.add_soft(And(Not(self._px[i][0]), Not(self._py[i][0])))

		for i in range(tmp_ncirc):
			for e in range(tmp_width-tmp_size[i][0]):
				self._s.add_soft(Or(Not(self._px[i][e]),self._px[i][e+1]))

		for i in range(tmp_ncirc):
			for e in range(tmp_width-tmp_size[i][0], width+1):
				self._s.add_soft(self._px[i][e])

		for i in range(tmp_ncirc):
			for f in range(sum_height-tmp_size[i][1]):
				self._s.add_soft(Or(Not(self._py[i][f]),self._py[i][f+1]))

		for i in range(tmp_ncirc):
			for f in range(sum_height-tmp_size[i][1], sum_height+1):
				self._s.add_soft(self._py[i][f])

		#no overlapping

		for i in range(tmp_ncirc):
			for j in range(i+1, tmp_ncirc):
				self._s.add_soft(Or(self._lr[i][j],self._lr[j][i],self._ud[i][j],self._ud[j][i]))

		for i in range(tmp_ncirc):
			for j in range(i+1, tmp_ncirc):
				for e in range(tmp_width-tmp_size[i][0]+1):
					self._s.add_soft(Or(Not(self._lr[i][j]),self._px[i][e],Not(self._px[j][e+tmp_size[i][0]])))

		for i in range(tmp_ncirc):
			for j in range(i+1, tmp_ncirc):
				for f in range(sum_height-tmp_size[j][1]+1):
					self._s.add_soft(Or(Not(self._ud[j][i]),self._py[j][f],Not(self._py[i][f+tmp_size[j][1]])))

		for i in range(tmp_ncirc):
			for j in range(i+1, tmp_ncirc):
				for e in range(tmp_width-tmp_size[j][0]+1):
					self._s.add_soft(Or(Not(self._lr[j][i]),self._px[j][e],Not(self._px[i][e+tmp_size[j,0]])))

		for i in range(tmp_ncirc):
			for j in range(i+1, tmp_ncirc):
				for f in range(sum_height-tmp_size[i][1]+1):
					self._s.add_soft(Or(Not(self._ud[i][j]),self._py[i][f],Not(self._py[j][f+tmp_size[i][1]])))

		#order constraint

		for o in range(sum_height-max_height):
			self._s.add_soft(Or(Not(self._ph[o]),self._ph[o+1]))

		for o in range(1,sum_height-max_height):
			for i in range(tmp_ncirc):
				self._s.add_soft(Or(Not(self._ph[o]),self._py[i][o-tmp_size[i][1]]))

		self._final_height = self._u.height_needed(self._ph,0)

	def solve(self):
		print(self._s.minimize(self._final_height))

