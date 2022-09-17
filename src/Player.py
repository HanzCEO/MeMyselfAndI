from .utils.ui import progress_bar

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
				selected.throw_to(self.get_biome())
				# Finally remove the item from our inventory
				itemAct = "delete"


			# Special interaction with item; consume
			if itemAct == "consume":
				# Not consume player bruh, the API has weird application
				itemAct = selected.consume(player)
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
		for i, item in enumerate(self_inventory):
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

	def act(self, inp):
		# XXX: Instead of using self.stage, we could directly use dialog
		self.stage = self.get_biome().act(self, self.stage, inp)
