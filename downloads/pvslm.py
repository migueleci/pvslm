#!/usr/bin/env python

import argparse
import sys
import subprocess
import os
from os import listdir

PVSLM='pvslmPath'
PVSLMSRC='pvslmSrc'
PVSLMREP='pvslmRep'

class PVSLMParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n\n' % message)
        self.print_help()
        sys.exit(2)

def main():
	#parser = argparse.ArgumentParser(version='PVS Library Manager 1.0',prog='PVS Library Manager')
	parser = PVSLMParser(version='PVS Library Manager 1.0',prog='PVS Library Manager')
	subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')

	# Create parser for the sources
	src = subparsers.add_parser('src', help='Source manager help')
	# Optional arguments
	src.add_argument("-a", "--add", action="store_true", help="Add a new source")
	src.add_argument("-m", "--modify", action="store_true", help="Modify an existing source")
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
	pkg.add_argument("-f", "--info", action="store_true", help="Get information about a package")
	# Positional arguments
	pkg.add_argument("name", type=str, help="Name of the package")
	
	args = parser.parse_args()
	if args.subparser_name=='src':
		if args.add:
			if args.description!=None and args.url!=None:
				name=args.name
				desc=args.description
				url=args.url
				try:
					files=listdir(PVSLMSRC)
					sources =[None]
					for f in files: 						
						if os.path.splitext(f)[1]=='.list': 
							sources.append(os.path.splitext(f)[0])
					if name not in sources:
						file_src=PVSLMSRC+'/'+name+'.list'
						content='"URL = '+url+'\nName = '+name+'\nDescription = '+desc+'"'
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
				sources =[None]
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
				sources =[None]
				for f in files: 
					if os.path.splitext(f)[1]=='.list': 
						sources.append(os.path.splitext(f)[0])
				if name in sources:
					files=listdir(PVSLMREP)
					repos =[None]
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
			try:
				files=listdir(PVSLMSRC)
				sources =[None]
				for f in files: 
					if os.path.splitext(f)[1]=='.list': 
						sources.append(os.path.splitext(f)[0])
				if name in sources:
					files=listdir(PVSLMREP)
					repos =[None]
					for f in files: 
						if(os.path.isdir(PVSLMREP+'/'+f)): 
							repos.append(f)
					if name in repos:
						src=open(PVSLMSRC+'/'+name+'.list')
						url=src.readline()
						url=url[6:-1]
						os.chdir(PVSLMREP+'/'+name)
						clone=subprocess.Popen('git fetch '+url,shell=True)
						clone.communicate()[0]
						print "Repository "+name+" updated successfully"
					else:
						print "The repository "+name+" does not exists. Created it first"
				else:
					print "The source your trying to update does not exist"
			except:
				print "Something went wrong. Please check the arguments and try again"
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
			print 'Under development.'
		elif args.update:
			print 'Under development.'
		elif args.delete:
			print 'Under development.'
		elif args.info:
			print 'Under development.'
	
		
if __name__=='__main__':
	main()	
