from ..Item import Item

# Name: Wood
# Weight: 0.4kg
class Wood(Item):
	def __init__(self):
		super().__init__('wood', 0.4)

	def detail_dialog(self):
		print("WOOD")
		print("-" * 25)
		print("The body of a dead tree.")
		print()
		print("Material")
		print()

		print("t - Throw")
		print("q - Quit this dialog")
		inp = input("->] ")

		if inp == "q":
			return False
		elif inp == "t":
			return 'throw'
