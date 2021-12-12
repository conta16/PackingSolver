#!/usr/bin/env python
# coding: utf-8

# In[62]:


from z3 import *
from os import listdir
from os.path import isfile, join
from pathlib import Path
from itertools import combinations
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
import math


# In[63]:


path = "instances/"

# extract the files contained in directory "instances"
files = [f for f in listdir(path) if isfile(join(path, f))]

# build a dictionary starting from the list containing all the files
files_dict = {}
for f in files:
    # the key for each element in the dictionary will be instance's name excluding the file extension
    instance = f[:f.index(".")]
    files_dict[instance] = f
print(files_dict)


# In[64]:


# extract the content of each instance as it appears in the corresponding file
def get_instance(path, instance):
    file = join(path, instance)
    
    instance = {}
    
    with open(file, "r") as _file:
        for idx, line in enumerate(_file):
            words = line.split()
            words = list(words)
            instance[idx] = words
    
    return instance


# In[65]:


# extract useful information from the dict representing the instance
def extract_data(instance):
    plates = []
    width = 0
    n_circuits = 0
    print(instance.items())
    for key, value in instance.items():
        # element with key 0 is the width of the plate
        if key == 0:
            width = int("".join(value))
        # element with key 1 is the number of circuits
        elif key == 1:
            n_circuits = int("".join(value))
        else:
            list_ints = [int(x) for x in value]
            plates.append(list_ints)
    return width, n_circuits, plates


# In[66]:


w, n, plates = extract_data(get_instance(path, files_dict["ins-10"]))
print("width: " + str(w))
print("number of circuits: " + str(n))
print("plates:", plates)

# compute the area of each plate (for symmetry breaking constraints)
areas = [plate[0] * plate[1] for plate in plates]
print("areas: {}".format(areas))


# In[67]:


# X coordinates of the plates' bottom-left corners
X = [ Int('x%s' % i) for i in range(n) ]
# Y coordinates of the plates' bottom-left corners
Y = [ Int('y%s' % i) for i in range(n)]


# In[68]:


def max_z3(vars):
    max = vars[0]
    for v in vars[1:]:
        max = If(v > max, v, max)
    return max


# In[69]:


def print_solution(plates, sol):
    # coordinates of the left-bottom corners of the plates
    coords_plates = [list(plate['coords']) for plate in sol[1:]]

    print(str(sol[0]['width']) + " " + str(sol[0]['length']))
    print(str(sol[0]['number of plates']))
    
    for coords_plate, plate in zip(coords_plates, plates):
        print(str(plate[0]) + " " + str(plate[1]) + " " + coords_plate[0] + " " + coords_plate[1])


# In[70]:


def show_solution(plates, sol):
    # coordinates of the left-bottom corners of the plates
    coords_plates = [list(plate['coords']) for plate in sol[1:]]
    
    fig, ax = plt.subplots()
    rectangles = {}
    colours = []
    
    # create a list of random colours
    random.seed(10000)
    for i in range(sol[0]["number of plates"]):
        colours.append('#%06X' % random.randint(0, 0xFFFFFF))
    
    # add rectangular patches(one for each plate) to the dictionary
    for coords_plate, plate in zip(coords_plates, plates):
        idx = plates.index(plate)
        col_idx = idx
        rectangles[idx] = mpatch.Rectangle((int(coords_plate[0]), int(coords_plate[1])),
                                           plate[0], plate[1], color=colours[idx])
    
    # draw the patches and add the number identifying the plate in the center of the patch
    for r in rectangles:
        ax.add_artist(rectangles[r])
        rx, ry = rectangles[r].get_xy()
        cx = rx + rectangles[r].get_width()/2.0
        cy = ry + rectangles[r].get_height()/2.0
        
        ax.annotate(r, (cx, cy), color="w", weight='bold', 
                    fontsize=16, ha='center', va='center')

    ax.set_xlim((0, sol[0]["max_width"]))
    ax.set_ylim((0, sol[0]["length"]))
    ax.margins=(1)
    # ax.set_aspect('equal')
    plt.grid(color="black", linestyle="--", linewidth=1)
    plt.xticks(np.arange(0, sol[0]["width"]+1, step = 1))
    plt.yticks(np.arange(0, sol[0]["length"]+1, step = 1))
    # plot the bottom-left corners as black dots
    plt.plot(np.array([int(coords_plate[0]) for coords_plate in coords_plates]), 
                np.array([int(coords_plate[1]) for coords_plate in coords_plates]),
                color="black",
                marker='o',
                linestyle='None')
    plt.show()


# In[71]:


#%%time
# to see the effects of symmetry breaking uncomment the previous line
opt = Optimize()

# Domain reducing constraints and objective

# length to minimize
length = Int('length')
objective = length == max_z3([Y[i] + plates[i][1] for i in range(n)])
opt.add(objective)
opt.minimize(length)

# all coordinates must be positive and can't overlap the edges of the circuit
positive_x = [And(X[i] >= 0, X[i] <= w - plates[i][0]) for i in range(n)]
positive_y = [And(Y[i] >= 0, Y[i] <= length - plates[i][1]) for i in range(n)]

opt.add(positive_x + positive_y)

# no overlapping plates
no_overlapping = []
for (i,j) in combinations(range(n),2):
    no_overlapping.append(
        Or(X[i] + plates[i][0] <= X[j],
           X[j] + plates[j][0] <= X[i],
           Y[i] + plates[i][1] <= Y[j],
           Y[j] + plates[j][1] <= Y[i])
    )
opt.add(no_overlapping)

# max_width
max_w = Int('max_w')
upper_bound = max_w == max_z3([X[i] + plates[i][0] for i in range(n)]) <= w # upper bound to width
opt.add(upper_bound)

# reduce domain of the maximum rectangle (width) (Section 4.2 paper16soh.pdf)

width_plates = [plate[0] for plate in plates] # consider only the width of each plate
max_plate_w = width_plates.index(max(width_plates)) # extract the index of the plate with maximum width
# specify new domain for this plate
max_plate_x_dom = [And(X[max_plate_w] >= 0, X[max_plate_w] <= math.floor((w - width_plates[max_plate_w]) / 2))]

# reduce domain of the maximum rectangle (length) (Section 4.2 paper16soh.pdf)

length_plates = [plate[1] for plate in plates] # consider only the length of each plate
max_plate_l = length_plates.index(max(length_plates)) # extract the index of the plate with maximum length
# specify new domain for this plate
max_plate_y_dom = [Y[max_plate_l] >= 0, Y[max_plate_l] <= (length - length_plates[max_plate_l]) / 2]

# can't pack large rectangles which exceed the width or the length constraint (or both)
no_packing = []
for (i,j) in combinations(range(n),2):
    no_packing.append(And(Implies(plates[i][0] + plates[j][0] > w, Not(Y[i] == Y[j])), 
        Implies(plates[i][1] + plates[j][1] > length, Not(X[i] == X[j]))))

# add domain reducing constraints, comment if you don't want them
opt.add(max_plate_x_dom + max_plate_y_dom + no_packing)


# In[72]:


# Symmetry breaking constraints

# impose ordering between plates with equal size
equal_size_sym = []
for (i,j) in combinations(range(n),2):
    equal_size_sym.append(Implies(plates[i] == plates[j], And(X[i] < X[j], Y[i] < Y[j])))
opt.add(equal_size_sym)

# break vertical/horizontal symmetries

# smaller circuits should be to the right or above bigger circuits
smaller_sym = []
for (i,j) in combinations(range(n),2):
    smaller_sym.append(Implies(areas[i] < areas[j], Or(X[i] > X[j], Y[i] > Y[j])))
opt.add(smaller_sym)


# In[73]:


# check model and find solution 

opt.check()
m = opt.model()

sol = []
sol.append({
    "width": w,
    "max_width": m.get_interp(max_w).as_long(),
    "length": m.get_interp(length).as_long(),
    "number of plates": n
})
for i in range(n):
    sol.append({
        "plate": i,
        "coords": [m.evaluate(X[i]).as_string(), m.evaluate(Y[i]).as_string()]
    })

print_solution(plates, sol)
show_solution(plates, sol)


# In[ ]:




