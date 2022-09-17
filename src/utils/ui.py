from blessed import Terminal

term = Terminal()

def clear():
	print(term.home + term.clear, end="")

def center(s):
	print(term.center(s))

def middle(offset):
	print(term.move_y(term.height // 2 + offset), end="")

def progress_bar(on='#', off='-', maxval=10, value=3):
	return (on * value).ljust(off, maxval)
