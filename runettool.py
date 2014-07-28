import Queue,subprocess,optparse,datetime,threading
import string,ConfigParser,os
import getTaglist
from time import sleep


def getCmdOperations():
	p = optparse.OptionParser()
	p.add_option("-l","--logpath",action="store",type="string",dest="logPath",
					help='The changelog path')
	p.add_option("-e","--ettoolpath",action="store",type="string",dest="et_toolPath",
					help="The et path")
	p.add_option("-m","--matestpath",action="store",type="string",dest="ma_testPath",
					help="the ma_test path")
	p.add_option("-t","--targets",action="store",type="string",dest="targets",
					help="targets IP address")
	p.add_option("-u","--user",action="store",type="string",dest="targetUser",
					help="target user")
	p.add_option("-p","--passwd",action="store",type="string",dest="targetPasswd",
					help="target passwd")
	p.add_option("--shared_ip",action="store",type="string",dest="shared_IP",
					help="shared ip, sometime need")
	p.add_option("--mappingFilePath",action="store",type="string",dest="mappingFilePath",
					help="mapping file path")

	p.set_defaults( logPath="",
					et_toolPath="",
					ma_testPath="",
					targets="",
					targetUser="",
					targetPasswd="",
					shared_IP="",
					mappingFilePath=""
		)

	return p.parse_args()


class hour_ft:

	def __init__(self,opts,tagSet):
		self.opts = opts
		self.tagQueue = Queue.Queue(20)
		self.tagSet = tagSet

	def productor(self):
		config = ConfigParser.ConfigParser('')

		for root, dirs, files in os.walk(os.path.join(self.opts.ma_testPath,'test_cases')):
			if 'et.ini' in files:
				config.read(os.path.join(root,'et.ini'))
				tagContent = config.get('Task','tag')
		
				for tag in self.tagSet:
					if string.find(tagContent,tag) != -1:
						self.tagQueue.put(root,1)
						print root
						break
		print 'productor done'

	def consumer(self):
		tag = False
		while True:
			path = ''
			try:
				path = self.tagQueue.get(1,20)
			except:
				tag = True
			if tag:
				break
			os.chdir(path)
			var = self.opts.et_toolPath + ' -t ' + self.opts.targets + ' -d ' + \
						self.opts.ma_testPath + ' -u ' + self.opts.targetUser + ' -p ' + \
						self.opts.targetPasswd + ' --shared_ip ' + self.opts.shared_IP
			print var
			subprocess.call(var, shell=True)
		print 'consumer done'


	def run(self):
		t1 = threading.Thread(
			target=self.consumer)
		t2 = threading.Thread(
			target=self.productor)
		t1.start()
		t2.start()
		t1.join()
		t2.join()



if __name__ == '__main__':
	opt,args = getCmdOperations()
	timeSpanMax = datetime.timedelta(hours=1)
	curTime = datetime.datetime.strptime('2014-07-22-15-30','%Y-%m-%d-%H-%M')
	opt.timeSpanMax = timeSpanMax
	opt.curTime = curTime
	tag_getter = getTaglist.tagGetter(opt)
	tagSet = tag_getter.run()
	autoRun = hour_ft(opt,tagSet)
	autoRun.run()
