import random
from ..Item import Item
from ..utils.math import clamp

# Name: Water Bottle
# Weight: 0.2kg
class WaterBottle(Item):
	def __init__(self):
		super().__init__('water-bottle', 0.2)

	def detail_dialog(self):
		print("WATER BOTTLE")
		print("-" * 25)
		print("You like it, you survive with it.")
		print()
		print("Consumeable")
		print()
		print("+ 50-70 Hydration")

		print("t - Throw")
		print("c - Consume")
		print("q - Quit this dialog")
		inp = input("->] ")

		if inp == "q":
			return False
		elif inp == "t":
			return 'throw'
		elif inp != "c":
			return False

		# Consume
		return "consume"

	def consume(self, player):
		delta = clamp(player.hydration + random.randint(50, 70), 0, 100) - player.hydration
		player.hydration += delta
		print(f"[$] You consumed a Water Bottle (+{delta} hydration)")

		# Give back empty water bottle
		from .Bottle import Bottle
		ind = player.search_item_index_by_name(self.name)
		del player.inventory[ind]
		player.stash(Bottle())

		return True
