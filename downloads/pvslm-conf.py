from sys import stdin
from subprocess import check_output
from fileinput import close
import subprocess
import sys
import os

global PVSPATH
PVSPATH=None

PVS="PVS_PATH"
envVar=os.environ
vals=envVar.keys()
for var in vals:
  if var.find(PVS)>=0:
    PVSPATH=envVar[var]
    break

if PVSPATH==None:
  print "PVS is not installed, please install and configure it first"
  sys.exit()

global repoPath
global confPath
global srcPath

DEFAULT_INSTALL_DIR = PVSPATH
DEFAULT_REPOSRC_DIR = PVSPATH+'/.pvslm/reposrc'
DEFAULT_REPOS_DIR = PVSPATH+'/.pvslm/repos'

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

srcPath=confPath+'/.pvslm/reposrc' 
replace=subprocess.Popen('mkdir -p '+srcPath,shell=True)
replace.communicate()[0]

repoPath=confPath+'/.pvslm/repos'
replace=subprocess.Popen('mkdir -p '+repoPath,shell=True)
replace.communicate()[0]

try:
  copy=subprocess.Popen('curl http://migueleci.github.io/pvslm/downloads/pvslm.py -o pvslm.py',shell=True)
  copy.communicate()[0]
  
  config='"'+confPath+'"'
  repoPath='"'+repoPath+'"'
  srcPath='"'+srcPath+'"'
  
  replace=subprocess.Popen('sed -e "s,pvslmPath,'+config+'," < pvslm.py > tmp.9996',shell=True)
  replace.communicate()[0]
  
  output=subprocess.Popen('mv tmp.9996 pvslm.py',shell=True)
  output.communicate()[0]
  
  replace=subprocess.Popen('sed -e "s,pvslmRep,'+repoPath+'," < pvslm.py > tmp.9998',shell=True)
  replace.communicate()[0]
  
  output=subprocess.Popen('mv tmp.9998 pvslm.py',shell=True)
  output.communicate()[0]
    
  replace=subprocess.Popen('sed -e "s,pvslmSrc,'+srcPath+'," < pvslm.py > tmp.9997',shell=True)
  replace.communicate()[0]
  
  output=subprocess.Popen('mv tmp.9997 pvslm.py',shell=True)
  output.communicate()[0]
    
  copy=subprocess.Popen('rsync -azh pvslm.py '+confPath,shell=True)
  copy.communicate()[0]
  
  copy=subprocess.Popen('chmod +x '+confPath+'/pvslm.py',shell=True)
  copy.communicate()[0]
  
  copy=subprocess.Popen('curl http://migueleci.github.io/pvslm/downloads/nasalib.list -o nasalib.list',shell=True)
  copy.communicate()[0]
  
  copy=subprocess.Popen('rsync -azh nasalib.list '+srcPath,shell=True)
  copy.communicate()[0]

  clone=subprocess.Popen('git clone https://github.com/nasa/pvslib.git '+repoPath+'/nasalib',shell=True)
  clone.communicate()[0]
    
  copy=subprocess.Popen('rsync -azh '+repoPath+'/nasalib/pvs-emacs '+PVSPATH+'/nasalib/',shell=True)
  copy.communicate()[0]
  
  copy=subprocess.Popen('rsync -azh '+repoPath+'/nasalib/PVSioChecker '+PVSPATH+'/nasalib/',shell=True)
  copy.communicate()[0]

  copy=subprocess.Popen('rsync -azh '+repoPath+'/nasalib/pvs-patches '+PVSPATH+'/nasalib/',shell=True)
  copy.communicate()[0]
  
  delete=subprocess.Popen('rm -rf pvslm.py',shell=True)
  delete.communicate()[0]
  
  delete=subprocess.Popen('rm -rf pvslm-install',shell=True)
  delete.communicate()[0]
  
  delete=subprocess.Popen('rm -rf nasalib.list',shell=True)
  delete.communicate()[0]
  
  print 'PVS Library Manager has been successfully configured. Thanks!'
except:
  print 'Something went wrong. Please try again.'
