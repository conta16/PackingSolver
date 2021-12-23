from z3 import *
import collections
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random

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

	def height_needed(self,ph,s,final_height,pos):
		if pos == self._sum-self._max:
			print("err")
			#return pos
		else:
			s.add(Implies(And(ph[pos+1],Not(ph[pos])),final_height==pos))
			self.height_needed(ph,s,final_height,pos+1)

	def comp(self,o): #used for ordering ordered_dict based on first integer inside str
  		return int(o[0].split('_')[0])

	def get_sym_height(self,ph,i=0):
		if i==0:
			return If(ph[i],i,self.get_sym_height(ph,i+1))
		elif i==len(ph)-1:
			return If(ph[i],i,i+1)
		else:
			return If(ph[i+1] != ph[i],i+1,self.get_sym_height(ph,i+1))

	def get_height(self,ph,i=0):
		if i==len(ph)-1:
			return i if ph[i] else i+1
		elif not ph[i] and ph[i+1]:
			return i+1
		return self.get_height(ph,i+1)

	def symb2array(self,m,num):
		lr, ud, px, py, ph = {}, {}, {}, {}, {}

		for d in m:
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

		lr = collections.OrderedDict(sorted(lr.items(),key=self.comp))
		ud = collections.OrderedDict(sorted(ud.items(),key=self.comp))
		px = collections.OrderedDict(sorted(px.items(),key=self.comp))
		py = collections.OrderedDict(sorted(py.items(),key=self.comp))
		ph = collections.OrderedDict(sorted(ph.items(),key=self.comp))

		lr = np.reshape(np.fromiter(lr.values(), dtype=int),(num,-1))
		ud = np.reshape(np.fromiter(ud.values(), dtype=int),(num,-1))
		px = np.reshape(np.fromiter(px.values(), dtype=int),(num,-1))
		py = np.reshape(np.fromiter(py.values(), dtype=int),(num,-1))
		ph = np.fromiter(ph.values(), dtype=int)

		return lr,ud,px,py,ph

	def get_coordinates(self,p):
		coordinates = []
		for row in p:
			i = 0
			while i < len(row)-1:
				if (i==0 and row[i]) or (not row[i] and row[i+1]):
					coordinates.append(i)
					break
				i += 1
		return coordinates

	def plot(self,x_coordinates,y_coordinates,size,w,h):
		fig = plt.figure()
		ax = fig.add_subplot(111)
		for i in range(len(size)):
			hexadecimal = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
			rect = matplotlib.patches.Rectangle((x_coordinates[i],y_coordinates[i]), size[i][0], size[i][1], color=hexadecimal)
			ax.add_patch(rect)
		plt.xlim([0, w])
		plt.ylim([0, h])
		plt.figtext(0.5, 0.01, "minimum height: "+str(h), wrap=True, horizontalalignment='center', fontsize=12)
		plt.show()

	def get_max_index(self,arr):
		max = -1
		pos = -1
		for i in range(len(arr)):
			if arr[i] > max:
				max = arr[i]
				pos = i
		return pos

	def debug(self,w,num_of_circuits,size,lr,ud,px,py,ph):
		print("Width:",w)
		print("Num of circuits:",num_of_circuits)
		print("Size of circuits:",size)
		print("lr:",lr)
		print("ud:",ud)
		print("px:",px)
		print("py:",py)
		print("ph:",ph)

