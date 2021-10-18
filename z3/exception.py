class ArgumentNumberException(Exception):
	def __init__(self):
		self.err = "Wrong number of input arguments"
		super().__init__(self.err)
