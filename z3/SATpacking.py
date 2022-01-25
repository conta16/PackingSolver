from solver import solver
from exception import *
import sys
import time

if __name__ == "__main__":
	if (len(sys.argv) < 2):
		raise ArgumentNumberException()
	s = solver(sys.argv[1])
	s.constraints()
	s.solve()
