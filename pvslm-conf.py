from sys import stdin
from subprocess import check_output
import subprocess
import os

global repoPath
global confPath
global srcPath

def pathAssing(name):
	ok=False
	while(not ok):
		try:
			path=raw_input("Enter the "+name+" path: ")
			if (not os.path.exists(path)):
				replace=subprocess.Popen('mkdir -p '+path,shell=True)	
				replace.communicate()[0]
			ok=True
		except:
			print 'The directory is not correct. Please try again!'
	return path

srcPath=pathAssing('source')
repoPath=pathAssing('repository')
confPath=pathAssing('configuration')

try:
	copy=subprocess.Popen('curl http://migueleci.github.io/pvslm/downloads/pvslm.py -o pvslm.py',shell=True)
	copy.communicate()[0]

	config='"'+confPath+'"'
	repoPath='"'+repoPath+'"'
	srcPath='"'+srcPath+'"'

	for i in range (0,2):
		replace=subprocess.Popen('sed -e "s,pvslmPath,'+config+'," < pvslm.py > tmp.9996',shell=True)
		output=subprocess.Popen('mv tmp.9996 pvslm.py',shell=True)

		replace=subprocess.Popen('sed -e "s,pvslmRep,'+repoPath+'," < pvslm.py > tmp.9998',shell=True)
		output=subprocess.Popen('mv tmp.9998 pvslm.py',shell=True)

		replace=subprocess.Popen('sed -e "s,pvslmSrc,'+srcPath+'," < pvslm.py > tmp.9997',shell=True)
		output=subprocess.Popen('mv tmp.9997 pvslm.py',shell=True)

	copy=subprocess.Popen('cp -r pvslm.py '+confPath,shell=True)
	copy=subprocess.Popen('chmod +x '+confPath+'/pvslm.py',shell=True)
	copy.communicate()[0]

	print 'PVS Library Manager has been successfully configured. Thanks!'
except:
	print 'Something went wrong. Please try again.'
