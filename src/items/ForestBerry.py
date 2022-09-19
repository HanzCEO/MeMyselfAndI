import random
from ..Item import Item
from ..utils.math import clamp

# Name: Forest Berry
# Weight: 0.05kg
class ForestBerry(Item):
	def __init__(self):
		super().__init__('forest-berry', 0.01)

	def detail_dialog(self):
		print("FOREST BERRY")
		print("-" * 25)
		print("Who knows if it is edible?.")
		print()
		print("Poisonus amongus")
		print()

		print("c - Consume")
		print("t - Throw")
		print("q - Quit this dialog")
		inp = input("->] ")

		if inp == "t":
			return 'throw'
		if inp == "c":
			return 'consume'
		return False

	def consume(self, player):
		player.health += vprint("[+] {0} health", 10)[0]
		player.hydration -= vprint("[-] {0} hydration", 5)[0]
		return 'delete'
