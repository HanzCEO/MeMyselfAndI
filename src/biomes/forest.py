import random
from ..Biome import Biome
from ..utils.print import vprint, log

# Lore: Just a forest
def forest_generate(rng):
	biom = Forest()
	return biom

class Forest(Biome):
	def __init__(self):
		super().__init__('forest', 27)

		self.resource['wood'] = random.randint(5, 10)
		self.resource['stick'] = random.randint(5, 20)
		self.resource['animal'] = random.randint(0, 2)
		self.resource['berry'] = random.randint(0, 3)

		self.commands.append("w - Search for wood")
		self.commands.append("f - Find something interesting")
		self.commands.append("h - Trace animal footprint and hunt them")

	def act(self, player, stage, inp):
		super().act(player, stage, inp)
		if inp == "w":
			# TODO: Difficulty depends on level and daytime
			if player.energy < 20:
				log("[!] You don't have enough energy (min. 20)")
				return 'overview'

			wood = random.choices([False, True], weights=[2, 1])[0]
			reward = random.choices([0, 1, 2], weights=[2, 2, 1])[0]

			if wood and self.resource['wood'] - reward >= 0 and reward > 0:
				# Stash wood to player
				from ..items.Wood import Wood
				for i in range(reward):
					if not player.stash(Wood()):
						log("[.] Not enough inventory space.")
						# TODO: Fix hydration not consumed like this
						return 'overview'
					else:
						log(f"[+] +1 Wood")
				self.resource['wood'] -= reward
			elif not wood and self.resource['stick'] - reward >= 0 and reward > 0:
				# Stash stick to player
				from ..items.Stick import Stick
				for i in range(reward):
					if not player.stash(Stick()):
						log("[.] Not enough inventory space.")
						# TODO: Fix hydration not consumed like this
						# IDEA: self.resource['wood'] -= rward should be -= 1
						return 'overview'
					else:
						log(f"[+] +1 Stick")
				self.resource['stick'] -= reward
			elif reward == 0:
				log("[.] No wood in this so-called forest?? 0 wood.")

			# Energy consumption
			# TODO: More energy used when summer
			# wenomechainsama

			player.hydration -= vprint("[.] -{0} Hydration", random.randint(5, 10))[0]
			player.energy -= vprint("[.] -{0} Energy", random.randint(5, 20))[0]
			return 'overview'
		elif inp == "f":
			if player.energy < 20:
				log("[!] You don't have enough energy (min. 20)")
				return 'overview'

			if self.resource['berry'] > 0:
				# 20% Got berry
				if random.choices([0, 1], weights=[4, 1])[0] == 1:
					from ..items.ForestBerry import ForestBerry
					if not player.stash(ForestBerry()):
						log("[!] Not enough inventory, forest berry returned.")
					else:
						self.resource['berry'] -= 1
						log("[+] +1 Forest berry")

					player.hydration -= vprint("[.] -{0} Hydration", random.randint(5, 10))[0]
					player.energy -= vprint("[.] -{0} Energy", random.randint(5, 20))[0]
					return 'overview'

			log("[.] You don't find anything interesting.")
			player.hydration -= vprint("[.] -{0} Hydration", random.randint(5, 10))[0]
			player.energy -= vprint("[.] -{0} Energy", random.randint(5, 20))[0]
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

			if random.choices([0, 1], weights=[9, 1])[0] == 1:
				# TODO: Animal could be boar, deer, etc. Just display name
				log("[+] You hunted an animal. +1 Raw Meat")
				# Raw meat, lets go who cares
				from ..items.RawMeat import RawMeat
				if not player.stash(RawMeat()):
					log("[!] Not enough space. Raw meat vaporized somehow")

				# No matter what, animal has been hunted you know?
				self.resource['animal'] -= 1

	def print(self):
		super().print()
