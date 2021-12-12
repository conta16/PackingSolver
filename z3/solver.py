from z3 import *
from data import data
from utility import utility
import numpy as np
import collections

class solver:

	def __init__(self,path):
		self._d = data(path)
		self._u = utility()
		self._s = Optimize()
		self._s.set(priority='pareto')

		tmp_ncirc = self._d.get_num_of_circuits()
		tmp_width = self._d.get_width()

		max_height = self._u.compute_max_height(self._d.get_size())
		sum_height = self._u.compute_sum_height(self._d.get_size())

		#self._lr = [ [ Bool("lr_%s_%s" % (i+1, j+1)) for j in range(tmp_ncirc) ] for i in range(tmp_ncirc) ]
		#self._ud = [ [ Bool("ud_%s_%s" % (i+1, j+1)) for j in range(tmp_ncirc) ] for i in range(tmp_ncirc) ]
		#self._px = [ [ Bool("px_%s_%s" % (i+1, j)) for j in range(tmp_width+1) ] for i in range(tmp_ncirc) ]
		#self._py = [ [ Bool("py_%s_%s" % (i+1, j)) for j in range(sum_height+1) ] for i in range(tmp_ncirc) ]
		self._ph = [ Bool("%s_ph" % (i)) for i in range(max_height,sum_height+1) ]

		self._lr = np.reshape(np.array([ Bool("%s_lr" % (i+1)) for i in range(tmp_ncirc*tmp_ncirc) ]),(tmp_ncirc,-1))
		self._ud = np.reshape(np.array([ Bool("%s_ud" % (i+1)) for i in range(tmp_ncirc*tmp_ncirc) ]),(tmp_ncirc,-1))
		self._px = np.reshape(np.array([ Bool("%s_px" % (i+1)) for i in range((tmp_width+1)*tmp_ncirc) ]),(tmp_ncirc,-1))
		self._py = np.reshape(np.array([ Bool("%s_py" % (i+1)) for i in range((sum_height+1)*tmp_ncirc) ]),(tmp_ncirc,-1))
		print(self._lr)

		self._final_height = Int('final_height')

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
			for f in range(sum_height-tmp_size[i][1]):
				self._s.add(Or(Not(self._py[i][f]),self._py[i][f+1]))

		for i in range(tmp_ncirc):
			for f in range(sum_height-tmp_size[i][1], sum_height+1):
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
				for f in range(sum_height-tmp_size[j][1]+1):
					self._s.add(Or(Not(self._ud[j][i]),self._py[j][f],Not(self._py[i][f+tmp_size[j][1]])))

		for i in range(tmp_ncirc):
			for j in range(i+1, tmp_ncirc):
				for e in range(tmp_width-tmp_size[j][0]+1):
					self._s.add(Or(Not(self._lr[j][i]),self._px[j][e],Not(self._px[i][e+tmp_size[j][0]])))

		for i in range(tmp_ncirc):
			for j in range(i+1, tmp_ncirc):
				for f in range(sum_height-tmp_size[i][1]+1):
					self._s.add(Or(Not(self._ud[i][j]),self._py[i][f],Not(self._py[j][f+tmp_size[i][1]])))

		#order constraint

		for o in range(sum_height-max_height):
			self._s.add(Or(Not(self._ph[o]),self._ph[o+1]))

		for o in range(1,sum_height-max_height):
			for i in range(tmp_ncirc):
				self._s.add(Or(Not(self._ph[o]),self._py[i][o-tmp_size[i][1]]))

		#self._final_height = self._u.height_needed(self._ph,0)
		#self._u.height_needed(self._ph,self._s,self._final_height,0)
		for pos in range(len(self._ph)-1): #this needs to be checked, it is wrong
			self._s.add(Implies(And(self._ph[pos+1],Not(self._ph[pos])),self._final_height==pos))
			self._s.add(Implies(self._final_height==pos,And(self._ph[pos+1],Not(self._ph[pos]))))
		print(self._s)
		#self._s.add(self._final_height <= self._u.height_needed(self._ph,0))
		#self._s.add(self._ph[13])

	def solve(self):
		set_option(max_lines=500,max_args=500)
		mx = self._s.minimize(self._final_height)
		if self._s.check() == sat:
			#print(mx.value())
			pass

		m = self._s.model()

		lr, ud, px, py, ph = {}, {}, {}, {}, {}

		for d in m:
			#print(d," ",m[d])
			if "lr" in str(d):
				lr[str(d)] = 1 if str(m[d]) == 'True' else 0
			elif "ud" in str(d):
				ud[str(d)] = 1 if str(m[d]) == 'True' else 0
			elif "px" in str(d):
				px[str(d)] = 1 if str(m[d]) == 'True' else 0
			elif "py" in str(d):
				py[str(d)] = 1 if str(m[d]) == 'True' else 0
			elif "ph" in str(d):
				ph[str(d)] = 1 if str(m[d]) == 'True' else 0
		#print(lr.items())
		print(px)
		lr = collections.OrderedDict(sorted(lr.items(),key=self._u.comp))
		ud = collections.OrderedDict(sorted(ud.items(),key=self._u.comp))
		px = collections.OrderedDict(sorted(px.items(),key=self._u.comp))
		py = collections.OrderedDict(sorted(py.items(),key=self._u.comp))
		ph = collections.OrderedDict(sorted(ph.items(),key=self._u.comp))
		print(px)
		num = self._d.get_num_of_circuits()

		lr = np.reshape(np.fromiter(lr.values(), dtype=int),(num,-1))
		ud = np.reshape(np.fromiter(ud.values(), dtype=int),(num,-1))
		px = np.reshape(np.fromiter(px.values(), dtype=int),(num,-1))
		py = np.reshape(np.fromiter(py.values(), dtype=int),(num,-1))
		ph = np.fromiter(ph.values(), dtype=int)
		#print(self._py)
		print(lr)
		print(ud)
		print(px)
		print(py)
		print(ph)
