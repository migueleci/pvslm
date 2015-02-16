#!/usr/bin/env python
import optparse
import os
import re
import subprocess
import shlex
from subprocess import check_output 
from sys import stdin
from os import listdir

def main():
	usage="usage: %prog [options] arg1 arg2 "
	p = optparse.OptionParser(usage=usage,version="PVS Library Manager 1.0",prog='PVS Library Manager')
	p.add_option('-a',	'--add-src'		,dest='add_src'	,action='store_true' 	,help="Create a new repository source, given its NAME and URL")
	p.add_option('-m',	'--modify-src'	,dest='mdf_src'	,action='store_true'	,help="Modify a repository source")
	p.add_option('-e',	'--delete-src'	,dest='del_src'	,action='store_true'	,help="Delete a repository source")
	p.add_option('-c',	'--create-repo'	,dest='cre_rep'	,action='store_true'	,help="Create a new repository, based on a source")
	p.add_option('-x',	'--update-repo'	,dest='upd_rep'	,action='store_true'	,help="Update a repository")
	p.add_option('-r',	'--delete-repo'	,dest='del_rep'	,action='store_true'	,help="Delete a repository")
	p.add_option('-i',	'--install'		,dest='ins_pkg'	,action='store_true'	,help="Install a new package and all its dependencies")
	p.add_option('-u',	'--update'		,dest='upd_pkg'	,action='store_true'	,help="Update a package and all its dependecies")
	p.add_option('-d',	'--delete'		,dest='del_pkg'	,action='store_true'	,help="Delete a package")
	p.add_option('-g',	'--info'		,dest='inf_pkg'	,action='store_true'	,help="Show all the information about a package")
	
	options, args = p.parse_args()
	print 'Welcome to PVS Library Manager'
	if options.add_src and len(args)==2:
		try :
			name=args[0]
			url=args[1]
			path=check_output(['printenv','PVSLM'])
			path = path[:-1]
			files=listdir(path)
			sources =[None]
			for f in files: sources.append(os.path.splitext(f)[0])
			if name not in sources:
				file_src=path+'/'+name+'.list'
				arg=subprocess.Popen(['sudo echo '+url+' > '+file_src]
									 ,shell=True, stdin=subprocess.PIPE
									 ,stdout=subprocess.PIPE
									 ,stderr=subprocess.PIPE)
				print "Source "+name+" added successfully"
			else:
				print "The source already exist, try to modify it."
		except :
			print "Please check the name and url, and try again"
	elif options.mdf_src and len(args)==2:
		try:
			name=args[0]
			url=args[1]
			path=check_output(['printenv','PVSLM'])
			path = path[:-1]
			files=listdir(path)
			sources =[None]
			for f in files: sources.append(os.path.splitext(f)[0])
			if name in sources:
				file_src=path+'/'+name+'.list'
				arg=subprocess.Popen(['sudo echo '+url+' > '+file_src]
									 ,shell=True, stdin=subprocess.PIPE
									 ,stdout=subprocess.PIPE
									 ,stderr=subprocess.PIPE)
				print "Source "+name+" modified successfully"
			else:
				print "The source your trying to modify does not exist"
		except:
			print "Please check the name and url, and try again"
	elif options.cre_rep and len(args)==1:
		try:
			name=args[0]
			path=check_output(['printenv','PVSLM'])
			path = path[:-1]
			files=listdir(path)
			sources =[None]
			for f in files: sources.append(os.path.splitext(f)[0])
			if name in sources:
				repos =[None]
				for f in files: 
					if(os.path.isdir(path+'/'+f)): 
						repos.append(f)
				if name not in repos:
					src=open(path+'/'+name+'.list')
					url=src.readline()
					url=url[:-1]
					clone=shlex.split('sudo git clone '+url+' '+path+'/'+name)
					arg=subprocess.Popen(clone,stdout=subprocess.PIPE)
					print arg.communicate("n\n")[0]
					print "Repository "+name+" created successfully"
				else:
					print "The repository is already created, try to update it"
			else:
				print "The source your trying to create does not exist"
		except:
			print "Please check the repository name and try again"
	else: print "Something went wrogn, please try again"
	
if __name__=='__main__':
	main()
	
