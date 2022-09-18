from .utils.print import vprint
from .utils.ui import progress_bar, clear, term, middle, center
from .Biome import Biome

class Player(object):
	def __init__(self):
		self.environment = None
		self.position = [0, 0]
		self.stage = 'menu'

		self.inventory = list()
		self.inventory_capacity = 10 # kg

		# Bro its just a game, chill
		self.health = 100
		self.hydration = 100
		self.hunger = 100
		self.energy = 100
		self.body_heat = 100

		from .items.WaterBottle import WaterBottle
		self.stash(WaterBottle())
		self.stash(WaterBottle())
		self.stash(WaterBottle())

	def print(self):
		print()
		print("PLAYER STAT")
		print("=" * 25)
		print(f"Health   : {progress_bar(value=(self.health // 10))} {self.health}%")
		print(f"Hydration: {progress_bar(value=(self.hydration // 10))} {self.hydration}%")
		print(f"Hunger   : {progress_bar(value=(self.hunger // 10))} {self.hunger}%")
		print(f"Energy   : {progress_bar(value=(self.energy // 10))} {self.energy}%")
		print(f"Body Heat: {progress_bar(value=(self.body_heat // 10))} {self.body_heat}%")

	def set_environment(self, env):
		self.environment = env

	def get_biome(self):
		return self.environment.get_biome(*self.position)

	def inventory_dialog(self):
		count = dict()
		for item in self.inventory:
			if count.get(item.name) is None:
				count[item.name] = dict(amount=0, weight=item.weight)

			count[item.name]['amount'] += 1

		i = 1
		for k, v in count.items():
			k = k.replace('_', ' ').title()
			print(f"[{i}] {k} ({v['amount']}x) - {round(v['weight'] * v['amount'], 2)}kg")
			i += 1

		# Actions
		print("q - Quit dialog")
		innp = 'i'
		while not innp.isnumeric():
			innp = input("->] ")
			if not innp.isnumeric() and innp != "q":
				print("[!] Input invalid")
			elif innp == "q":
				return False
			else:
				tkeys = list(count.keys())
				if (int(innp)-1) >= len(tkeys) or (int(innp)-1) < 0:
					print("[!] Item number invalid")
					continue

				selectedName = tkeys[int(innp)-1]
				selected = self.search_item_by_name(selectedName)
				break

		# Item not found
		if selected is None:
			print(f"[!] Unexpected! Item \"{selected.display_name}\" not found.")
			return False
		else:
			itemAct = selected.detail_dialog()

			# Throw item
			if itemAct == "throw":
				# Items throwed will be store in the current biome
				index = self.search_item_index_by_name(selected.name)
				self.throw_item(index, self.get_biome())
				# Finally remove the item from our inventory
				itemAct = "delete"


			# Special interaction with item; consume
			if itemAct == "consume":
				# Not consume player bruh, the API has weird application
				itemAct = selected.consume(self)
				# Consumeable has the ability to delete themselve by
				# returning the value "delete"

			# Item deleted
			# This act will be returned by the dialog either when consumed or else.
			if itemAct == "delete":
				index = self.search_item_index_by_name(selected.name)
				if index is None:
					print("[!] Unexpected! Item not found while searching by index.")
				else:
					del self.inventory[index]
					print(f"[i] {selected.name} dropped on current biome")

	def search_items_by_name(self, name):
		items = list()
		for item in self.inventory:
			if item.name == name:
				items.append(item)

		return items

	def search_item_by_name(self, name):
		for item in self.inventory:
			if item.name == name:
				return item

		return None

	def search_items_index_by_name(self, name):
		indexes = list()

		for i, item in enumerate(self.inventory):
			if item.name == name:
				indexes.append(i)

		return indexes

	def search_item_index_by_name(self, name):
		for i, item in enumerate(self.inventory):
			if item.name == name:
				return i

		return None

	def get_inventory_weight(self):
		weight = 0.00
		for item in self.inventory:
			weight += item.weight

		return round(weight, 2)

	def stash(self, item):
		# Check if we have more inventory
		# Will there be rounding error? Yes.
		# TODO: Player.inventory_capacity should be treated like 'money' variable
		if round(self.get_inventory_weight() + item.weight, 2) > self.inventory_capacity:
			return False
		else:
			self.inventory.append(item)
			return True

	def throw_item(self, index, biom):
		biom.stuff.append(self.inventory[index])
		# TODO: Allow throw all items qty
		vprint("[i] You throwed 1 {0} to the current location", self.inventory[index].name)
		del self.inventory[index]

	def act(self, inp):
		# XXX: Instead of using self.stage, we could directly use dialog
		self.stage = self.get_biome().act(self, self.stage, inp)

	def dialog_walk_to_biome(self):
		clear()
		adjacent = list()
		for y in range(-1, 2):
			for x in range(-1, 2):
				pos = [self.position[0] + x, self.position[1] + y]
				biom = self.environment.get_biome(*pos)
				adjacent.append((biom, pos))

		def print_adjacent(cord):
			clear()
			middle(-6 + (-4))
			# Guide
			center("Up/Down/Left/Right Arrows - Point direction")
			center("Return/Enter - Start journey")
			center("Esc - Back to current biome")
			print()

			_n = lambda x: (term.normal + x)
			# For loop
			for i in range(3):
				frow = ['', '', '', '', '']
				cpos = [cord[0] + self.position[0], cord[1] + self.position[1]]
				for b, pos in adjacent[(i*3):(i*3)+3]:
					if b is None:
						b = Biome('VOID', 0, term.black_on_black)
						b.distance = 0
						b.travel_hour = 0

					gold = term.on_gold('|') if pos == cpos else (term.normal + '|')
					gold1 = term.on_gold('+') if pos == cpos else (term.normal + '+')
					goldif = (lambda x: term.on_gold(x)) if pos == cpos else _n

					# TODO: goldif should activate when row 2 selected
					if i != 1:
						frow[0] += gold1 + goldif('-' * 10) + gold1
					frow[1] += gold + b.color(b.name.center(10)) + gold
					# TODO: "1 hours" should be "an hour" or "1 hour"
					if pos == self.position:
						frow[2] += gold + b.color(f"YOU ARE".center(10)) + gold
					else:
						frow[2] += gold + b.color(f"{b.travel_hour} hours".center(10)) + gold
					# Distance is in KM, so one KM = 20 energy
					# TODO: if energy not enough, paint this red
					if pos == self.position:
						frow[3] += gold + b.color(f"HERE".center(10)) + gold
					else:
						frow[3] += gold + b.color(f"{b.distance * 20} energy".center(10)) + gold
					if i != 1:
						frow[4] += gold1 + goldif('-' * 10) + gold1

				if i != 1:
					center(frow[0])
				center(frow[1])
				center(frow[2])
				center(frow[3])
				if i != 1:
					center(frow[4])

		# Select biome
		cord = [0, 0]
		inp = chr(0)

		def move_cord(x, y):
			cord[0] += x
			cord[1] += y

			if cord[0] > 1 or cord[0] < -1:
				cord[0] -= x
			if cord[1] > 1 or cord[1] < -1:
				cord[1] -= y

		print_adjacent(cord)
		while inp != '\n':
			with term.cbreak(), term.hidden_cursor():
				inp = term.inkey()

			if inp.name == "KEY_UP":
				move_cord(0, -1)
			if inp.name == "KEY_DOWN":
				move_cord(0, 1)
			if inp.name == "KEY_LEFT":
				move_cord(-1, 0)
			if inp.name == "KEY_RIGHT":
				move_cord(1, 0)

			if inp.name == "KEY_ESCAPE":
				return False

			print_adjacent(cord)

		d = list(self.position)
		self.position[0] += cord[0]
		self.position[1] += cord[1]

		bi = self.environment.get_biome(*self.position)

		# Bro, you can't travel to VOID
		if bi is None:
			self.position = d
			return False

		if d != self.position:
			self.energy -= vprint("[-] {0} Energy", bi.distance * 20)[0]
		return True
