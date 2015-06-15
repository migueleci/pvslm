#!/usr/bin/env python

import argparse
import sys
import subprocess
import re
import os
from os import listdir

PVSPATH='pvsPath'
PVSLM='pvslmPath'
PVSLMSRC='pvslmSrc'
PVSLMREP='pvslmRep'

class PVSLMParser(argparse.ArgumentParser):
  def error(self, message):
    sys.stderr.write('error: %s\n\n' % message)
    self.print_help()
    sys.exit(2)

global listed

def listdep(name, pkgs, pkgs_name):
  if(name in pkgs_name):
    src=open(pkgs[pkgs_name.index(name)]+'/pvsbin/top.dep')
    for line_dep in src.readlines():
      if line_dep.find("/")>0:
        pack=line_dep[0:line_dep.find("/")]
        if (pack not in listed):
          if(pack in pkgs_name):
            listed.append(pack)
          listdep(pack,pkgs,pkgs_name)
        line_dep=src.readline()

def listAlldep(name, pkgs, pkgs_name):
  pend_pkg=[val for val in pkgs_name if val not in listed]
  for p in pend_pkg:
    src=open(pkgs[pkgs_name.index(p)]+'/pvsbin/top.dep')
    for line_dep in src.readlines():
      finded=False
      if line_dep.find("/")>0 and not finded:
        pack=line_dep[0:line_dep.find("/")]
        if (pack in listed):
            listed.append(p)
            finded=True
            listAlldep(p, pkgs, pkgs_name)
        line_dep=src.readline()
  
def update_library(name):
  try:
    files=listdir(PVSLMSRC)
    sources =[]
    for f in files: 
      if os.path.splitext(f)[1]=='.list': 
        sources.append(os.path.splitext(f)[0])
    if name in sources:
      files=listdir(PVSLMREP)
      repos =[]
      for f in files: 
        if(os.path.isdir(PVSLMREP+'/'+f)): 
          repos.append(f)
      if name in repos:
        src=open(PVSLMSRC+'/'+name+'.list')
        url=src.readline()
        url=url[6:-1]
        os.chdir(PVSLMREP+'/'+name)
        clone=subprocess.Popen('git pull '+url,shell=True)
        clone.communicate()[0]
        print "Repository "+name+" updated successfully"
      else:
        print "The repository "+name+" does not exists. Created it first"
    else:
      print "The source your trying to update does not exist"
  except:
    print "Something went wrong. Please check the arguments and try again"

def main():
  #parser = argparse.ArgumentParser(version='PVS Library Manager 1.0',prog='PVS Library Manager')
  parser = PVSLMParser(version='PVS Library Manager 1.0',prog='PVS Library Manager')
  subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')
  
  # Create parser for the sources
  src = subparsers.add_parser('src', help='Source manager help')
  # Optional arguments
  src.add_argument("-a", "--add", action="store_true", help="Add a new source")
  src.add_argument("-d", "--delete", action="store_true", help="Delete an existing source")
  src.add_argument("-c", "--create", action="store_true", help="Create a new repository")
  src.add_argument("-u", "--update", action="store_true", help="Update an existing repository")
  src.add_argument("-r", "--remove", action="store_true", help="Remove an existing repository")
  # Positional arguments
  src.add_argument("name", type=str, help="Name of the repositoy or source") 
  src.add_argument("description", type=str, help="Descriprion of a source",nargs='?') # Optional
  src.add_argument("url", type=str, help="URL of a source",nargs='?') # Optional
  
  # Create parser for the packages
  pkg = subparsers.add_parser('pkg', help='Package manager help')
  # Optional arguments
  pkg.add_argument("-i", "--install", action="store_true", help="Install a package and all its dependecies")
  pkg.add_argument("-u", "--update", action="store_true", help="Update a package and all its dependecies")
  pkg.add_argument("-d", "--delete", action="store_true", help="Delete a package")
  pkg.add_argument("-l", "--list", action="store_true", help="nargs = List available libraries\nlibrary = list all its packages\nlibrary@package = list all dependencies of the package")
  # Positional arguments
  pkg.add_argument("library@package", type=str, help="name of the package and its library",nargs='?') # Optional
  
  global listed
  
  args = parser.parse_args()
  if args.subparser_name=='src':
    if args.add:
      if args.description!=None and args.url!=None:
        name=args.name
        desc=args.description
        url=args.url
        try:
          files=listdir(PVSLMSRC)
          sources =[]
          for f in files:             
            if os.path.splitext(f)[1]=='.list': 
              sources.append(os.path.splitext(f)[0])
          if name not in sources:
            file_src=PVSLMSRC+'/'+name+'.list'
            content='"URL = '+url+'\nName = '+name+'\nDescription = '+desc+'\nEnable = Yes"'
            crt=subprocess.Popen('echo '+content+' > '+file_src,shell=True)
            crt.communicate()[0]
            print "Source "+name+" added successfully"
          else:
            print "The source already exist, try to modify it."
        except :
          print "Something went wrong. Please check the arguments and try again"
      else:
        print "Please include the description and url"
    elif args.modify:
      print 'Under development.'
    elif args.delete:
      name=args.name
      try:
        files=listdir(PVSLMSRC)
        sources =[]
        for f in files: 
          if os.path.splitext(f)[1]=='.list': 
            sources.append(os.path.splitext(f)[0])
        if name in sources:
          crt=subprocess.Popen('rm -rf '+PVSLMSRC+'/'+name+'.list',shell=True)
          crt.communicate()[0]
          print "Source "+name+" deleted successfully"
        else:
          print 'The source does not exist.'
      except:
        print "Something went wrong. Please check the arguments and try again"
    elif args.create:
      name=args.name
      try:
        files=listdir(PVSLMSRC)
        sources =[]
        for f in files: 
          if os.path.splitext(f)[1]=='.list': 
            sources.append(os.path.splitext(f)[0])
        if name in sources:
          files=listdir(PVSLMREP)
          repos =[]
          for f in files: 
            if(os.path.isdir(PVSLMREP+'/'+f)): 
              repos.append(f)
          if name not in repos:
            src=open(PVSLMSRC+'/'+name+'.list')
            url=src.readline()
            url=url[6:-1]
            clone=subprocess.Popen('git clone '+url+' '+PVSLMREP+'/'+name,shell=True)
            clone.communicate()[0]
            print "Repository "+name+" created successfully"
          else:
            print "The repository "+name+" is already created, try to update it."
        else:
          print "The source your trying to create does not exist"
      except:
        print "Something went wrong. Please check the arguments and try again"
    elif args.update:
      name=args.name
      update_library(name)
    elif args.remove:
      name=args.name
      try:
        files=listdir(PVSLMREP)
        repos =[None]
        for f in files: 
          if(os.path.isdir(PVSLMREP+'/'+f)): 
            repos.append(f)
        if name in repos:
          clone=subprocess.Popen('rm -rf '+PVSLMREP+'/'+name,shell=True)
          clone.communicate()[0]
          print "Repository "+name+" removed successfully"
        else:
          print "The repository "+name+" does not exists. Created first"
      except:
        print "Something went wrong. Please check the arguments and try again"
  else :
    if args.install:      
      val=[]
      if args.package!=None:
        val=re.split('@+',args.package)
      if len(val)!=2:
        print "Remeber to specify te library and package (library@package). Please try again"
        sys.exit()
      fpackage=val[1]
      flibrary=val[0]
      try:
        lpath=PVSLMREP+'/'+flibrary
        if(os.path.isdir(lpath)):
          files=listdir(lpath)
          pkgs=[]
          listed = []
          pkgs_name=[]
          for f in files:
            if(os.path.isdir(lpath+'/'+f+'/pvsbin')):
              pkgs.append(lpath+'/'+f)
              pkgs_name.append(f)
          if fpackage in pkgs_name:
            listed.append(fpackage)
            listdep(fpackage, pkgs, pkgs_name)
            listed.remove(fpackage)
            if len(listed)>0:
              listed=sorted(set(listed))
              print 'The package '+fpackage+' depends on:'
              print '\n'.join(str(p) for p in listed)
            else:
              print "The package "+fpackage+" has no dependencies"
            apr=raw_input('Would you like to install the package(s) (Y/N): ')
            if apr=='Y' or apr=='y':
              if(not os.path.isdir(PVSLM+'/'+flibrary)):
                create=subprocess.Popen('mkdir -p '+PVSPATH+'/'+flibrary,shell=True)
                create.communicate()[0]
              listed.append(fpackage)
              for l in listed:
                copy=subprocess.Popen('rsync -azh '+pkgs[pkgs_name.index(l)]+' '+PVSPATH+'/'+flibrary,shell=True)
                copy.communicate()[0]
              print "Package "+fpackage+" installed successfully"
          else:
            print "The package "+fpackage+" does not exist"
        else:
          print "The library "+flibrary+" does not exist"
      except:
        print "Something went wrong. Please check the arguments and try again"
    elif args.update:
      val=[]
      if args.package!=None:
        val=re.split('@+',args.package)
      if len(val)!=2:
        print "Remeber to specify te library and package (library@package). Please try again"
        sys.exit()
      fpackage=val[1]
      flibrary=val[0]
      try:
        lpath=PVSPATH+'/'+flibrary
        if(os.path.isdir(lpath)):
          files=listdir(lpath)
          pkgs=[]
          listed = []
          pkgs_name=[]
          for f in files:
            if(os.path.isdir(lpath+'/'+f+'/pvsbin')):
              pkgs.append(lpath+'/'+f)
              pkgs_name.append(f)
          if fpackage in pkgs_name:
            update_library(flibrary)
            listed.append(fpackage)
            listdep(fpackage, pkgs, pkgs_name)
            listed.remove(fpackage)
            if len(listed)>0:
              listed=sorted(set(listed))
              print 'The package '+fpackage+' depends on:'
              print '\n'.join(str(p) for p in listed)
            else:
              print "The package "+fpackage+" has no dependencies"
            apr=raw_input('Would you like to update the package(s) (Y/N): ')
            if apr=='Y' or apr=='y':
              if(not os.path.isdir(PVSLM+'/'+flibrary)):
                create=subprocess.Popen('mkdir -p '+lpath,shell=True)
                create.communicate()[0]
              listed.append(fpackage)
              for l in listed:
                copy=subprocess.Popen('rsync -azh '+pkgs[pkgs_name.index(l)]+' '+lpath,shell=True)
                copy.communicate()[0]
              print "The package "+fpackage+" has been updated successfully"
          else:
            print "The package "+fpackage+" is not installed"
        else:
          print "The library "+flibrary+" does not exist"
      except:
        print "Something went wrong. Please check the arguments and try again"
    elif args.delete:
      val=[]
      if args.package!=None:
        val=re.split('@+',args.package)
      if len(val)!=2:
        print "Remeber to specify te library and package (library@package). Please try again"
        sys.exit()
      fpackage=val[1]
      flibrary=val[0]
      try:
        lpath=PVSPATH+'/'+flibrary
        if(os.path.isdir(lpath)):
          files=listdir(lpath)
          pkgs=[]
          listed = []
          pkgs_name=[]
          for f in files:
            if(os.path.isdir(lpath+'/'+f+'/pvsbin')):
              pkgs.append(lpath+'/'+f)
              pkgs_name.append(f)
          if fpackage in pkgs_name:
            listed.append(fpackage)
            listAlldep(fpackage, pkgs, pkgs_name)
            listed.remove(fpackage)
            if len(listed)>0:
              listed=sorted(set(listed))
              print 'The package '+fpackage+' depends on:'
              print '\n'.join(str(p) for p in listed)
            else:
              print "The package "+fpackage+" has no dependencies"
            apr=raw_input('Would you like to remove the package(s) (Y/N): ')
            if apr=='Y' or apr=='y':
              listed.append(fpackage)
              for l in listed:
                delete=subprocess.Popen('rm -rf '+pkgs[pkgs_name.index(l)],shell=True)
                delete.communicate()[0]
              print "The package "+fpackage+" has been removed successfully"
          else:
            print "The package "+fpackage+" does not exist"
        else:
          print "The library "+flibrary+" does not exist"
      except:
        print "Something went wrong. Please check the arguments and try again"
    elif args.list:      
      val=[]
      if args.package!=None:
        val=re.split('@+',args.package)
      if len(val)==0:
        try:
          files=listdir(PVSLMREP)
          repos =[]
          for f in files: 
            if os.path.isdir(PVSLMREP+'/'+f):
              repos.append(f)
          print "You have configured the libraries:"
          print '\n'.join(str(p) for p in repos)
        except:
          print "Something went wrong. Please check the arguments and try again"
      elif len(val)==1:
        flibrary=val[0]
        try:
          lpath=PVSLMREP+'/'+flibrary
          if(os.path.isdir(lpath)):
            files=listdir(lpath)
            pkgs=[]
            pkgs_name=[]
            for f in files:
              if(os.path.isdir(lpath+'/'+f+'/pvsbin')):
                pkgs.append(lpath+'/'+f)
                pkgs_name.append(f)
            print 'The library '+flibrary+' has the packages:'
            print '\n'.join(str(p) for p in pkgs_name)
          else:
            print "The library "+flibrary+" does not exist"
        except:
          print "Something went wrong. Please check the arguments and try again"
      elif len(val)==2:
        fpackage=val[1]
        flibrary=val[0]
        try:
          lpath=PVSLMREP+'/'+flibrary
          if(os.path.isdir(lpath)):
            files=listdir(lpath)
            pkgs=[]
            listed = []
            pkgs_name=[]
            for f in files:
              if(os.path.isdir(lpath+'/'+f+'/pvsbin')):
                pkgs.append(lpath+'/'+f)
                pkgs_name.append(f)
            if fpackage in pkgs_name:
              listed.append(fpackage)
              listdep(fpackage, pkgs, pkgs_name)
              listed.remove(fpackage)
              if len(listed)>0:
                listed=sorted(set(listed))
                print 'The package '+fpackage+' depends on:'
                print '\n'.join(str(p) for p in listed)
              else:
                print "The package "+fpackage+" has no dependencies"
            else:
              print "The package "+fpackage+" does not exist"
          else:
            print "The library "+flibrary+" does not exist"
        except:
          print "Something went wrong. Please check the arguments and try again"
      else:
        print "Remeber to specify te library and package (library@package). Please try again"
        sys.exit()

if __name__=='__main__':
  main()  
