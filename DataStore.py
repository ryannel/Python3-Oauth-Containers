import shelve
import os, __main__

class DataStore():
	def __init__ (self, name):
		mainPath = os.path.dirname(os.path.abspath(__main__.__file__))
		self.db = shelve.open(mainPath +'/'+name)
		
	def get(self, key):
		try:
			model = self.db[key]
		except KeyError:
			model = {}
		return model
		
	def set(self, key, value):
		self.db[key] = value
