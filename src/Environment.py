import random
from .BiomeGen import RNG

ENV_SIZES = dict(
	tiny=(4, 4), # Only for test
	small=(7, 7),
	medium=(10, 10),
	big=(20, 20),
	huge=(40, 40)
)

def generate_random_environment(level='easy', size='tiny'):
	return Environment(level, size)

class Environment(object):
	def __init__(self, level='easy', size='tiny'):
		level = level.lower()
		size = size.lower()

		self.size = ENV_SIZES[size]

		biomerng = RNG(random.randint(0, 100000))
		self.biomes = list()
		for y in range(ENV_SIZES[size][1]):
			self.biomes.append(list())
			for x in range(ENV_SIZES[size][0]):
				self.biomes[y].append(biomerng.getxy(x, y))

	def get_biome(self, x, y):
		# (0, 0) must be the center
		centerX = self.size[0] // 2
		centerY = self.size[1] // 2

		# Normalize
		x += centerX
		y += centerY

		try:
			return self.biomes[y][x]
		except IndexError:
			return None

	def mother_nature_turn(self):
		# TODO: def mother_nature_turn()
		pass
