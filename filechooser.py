
import os
import re
import string

class FileChooser():

	def __init__(self):
		self.allowed_prefix = [ 
			'/mnt/data',
			'/home/ftp/serialy',
			'/mnt/kesunka/serialy',
			'/mnt/kesunka/video',
			]
		self.back_item = '__back__'
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

	def goBack(self, item=None):
		print "go back"
		if item.split('/')[-1] == self.back_item:
			print "matches ", self.back_item
			out = self.cpath[:self.cpath.rfind('/')]
			if re.match("("+string.join(self.allowed_prefix, "|")+")", out):
				self.cpath = out
	
	def getList(self):
		out = self.transformList(os.listdir(self.cpath))
		return out
	
	def transformList(self, list):
		out = []
		list.sort()
		for d in list:
			if all(ord(c) < 128 for c in d):
				out.append(d)
		out.insert(0, self.back_item)
		return out

		
if __name__ == "__main__":
	fc = FileChooser()
	print fc.getFile("na/..me")
	print fc.getList()

