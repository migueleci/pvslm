from sys import stdin
from subprocess import check_output
import subprocess
import os

global repoPath
global confPath
global srcPath

DEFAULT_INSTALL_DIR = '/usr/local/bin'
DEFAULT_REPOSRC_DIR = '$HOME/.pvslm/reposrc'
DEFAULT_REPOS_DIR = '$HOME/.pvslm/repos'

def pathAssing(name,default):
  ok=False
  while(not ok):
    try:
      path=raw_input("Enter the {0} (default={1}): ".format(name,default))
      path = path.strip()
      if len(path)==0: path=default
      if (not os.path.exists(path)):
        replace=subprocess.Popen('mkdir -p '+path,shell=True)
        replace.communicate()[0]
      ok=True
    except:
      print 'The provided path is not valid; please try again.'
  return path

confPath=pathAssing('library manager installation path',DEFAULT_INSTALL_DIR)
srcPath=pathAssing('repositories source configuration path',DEFAULT_REPOSRC_DIR)
repoPath=pathAssing('repositories download path',DEFAULT_REPOS_DIR)

try:
	copy=subprocess.Popen('sudo curl http://migueleci.github.io/pvslm/downloads/pvslm.py -o pvslm.py',shell=True)
	copy.communicate()[0]

	config='"'+confPath+'"'
	repoPath='"'+repoPath+'"'
	srcPath='"'+srcPath+'"'

	for i in range (0,2):
		replace=subprocess.Popen('sudo sed -e "s,pvslmPath,'+config+'," < pvslm.py > tmp.9996',shell=True)
		output=subprocess.Popen('mv tmp.9996 pvslm.py',shell=True)

		replace=subprocess.Popen('sudo sed -e "s,pvslmRep,'+repoPath+'," < pvslm.py > tmp.9998',shell=True)
		output=subprocess.Popen('mv tmp.9998 pvslm.py',shell=True)

		replace=subprocess.Popen('sudo sed -e "s,pvslmSrc,'+srcPath+'," < pvslm.py > tmp.9997',shell=True)
		output=subprocess.Popen('mv tmp.9997 pvslm.py',shell=True)

	copy=subprocess.Popen('sudo cp -r pvslm.py '+confPath,shell=True)
	copy=subprocess.Popen('sudo chmod +x '+confPath+'/pvslm.py',shell=True)
	copy.communicate()[0]
	
	delete=subprocess.Popen('sudo rm -rf pvslm.py',shell=True)
	delete.communicate()[0]
	print 'PVS Library Manager has been successfully configured. Thanks!'
except:
	print 'Something went wrong. Please try again.'
