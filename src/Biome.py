import random
from .utils.print import vprint
from .utils.math import clamp

class Biome(object):
	def __init__(self, name='forest', heat=25):
		self.name = name.title()
		self.heat = heat

		# For developers who wants to create new biome:
		# This variable is not limited to Item name,
		# it could be more general like: Animal.
		# Then, you could use RNG to determine which Item
		# will be received by the player inside the .act() method
		self.resource = dict(
			wood=5,
			water=2
		)

	def print(self):
		print()
		print("=" * 25)
		print(f"{self.name} ({self.heat}{chr(176)}C)")
		print("r - Rest for a moment")
		print("s - Sleep. Yes.")

	def act(self, player, stage, inp):
		if inp == "r":
			player.hydration -= vprint("[-] -{0} Hydration", random.randint(0, 10))[0]
			player.hunger -= vprint("[-] -{0} Hunger", random.randint(5, 10))[0]
			player.energy += vprint("[+] +{0} Energy", random.randint(20, 50))[0]
		elif inp == "s":
			player.hydration -= vprint("[-] -{0} Hydration", random.randint(0, 20))[0]
			player.hunger -= vprint("[-] -{0} Hunger", random.randint(0, 20))[0]
			player.energy += vprint("[+] +{0} Energy", random.randint(100, 200))[0]

		player.hydration = clamp(player.hydration, 0, 100)
		player.hunger = clamp(player.hunger, 0, 100)
		player.energy = clamp(player.energy, 0, 100)
