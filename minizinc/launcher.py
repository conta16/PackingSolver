import os
import sys
import re
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random

"""
usage: python3 launcher.py [.mzn file] [.dzn file]
The script launches the packing .mzn program and shows the results in a graphical window
"""

def launch_command(mzn_path,values_path):
	os.system('minizinc '+mzn_path+' '+values_path+' > tmp.txt')

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
	ROTATION = False
	with open('tmp.txt','r') as f:
		solution = f.readlines()[:-2]
		if len(solution) == 6:
			ROTATION = True
		for i in range(len(solution)):
			solution[i] = regex_reduction(solution[i])
	os.remove('tmp.txt')
	if ROTATION:
		return solution, True
	else:
		return solution, False

def get_values(values_path):
        """
        input: path to .dzn file
        output: width of plate, number of circuits, size of each circuit. These values are taken from the .dzn file
        """
        with open(values_path,'r') as f:
                values = f.readlines()
                w = eval(re.split(';',re.split('=',values[0])[1][1:])[0])
                num_of_circuits = eval(re.split(';',re.split('=',values[1])[1][1:])[0])
                width = eval(re.split(';',re.split('=',values[2])[1][1:])[0])
                height = eval(re.split(';',re.split('=',values[3])[1][1:])[0])
        return w, num_of_circuits, width, height


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

def plot(x_coordinates,y_coordinates,size,w,h,rotation_sol=[]):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	for i in range(len(size)):
		hexadecimal = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
		if len(rotation_sol) > 0 and rotation_sol[i]:
			rect = matplotlib.patches.Rectangle((x_coordinates[i],y_coordinates[i]), size[i][1], size[i][0], color=hexadecimal)
		else:
			rect = matplotlib.patches.Rectangle((x_coordinates[i],y_coordinates[i]), size[i][0], size[i][1], color=hexadecimal)
		ax.add_patch(rect)
	plt.xlim([0, w])
	plt.ylim([0, h])
	plt.figtext(0.5, 0.01, "minimum height: "+str(h), wrap=True, horizontalalignment='center', fontsize=12)
	plt.show()

def debug(w,num_of_circuits,size,solution,rotation):
        print("Width:",w)
        print("Num of circuits:",num_of_circuits)
        print("Size of circuits:",size)
        print("lr:",solution[0])
        print("ud:",solution[1])
        print("px:",solution[2])
        print("py:",solution[3])
        print("ph:",solution[4])
        if rotation:
                print("rotation:",solution[5])
        else:
                print("rotation: False")

if len(sys.argv) != 3:
	print("error: wrong number of arguments (got",len(sys.argv),"expected 2)")
else:
	mzn_path = sys.argv[1]
	values_path = sys.argv[2]
	launch_command(mzn_path,values_path)
	solution, rotation = get_solution()
	w, n, size = get_values(values_path)
	solution[0], solution[1], solution[2], solution[3] = reshape(solution[0],solution[1],solution[2],solution[3])
	x_coordinates, y_coordinates = get_coordinates(solution[2]), get_coordinates(solution[3])
	size = np.array(size)
	height = get_height(solution[4]) + get_max_height(size[:,1])
	debug(w,n,size,solution,rotation)
	if rotation:
		plot(x_coordinates,y_coordinates,size,w,height,solution[5])
	else:
		plot(x_coordinates,y_coordinates,size,w,height)
