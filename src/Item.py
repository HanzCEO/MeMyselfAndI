class Item(object):
	def __init__(self, name, weight):
		self.name = name
		self.weight = weight

	@property
	def display_name(self):
		return self.name.replace('_', ' ').title()

	def detail_dialog(self):
		return "noop"
