import src.utils.ui as ui
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

	ui.clear()

	if inp in META_ACTIONS.keys():
		META_ACTIONS[inp](player)
	else:
		player.act(inp)

	environment.mother_nature_turn()
