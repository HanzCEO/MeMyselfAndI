import random
from ..Biome import Biome
from ..utils.print import vprint

# Lore: Riverside camp
def camp_generate(rng):
	biom = Camp()
	return biom

class Camp(Biome):
	def __init__(self):
		super().__init__('camp', 27)

		self.resource['wood'] = 50
		self.resource['water'] = 10000
		self.resource['animal'] = 3
		self.resource['corned'] = 5

	def act(self, player, stage, inp):
		super().act(player, stage, inp)
		if inp == "w":
			# TODO: Difficulty depends on level and daytime
			if player.energy < 20:
				print("[!] You don't have enough energy (min. 20)")
				return 'overview'

			reward = random.choices([0, 1, 2], weights=[2, 2, 1])[0]

			if self.resource['wood'] - reward >= 0 and reward > 0:
				# Stash wood to player
				from ..items.Wood import Wood
				for i in range(reward):
					if not player.stash(Wood()):
						print("[.] Not enough inventory space.")
						return 'overview'
					else:
						print(f"[+] +1 Wood")
				self.resource['wood'] -= reward
			elif reward == 0:
				print("[.] No wood in this so-called forest?? 0 wood.")

			# Energy consumption
			# TODO: More energy used when summer
			# wenomechainsama

			player.hydration -= vprint("[.] -{0} Hydration", random.randint(5, 10))[0]
			player.energy -= vprint("[.] -{0} Energy", random.randint(5, 20))[0]
			return 'overview'
		elif inp == "b":
			bottles = player.search_items_index_by_name("empty-bottle")
			if len(bottles) == 0:
				print("[.] You don't have any empty bottle")
				return 'overview'

			from ..items.WaterBottle import WaterBottle
			for index in bottles:
				del player.inventory[index]
				if not player.stash(WaterBottle()):
					print("[!] Not enough inventory for the water bottle")
		elif inp == "f":
			if player.energy < 20:
				print("[!] You don't have enough energy (min. 20)")
				return 'overview'

			if self.resource['corned'] > 0:
				# 20% Got corned beef
				if random.choices([0, 1], weights=[4, 1])[0] == 1:
					from ..items.CornedBeef import CornedBeef
					if not player.stash(CornedBeef()):
						print("[!] Not enough inventory, corned beef returned.")
					else:
						self.resource['corned'] -= 1
						print("[+] +1 Corned beef")

					return 'overview'

			print("[.] You don't find anything interesting.")
			return 'overview'
		elif inp == "h":
			if self.resource['animal'] <= 0:
				print("[.] You found nothing.")
				return 'overview'
			if player.energy < 30:
				print("[!] You are too tired. (min. 30 energy)")
				return 'overview'
			# TODO: Willpower??
			if random.choices([0, 1], weights=[19, 1])[0] == 1:
				print("[.] You just don't want to do it.")
				return 'overview'

			if random.choices([0, 1], weights=[4, 1])[0] == 1:
				# TODO: Animal could be boar, deer, etc. Just display name
				print("[+] You traced an animal. +1 Raw Meat")
				# Raw meat, lets go who cares
				from ..items.RawMeat import RawMeat
				if not player.stash(RawMeat()):
					print("[!] Not enough space. Raw meat vaporized somehow")

				# No matter what, animal has been hunted you know?
				self.resource['animal'] -= 1

	def print(self):
		super().print()

		print("w - Collect wood")
		print("b - Fill water bottles")
		print("f - Find something interesting")
		print("h - Trace animal footprint and hunt them")
