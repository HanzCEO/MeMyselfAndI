import src.utils
import src.items
from src.Environment import generate_random_environment
from src.Player import Player

player = Player()
environment = generate_random_environment()

player.set_environment(environment)

# TODO: Move META_ACTIONS variable to .src.MetaActions
META_ACTIONS = {
	"!inventory": lambda x: player.inventory_dialog()
}

while True:
	player.print()
	player.get_biome().print()
	inp = input("->] ")

	# TODO: Get terminal height
	print("\n" * 100)
	print("#" * 25)

	if inp in META_ACTIONS.keys():
		META_ACTIONS[inp](player)
	else:
		player.act(inp)

	environment.mother_nature_turn()
