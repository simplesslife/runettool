import os
import ConfigParser
import datetime
import string 




class tagGetter:

	def __init__(self,opt):
		self.opt = opt
		self.tagSet = set()
		self.config = ConfigParser.ConfigParser('')

	def getTags(self,changeFileName):
		self.config.read(self.opt.mappingFilePath)
		tagStr = self.config.get('MAPPING',changeFileName)
		return string.split(tagStr,',')

	def addTag(self,filepath):
		fileHandle = open(filepath,'r')
		with fileHandle:
			fileList = fileHandle.readlines()
			for fileLine in fileList:
				fileLine = string.replace(fileLine,'\r','')
				fileLine = string.replace(fileLine,'\n','')
				taglists = self.getTags(fileLine)
				for item in taglists:
					self.tagSet.add(item)


	def run(self):
		if os.path.exists(self.opt.logPath):
			for root, dirs, files in os.walk(self.opt.logPath):
				for filename in files:
					fileCreateTimeStr = filename.split('.')[0]
					fileCreateTime = ''
					try:
						fileCreateTime = datetime.datetime.strptime(fileCreateTimeStr,'%Y-%m-%d-%H-%M')
					except:
						continue
					timeSpan = self.opt.curTime - fileCreateTime
					if timeSpan < self.opt.timeSpanMax:
						filepath = os.path.join(self.opt.logPath,filename)
						self.addTag(filepath)
		else:
			print 'no file exists'

		return self.tagSet