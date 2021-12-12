from z3 import *
from data import data
from utility import utility
import numpy as np

class solver:

	def __init__(self,path):
		self._d = data(path)
		self._u = utility()
		self._s = Optimize()
		self._s.set(priority='pareto')

		tmp_ncirc = self._d.get_num_of_circuits()
		tmp_width = self._d.get_width()

		self._max_height = self._u.compute_max_height(self._d.get_size())
		self._sum_height = self._u.compute_sum_height(self._d.get_size())

		self._ph = [ Bool("%s_ph" % (i)) for i in range(self._max_height,self._sum_height+1) ]

		self._lr = np.reshape(np.array([ Bool("%s_lr" % (i+1)) for i in range(tmp_ncirc*tmp_ncirc) ]),(tmp_ncirc,-1))
		self._ud = np.reshape(np.array([ Bool("%s_ud" % (i+1)) for i in range(tmp_ncirc*tmp_ncirc) ]),(tmp_ncirc,-1))
		self._px = np.reshape(np.array([ Bool("%s_px" % (i+1)) for i in range((tmp_width+1)*tmp_ncirc) ]),(tmp_ncirc,-1))
		self._py = np.reshape(np.array([ Bool("%s_py" % (i+1)) for i in range((self._sum_height+1)*tmp_ncirc) ]),(tmp_ncirc,-1))

	def debug(self):
		print(self._d.get_width())
		print(self._d.get_num_of_circuits())
		print(self._d.get_size())

	def constraints(self):
		tmp_ncirc = self._d.get_num_of_circuits()
		tmp_width = self._d.get_width()
		tmp_size = self._d.get_size()

		#order encoding

		for i in range(tmp_ncirc):
			self._s.add(Not(self._px[i][0]))

		for i in range(tmp_ncirc):
			self._s.add(Not(self._py[i][0]))

		for i in range(tmp_ncirc):
			for e in range(tmp_width-tmp_size[i][0]):
				self._s.add(Or(Not(self._px[i][e]),self._px[i][e+1]))

		for i in range(tmp_ncirc):
			for e in range(tmp_width-tmp_size[i][0], tmp_width+1):
				self._s.add(self._px[i][e])

		for i in range(tmp_ncirc):
			for f in range(self._sum_height-tmp_size[i][1]):
				self._s.add(Or(Not(self._py[i][f]),self._py[i][f+1]))

		for i in range(tmp_ncirc):
			for f in range(self._sum_height-tmp_size[i][1], self._sum_height+1):
				self._s.add(self._py[i][f])

		#no overlapping
		####
		for i in range(tmp_ncirc):
			self._s.add(Not(self._lr[i][i]))

		for i in range(tmp_ncirc):
			self._s.add(Not(self._ud[i][i]))
		####
		for i in range(tmp_ncirc):
			for j in range(i+1, tmp_ncirc):
				self._s.add(Or(self._lr[i][j],self._lr[j][i],self._ud[i][j],self._ud[j][i]))

		for i in range(tmp_ncirc):
			for j in range(i+1, tmp_ncirc):
				for e in range(tmp_width-tmp_size[i][0]+1):
					self._s.add(Or(Not(self._lr[i][j]),self._px[i][e],Not(self._px[j][e+tmp_size[i][0]])))

		for i in range(tmp_ncirc):
			for j in range(i+1, tmp_ncirc):
				for f in range(self._sum_height-tmp_size[j][1]+1):
					self._s.add(Or(Not(self._ud[j][i]),self._py[j][f],Not(self._py[i][f+tmp_size[j][1]])))

		for i in range(tmp_ncirc):
			for j in range(i+1, tmp_ncirc):
				for e in range(tmp_width-tmp_size[j][0]+1):
					self._s.add(Or(Not(self._lr[j][i]),self._px[j][e],Not(self._px[i][e+tmp_size[j][0]])))

		for i in range(tmp_ncirc):
			for j in range(i+1, tmp_ncirc):
				for f in range(self._sum_height-tmp_size[i][1]+1):
					self._s.add(Or(Not(self._ud[i][j]),self._py[i][f],Not(self._py[j][f+tmp_size[i][1]])))

		#order constraint

		for o in range(self._sum_height-self._max_height):
			self._s.add(Or(Not(self._ph[o]),self._ph[o+1]))

		for o in range(1,self._sum_height-self._max_height):
			for i in range(tmp_ncirc):
				self._s.add(Or(Not(self._ph[o]),self._py[i][o-tmp_size[i][1]]))

	def solve(self):
		set_option(max_lines=500,max_args=500)
		mx = self._s.minimize(self._u.get_sym_height(self._ph))
		if self._s.check() == sat:
			m = self._s.model()

			lr, ud, px, py, ph = self._u.symb2array(m,self._d.get_num_of_circuits())

			final_height = self._u.get_height(ph) - 1

			x_coordinates = self._u.get_coordinates(px)
			y_coordinates = self._u.get_coordinates(py)

			self._u.debug(self._d.get_width(),self._d.get_num_of_circuits(),self._d.get_size(),lr,ud,px,py,ph)
			self._u.plot(x_coordinates,y_coordinates,self._d.get_size(),self._d.get_width()-1,final_height)
		else:
			print("unsat")
