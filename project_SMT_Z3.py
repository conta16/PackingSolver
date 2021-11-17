#!/usr/bin/env python
# coding: utf-8

from z3 import *
from os import listdir
from os.path import isfile, join
from pathlib import Path
from itertools import combinations
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch

random.seed(42)

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

def print_solution(plates, sol):
    # coordinates of the left-bottom corners of the plates
    coords_plates = [list(plate['coords']) for plate in sol[1:]]

    print(str(sol[0]['width']) + " " + str(sol[0]['length']))
    print(str(sol[0]['number of plates']))

    for coords_plate, plate in zip(coords_plates, plates):
        print(str(plate[0]) + " " + str(plate[1]) + " " + coords_plate[0] + " " + coords_plate[1])


def show_solution(plates, sol):
    # coordinates of the left-bottom corners of the plates
    coords_plates = [list(plate['coords']) for plate in sol[1:]]

    fig, ax = plt.subplots()
    rectangles = {}
    colours = []

    # create a list of random colours
    for i in range(sol[0]["number of plates"]):
        colours.append('#%06X' % randint(0, 0xFFFFFF))

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
                    fontsize=20, ha='center', va='center')

    ax.set_xlim((0, sol[0]["width"]))
    ax.set_ylim((0, sol[0]["length"]))
    ax.set_aspect('equal')
    plt.grid(color="black", linestyle="--", linewidth=1)
    plt.xticks(np.arange(0, sol[0]["width"], step = 1))
    plt.yticks(np.arange(0, sol[0]["width"], step = 1))
    plt.show()


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
    "length": m.get_interp(length).as_long(),
    "number of plates": n
})
for i in range(n):
    sol.append({
        "plate": i,
        "coords": m.evaluate(X[i]).as_string() + m.evaluate(Y[i]).as_string()
    })

print_solution(plates, sol)
show_solution(plates, sol)

