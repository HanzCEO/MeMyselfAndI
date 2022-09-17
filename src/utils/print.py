logs = list()

'''
Extends Python's print
to print and rturn values
'''
def vprint(s, *arg, **kwargs):
	if not kwargs.get('log', False):
		print(s.format(*arg), **kwargs)
	else:
		log(s.format(*arg), **kwargs)
	return arg

def log(s, **kwargs):
	logs.append((s, kwargs))

def flush_logs():
	for s, kw in logs:
		print(s, **kw)
