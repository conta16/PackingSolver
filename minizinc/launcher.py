import os
import sys
import re
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random

"""
usage: python3 launcher.py [.dzn file]
The script launches the SATpacking.mzn program and shows the results in a graphical window
"""

def launch_command(valeus_path):
	os.system('minizinc SATpacking.mzn '+values_path+' > tmp.txt')

def regex_reduction(solution):
	"""
	input: solution given by minizinc in string format
	output: solution with each true and false turned into 1 and 0 respectively
	"""
	solution = re.sub('true','1',solution)
	solution = re.sub('false','0',solution)
	return eval('['+re.split('\]',re.split('\[',solution)[1])[0]+']')

def get_solution():
	"""
	output: applies regex_reduction to each line of the output given by minizinc.
		Returns a string containing the output of minizinc
	"""
	with open('tmp.txt','r') as f:
		solution = f.readlines()[:-2]
		for i in range(len(solution)):
			solution[i] = regex_reduction(solution[i])
	os.remove('tmp.txt')
	return solution

def get_values(values_path):
	"""
	input: path to .dzn file
	output: width of plate, number of circuits, size of each circuit. These values are taken from the .dzn file
	"""
	with open(values_path,'r') as f:
		values = f.readlines()
		w = eval(re.split(';',re.split('=',values[0])[1][1:])[0])
		num_of_circuits = eval(re.split(';',re.split('=',values[1])[1][1:])[0])
		size = values[2:]
		size[0] = re.split('=',size[0])[1]
		for i in range(len(size)):
			size[i] = re.sub('\t','',size[i])
			size[i] = re.sub('\n','',size[i])
		size[-1] = re.sub('\|','[',size[-1],1)
		size[-1] = re.split(';',re.sub('\|',']',size[-1]))[0]
		for i in range(len(size)-1):
			size[i] = re.sub('\|','[',size[i])+'],'
		size = eval(''.join(size))
	return w, num_of_circuits, size

def reshape(lr,ud,px,py):
	"""
	Simple reshaping, applied by following the matrix dimensions specified in the pdf paper
	"""
	return np.reshape(lr,(n,n)), np.reshape(ud,(n,n)), np.reshape(px,(n,-1)), np.reshape(py,(n,-1))

def get_coordinates(p):
	coordinates = []
	for row in p:
		i = 0
		while i < len(row)-1:
			if (i==0 and row[i]) or (not row[i] and row[i+1]):
				coordinates.append(i)
				break
			i += 1
	return coordinates

def get_height(ph):
	height = -1
	for i in range(len(ph)-1):
		if (i==0 and ph[i]) or (not ph[i] and ph[i+1]):
			height = i
			break
	return height

def get_max_height(size_h):
	max_height = -1
	for el in size_h:
		if el > max_height:
			max_height = el
	return max_height

def plot(x_coordinates,y_coordinates,size,w,h):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	for i in range(len(size)):
		hexadecimal = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
		rect = matplotlib.patches.Rectangle((x_coordinates[i],y_coordinates[i]), size[i][0], size[i][1], color=hexadecimal)
		ax.add_patch(rect)
	plt.xlim([0, w])
	plt.ylim([0, h])
	print(h)
	plt.figtext(0.5, 0.01, "minimum height: "+str(h), wrap=True, horizontalalignment='center', fontsize=12)
	plt.show()

def debug(w,num_of_circuits,size,lr,ud,px,py,ph):
        print("Width:",w)
        print("Num of circuits:",num_of_circuits)
        print("Size of circuits:",size)
        print("lr:",lr)
        print("ud:",ud)
        print("px:",px)
        print("py:",py)
        print("ph:",ph)

if len(sys.argv) != 2:
	print("error: wrong number of arguments (got",len(sys.argv),"expected 2)")
else:
	values_path = sys.argv[1]
	launch_command(values_path)
	lr, ud, px, py, ph = get_solution()
	w, n, size = get_values(values_path)
	lr, ud, px, py = reshape(lr,ud,px,py)
	debug(w,n,size,lr,ud,px,py,ph)
	x_coordinates, y_coordinates = get_coordinates(px), get_coordinates(py)
	size = np.array(size)
	height = get_height(ph) + get_max_height(size[:,1])
	print(size[:,1])
	print(get_height(ph))
	print(get_max_height(size[:,1]))
	print(height)
	plot(x_coordinates,y_coordinates,size,w,height)
