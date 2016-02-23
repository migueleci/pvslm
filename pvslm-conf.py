from sys import stdin
from subprocess import check_output
from fileinput import close
import subprocess
import sys
import os

global PVSPATH
PVSPATH=None

# Find PVS environment variable
PVS="PVS_PATH"
envVar=os.environ
vals=envVar.keys()
for var in vals:
  if var.find(PVS)>=0:
    PVSPATH=envVar[var]
    break

# If the variable is not define, the abort the installation
if PVSPATH==None:
  print "PVS is not installed, please install and configure it first"
  sys.exit()

if PVSPATH[-1]=='/':
  PVSPATH=PVSPATH[0:-1]

global repoPath
global confPath
global srcPath

# Define the paths for the installation
DEFAULT_INSTALL_DIR = PVSPATH
DEFAULT_REPOSRC_DIR = PVSPATH+'/.pvslm/reposrc'
DEFAULT_REPOS_DIR = PVSPATH+'/.pvslm/repos'

# User define Paths
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

if confPath[-1]=='/':
  confPath=confPath[0:-1]

# Create paths for the tool
# Sources Path
srcPath=confPath+'/.pvslm/reposrc' 
replace=subprocess.Popen('mkdir -p '+srcPath,shell=True)
replace.communicate()[0]
# Git Repos Path
repoPath=confPath+'/.pvslm/repos'
replace=subprocess.Popen('mkdir -p '+repoPath,shell=True)
replace.communicate()[0]

try:
  # Download pvslm tool
  copy=subprocess.Popen('curl http://migueleci.github.io/pvslm/downloads/pvslm.py -o pvslm.py',shell=True)
  copy.communicate()[0]
  
  pvsloc='"'+PVSPATH+'"'
  config='"'+confPath+'"'
  repoPath='"'+repoPath+'"'
  srcPath='"'+srcPath+'"'
  
  # Modifiy tool with the especified paths (PVS)
  replace=subprocess.Popen('sed -e "s,pvsPath,'+pvsloc+'," < pvslm.py > tmp.9995',shell=True)
  replace.communicate()[0]
  
  output=subprocess.Popen('mv tmp.9995 pvslm.py',shell=True)
  output.communicate()[0]

  # Modifiy tool with the especified paths (PVSlm)
  replace=subprocess.Popen('sed -e "s,pvslmPath,'+config+'," < pvslm.py > tmp.9996',shell=True)
  replace.communicate()[0]
  
  output=subprocess.Popen('mv tmp.9996 pvslm.py',shell=True)
  output.communicate()[0]
  
  # Modifiy tool with the especified paths (PVSlm Repos)
  replace=subprocess.Popen('sed -e "s,pvslmRep,'+repoPath+'," < pvslm.py > tmp.9998',shell=True)
  replace.communicate()[0]
  
  output=subprocess.Popen('mv tmp.9998 pvslm.py',shell=True)
  output.communicate()[0]
    
  # Modifiy tool with the especified paths (PVSlm Sources)
  replace=subprocess.Popen('sed -e "s,pvslmSrc,'+srcPath+'," < pvslm.py > tmp.9997',shell=True)
  replace.communicate()[0]
  
  output=subprocess.Popen('mv tmp.9997 pvslm.py',shell=True)
  output.communicate()[0]
  
  # Save and copy tool to its path
  copy=subprocess.Popen('rsync -azh pvslm.py '+confPath,shell=True)
  copy.communicate()[0]
  
  # Give permissions to the tool (executable)
  copy=subprocess.Popen('chmod +x '+confPath+'/pvslm.py',shell=True)
  copy.communicate()[0]

  if confPath!=PVSPATH:
    link=subprocess.Popen('ln -s '+confPath+'/pvslm.py '+PVSPATH+'/',shell=True)
    link.communicate()[0]

  # Download NASALIB 
  copy=subprocess.Popen('curl http://migueleci.github.io/pvslm/downloads/nasalib.list -o nasalib.list',shell=True)
  copy.communicate()[0]
  
  # Copy nasalib to the Sources Path
  copy=subprocess.Popen('rsync -azh nasalib.list '+srcPath,shell=True)
  copy.communicate()[0]

  # Copy nasalib to the Repos Path
  clone=subprocess.Popen('git clone https://github.com/nasa/pvslib.git '+repoPath+'/nasalib',shell=True)
  clone.communicate()[0]
  
  # Configure nasalib
  copy=subprocess.Popen('rsync -azh '+repoPath+'/nasalib/pvs-patches '+PVSPATH+'/nasalib/',shell=True)
  copy.communicate()[0]

  copy=subprocess.Popen('rsync -azh '+repoPath+'/nasalib/install-scripts '+PVSPATH+'/nasalib/',shell=True)
  copy.communicate()[0]
  
  os.chdir(PVSPATH+'/nasalib')
  install=subprocess.Popen('sh '+PVSPATH+'/nasalib/install-scripts',shell=True)
  install.communicate()[0]
  
  # Remove installation files
  delete=subprocess.Popen('rm -rf pvslm-install',shell=True)
  delete.communicate()[0]
  
  delete=subprocess.Popen('rm -rf pvslm.py',shell=True)
  delete.communicate()[0]

  delete=subprocess.Popen('rm -rf nasalib.list',shell=True)
  delete.communicate()[0]
  
  print 'PVS Library Manager has been successfully configured. Thanks!'
except:
  print 'Something went wrong. Please try again.'
