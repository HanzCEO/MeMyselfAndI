import random
from ..Item import Item
from ..utils.math import clamp

# Name: Bottle
# Weight: 0.05kg
class WaterBottle(Item):
	def __init__(self):
		super().__init__('bottle', 0.05)

	def detail_dialog(self):
		print("BOTTLE")
		print("-" * 25)
		print("An empty liquid container.")
		print()
		print("Material")
		print()

		print("t - Throw")
		print("q - Quit this dialog")
		inp = input("->] ")

		if inp == "t":
			return 'throw'
		return False
