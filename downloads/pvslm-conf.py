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
			if (os.path.exists(path)):
				ok=True
			else :
				print 'The directory is not correct. Please try again!'
		except:
			print 'The directory is not correct. Please try again!'
	return path

srcPath=pathAssing('source')
repoPath=pathAssing('repository')
confPath=pathAssing('configuration')

for i in range (0,2):
	replace=subprocess.Popen('sed -e "s,^PVSLM=.*$,PVSLM='+confPath+'," < pvslm > tmp.9996',shell=True)
	output=subprocess.Popen('mv tmp.9996 pvslm',shell=True)

	replace=subprocess.Popen('sed -e "s,^PVSLMREP=.*$,PVSLMREP='+repoPath+'," < pvslm > tmp.9998',shell=True)
	output=subprocess.Popen('mv tmp.9998 pvslm',shell=True)

	replace=subprocess.Popen('sed -e "s,^PVSLMSRC=.*$,PVSLMSRC='+srcPath+'," < pvslm > tmp.9997',shell=True)
	output=subprocess.Popen('mv tmp.9997 pvslm',shell=True)

copy=subprocess.Popen('sudo cp -r pvslm '+confPath,shell=True)
print copy.communicate("n\n")[0]
