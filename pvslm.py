import argparse

def main():
	
	parser = argparse.ArgumentParser(version='PVS Library Manager 1.0',prog='PVS Library Manager')
	subparsers = parser.add_subparsers(help='sub-command help')

	# create the parser for the "a" command
	pkg = subparsers.add_parser('pkg', help='Package manager help')
	pkg.add_argument('bar', type=int, help='bar help')

	# create the parser for the "b" command
	src = subparsers.add_parser('src', help='Source manager help')
	src.add_argument('--baz', choices='XYZ', help='baz help')

	# parse some argument lists
	#parser.parse_args(['a', '12'])
	#Namespace(bar=12, foo=False)
	#parser.parse_args(['--foo', 'b', '--baz', 'Z'])
	#Namespace(baz='Z', foo=True)
	
	args=parser.parse_args()
	
if __name__=='__main__':
	main()	
