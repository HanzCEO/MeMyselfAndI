import random
from ..Item import Item
from .utils.math import clamp

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
		print("+ 30-40 Hydration")

		print("c - Consume")
		print("q - Quit this dialog")
		inp = input("->] ")

		if inp == "q":
			return False
		elif inp != "c":
			return False

		# Consume
		return "consume"

	def consume(self, player):
		delta = clamp(player.hydration + random.randint(30, 40), 0, 100) - player.hydration
		player.hydration += delta
		print(f"[$] You consumed a Water Bottle (+{delta} hydration)")

		return "delete"
