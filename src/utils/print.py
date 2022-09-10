
'''
Extends Python's print
to print and rturn values
'''
def vprint(s, *arg, **kwargs):
	print(s.format(*arg), **kwargs)
	return arg
