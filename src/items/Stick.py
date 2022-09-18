from ..Item import Item

# Name: Stick
# Weight: 0.1kg
class Stick(Item):
	def __init__(self):
		super().__init__('stick', 0.4)

	def detail_dialog(self):
		print("STICK")
		print("-" * 25)
		print("The hand of a dead tree.")
		print()
		print("Material")

		print("t - Throw")
		print("q - Quit this dialog")
		inp = input("->] ")

		if inp == "t":
			return 'throw'
		return False
