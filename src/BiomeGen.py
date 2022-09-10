import random
print("[*] Loading OpenSimplex")
from opensimplex import OpenSimplex
print("[i] Done.")

from .Biome import Biome
from .biomes import *

BIOME_GENERATORS = dict(
	swamp=swamp_generate,
	forest=forest_generate,
	grass=grass_generate,
	road=road_generate,
	lake=lake_generate,
	hill=hill_generate,
	savana=savana_generate,
	camp=camp_generate
)

# TODO: Variable BIOME_NOISE between level difficulty
'''BIOME_NOISE = dict(
	swamp=(-1.0, -0.5),
	forest=(-0.5, -0.2),
	grass=(-0.2, 0.0),
	road=(0.0, 0.1),
	lake=(0.1, 0.3),
	hill=(0.3, 0.4),
	savana=(0.4, 0.7),
	camp=(0.7, 1.0)
)'''
BIOME_NOISE = dict(camp=(-1.0, 1.0))

# Only for generation
class RNG(object):
	def __init__(self, seed=0):
		self.rng = random.Random()
		self.rng.seed(seed, version=2)

		self.noise = OpenSimplex(self.rng.randint(0, 10000000))

		# Storing purpose
		self.seed = seed

	def getxy(self, x, y):
		noise = self.noise.noise2(x, y)

		for k, v in BIOME_NOISE.items():
			if noise >= v[0] and noise <= v[1]:
				return BIOME_GENERATORS[k](self)

		return None
