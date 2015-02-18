import argparse

PVSLM='?'
PVSLMSRC='?'
PVSLMREP='?'

def main():
	
	parser = argparse.ArgumentParser(version='PVS Library Manager 1.0',prog='PVS Library Manager')
	subparsers = parser.add_subparsers(help='sub-command help')

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
	src.add_argument("description", type=str, help="Descriprion of a source")
	src.add_argument("url", type=str, help="URL of a source")
	
	# Create parser for the packages
	pkg = subparsers.add_parser('pkg', help='Package manager help')
	# Optional arguments
	pkg.add_argument("-i", "--install", action="store_true", help="Install a package and all its dependecies")
	pkg.add_argument("-u", "--update", action="store_true", help="Update a package and all its dependecies")
	pkg.add_argument("-d", "--delete", action="store_true", help="Delete a package")
	pkg.add_argument("-f", "--info", action="store_true", help="Get information about a package")
	# Positional arguments
	pkg.add_argument("name", type=str, help="Name of the package")
	
	args=parser.parse_args()
	
if __name__=='__main__':
	main()	
