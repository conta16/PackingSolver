from z3 import *

# 3x3 matrix of integer variables
A = [ [ Int("a_%s_%s" % (i+1, j+1)) for j in range(3) ] 
      for i in range(3) ]
print(A)

# Rows constraints
rows_c = [ Sum(r) == 1 for r in A ]
print(rows_c)

# Columns constraints
A_transpose = [ [ A[i][j] for i in range(3) ] for j in range(3) ]
cols_c = [ Sum(c) <= 10 for c in A_transpose ]
print(cols_c)

s = Solver()
s.add(rows_c)
s.add(cols_c)
# solve constraints
print(s.check())
# print solution
m = s.model()
print(m)
# printing the solution in a nicer way
r = [ [ m.evaluate(A[i][j]) for j in range(3) ] for i in range(3) ]
print_matrix(r)
