from solver import solver
from exception import *
import sys

if __name__ == "__main__":
	if (len(sys.argv) < 2):
		raise ArgumentNumberException()
	s = solver(sys.argv[1])
	#s.debug()
	s.constraints()
	s.solve()
	#s.debug()
