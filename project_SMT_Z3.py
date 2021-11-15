!/usr/bin/env python
# coding: utf-8

# In[99]:


from z3 import *
from os import listdir
from os.path import isfile, join
from pathlib import Path
from itertools import combinations

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

# extract the content of each instance as it appears in the corresponding file
def get_instance(path, instance):
    file = join(path, instance)
    
    instance = {}
    
    with open(file, "r") as _file:
        for idx, line in enumerate(_file):
            stripped_line = line.strip()
            stripped_line = stripped_line.replace(" ", "")
            instance[idx] = list(stripped_line)
    
    return instance

print(get_instance(path, files_dict['ins-1']))

# extract useful information from the dict representing the instance
def extract_data(instance):
    plates = []
    width = 0
    n_circuits = 0
    for key, value in instance.items():
        # element with key 0 is the width of the plate
        if key == 0:
            width = int(value[0])
        # element with key 1 is the number of circuits
        elif key == 1:
            n_circuits = int(value[0])
        else:
            list_ints = [int(x) for x in value]
            plates.append(list_ints)
    return width, n_circuits, plates

w, n, plates = extract_data(get_instance(path, files_dict["ins-1"]))
print("width: " + str(w))
print("number of circuits: " + str(n))
print("plates:", plates)

# X coordinates of the plates' bottom-left corners
X = [ Int('x%s' % i) for i in range(n) ]
# Y coordinates of the plates' bottom-left corners
Y = [ Int('y%s' % i) for i in range(n)]

def max_z3(vars):
    max = vars[0]
    for v in vars[1:]:
        max = If(v > max, v, max)
    return max

opt = Optimize()

# Constraints

# all coordinates must be positive
positive_x = [X[i] >= 0 for i in range(n)]
positive_y = [Y[i] >= 0 for i in range(n)]

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
max_w = max_z3([X[i] + plates[i][0] for i in range(n)]) <= w # upper bound to width
opt.add(max_w)

# length to minimize
length = Int('length')
objective = length == max_z3([Y[i] + plates[i][1] for i in range(n)])
opt.add(objective)
opt.minimize(length)

opt.check()
m = opt.model()

sol = []
sol.append({
    "width": w,
    "length": m.get_interp(length),
    "number of plates": n
})
for i in range(n):
    sol.append({
        "plate": i,
        "coords": m.evaluate(X[i]).as_string() + " " + m.evaluate(Y[i]).as_string()
    })
print(sol)

