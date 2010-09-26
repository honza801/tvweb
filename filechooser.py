
import os
import re
import string

class FileChooser():

	def __init__(self):
		self.allowed_prefix = [ '/mnt/data', '/home/ftp/serialy' ]
		self.cpath = self.allowed_prefix[0] 
	
	def getAllowed(self):
		return self.allowed_prefix

	def getCurrentPath(self):
		return self.cpath

	def getFile(self, filename):
		out = self.cpath + "/" + filename
		if self.checkPath(out):
			return out
		return None
	
	def setPath(self, dir):
		if self.checkPath(dir):
			self.cpath = dir
			
	def checkPath(self, file):
		if re.match("("+string.join(self.allowed_prefix, "|")+")", file) and not re.search("(/\.\.|\.\./)", file):
			return True
		else:
			return False
	
	def getList(self):
		return os.listdir(self.cpath)
	
		
if __name__ == "__main__":
	fc = FileChooser()
	print fc.getFile("na/..me")
	print fc.getList()

