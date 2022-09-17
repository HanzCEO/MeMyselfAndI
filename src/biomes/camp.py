import random
from ..Biome import Biome
from ..utils.print import vprint, log
from ..utils.ui import term

# Lore: Riverside camp
def camp_generate(rng):
	biom = Camp()
	return biom

class Camp(Biome):
	def __init__(self):
		super().__init__('camp', 27, color=term.orange4_on_palegreen3)

		self.resource['wood'] = 50
		self.resource['water'] = 10000
		self.resource['animal'] = 3
		self.resource['corned'] = 5

	def act(self, player, stage, inp):
		super().act(player, stage, inp)
		if inp == "w":
			# TODO: Difficulty depends on level and daytime
			if player.energy < 20:
				log("[!] You don't have enough energy (min. 20)")
				return 'overview'

			reward = random.choices([0, 1, 2], weights=[2, 2, 1])[0]

			if self.resource['wood'] - reward >= 0 and reward > 0:
				# Stash wood to player
				from ..items.Wood import Wood
				for i in range(reward):
					if not player.stash(Wood()):
						log("[.] Not enough inventory space.")
						return 'overview'
					else:
						log(f"[+] +1 Wood")
				self.resource['wood'] -= reward
			elif reward == 0:
				log("[.] No wood in this so-called forest?? 0 wood.")

			# Energy consumption
			# TODO: More energy used when summer
			# wenomechainsama

			player.hydration -= vprint("[.] -{0} Hydration", random.randint(5, 10))[0]
			player.energy -= vprint("[.] -{0} Energy", random.randint(5, 20))[0]
			return 'overview'
		elif inp == "b":
			bottles = player.search_items_index_by_name("empty-bottle")
			if len(bottles) == 0:
				log("[.] You don't have any empty bottle")
				return 'overview'

			from ..items.WaterBottle import WaterBottle
			for index in bottles:
				del player.inventory[index]
				if not player.stash(WaterBottle()):
					log("[!] Not enough inventory for the water bottle")
		elif inp == "f":
			if player.energy < 20:
				log("[!] You don't have enough energy (min. 20)")
				return 'overview'

			if self.resource['corned'] > 0:
				# 20% Got corned beef
				if random.choices([0, 1], weights=[4, 1])[0] == 1:
					from ..items.CornedBeef import CornedBeef
					if not player.stash(CornedBeef()):
						log("[!] Not enough inventory, corned beef returned.")
					else:
						self.resource['corned'] -= 1
						log("[+] +1 Corned beef")

					return 'overview'

			log("[.] You don't find anything interesting.")
			return 'overview'
		elif inp == "h":
			if self.resource['animal'] <= 0:
				log("[.] You found nothing.")
				return 'overview'
			if player.energy < 30:
				log("[!] You are too tired. (min. 30 energy)")
				return 'overview'
			# TODO: Willpower??
			if random.choices([0, 1], weights=[19, 1])[0] == 1:
				log("[.] You just don't want to do it.")
				return 'overview'

			if random.choices([0, 1], weights=[4, 1])[0] == 1:
				# TODO: Animal could be boar, deer, etc. Just display name
				log("[+] You traced an animal. +1 Raw Meat")
				# Raw meat, lets go who cares
				from ..items.RawMeat import RawMeat
				if not player.stash(RawMeat()):
					log("[!] Not enough space. Raw meat vaporized somehow")

				# No matter what, animal has been hunted you know?
				self.resource['animal'] -= 1

	def print(self):
		super().print()

		log("w - Collect wood")
		log("b - Fill water bottles")
		log("f - Find something interesting")
		log("h - Trace animal footprint and hunt them")
