import clutter
import gtk
import os
import math

class BehaviourHighlight(clutter.Behaviour):

	__gtype_name__ = 'BehaviourHighlight'

	def __init__(self, alpha):
		clutter.Behaviour.__init__(self)
		self.set_alpha(alpha)

	def do_alpha_notify(self, alpha_value):
		progress = (alpha_value + 0.0) / (clutter.MAX_ALPHA + 0.0)
		for actor in self.get_actors():
			if actor.newly_selected:
				actor.set_scale(actor.normal_scale[0] + actor.normal_scale[0] * progress, actor.normal_scale[1] + actor.normal_scale[1] * progress)
				if progress == 1.0:
					actor.newly_selected = False
			elif actor.unselected:
				actor.set_scale(actor.normal_scale[0] + actor.normal_scale[0] * (1 - progress), actor.normal_scale[1] + actor.normal_scale[1] * (1 - progress))
				if progress == 1.0:
					actor.unselected = False

class BehaviourScroll(clutter.Behaviour):

	__gtype_name__ = 'BehaviourScroll'

	def __init__(self, alpha, rate, direction = "Down"):
		clutter.Behaviour.__init__(self)
		self.set_alpha(alpha)

	def do_alpha_notify(self, alpha_value):
		progress = (alpha_value + 0.0) / (clutter.MAX_ALPHA + 0.0)
		for actor in self.get_actors():
			if direction == "Down":
				actor.set_position(actor.old_position[0], actor.old_position[1] + rate * progress)
			elif direction == "Up":
				actor.set_position(actor.old_position[0], actor.old_position[1] - rate * progress)
			elif direction == "Left":
				actor.set_position(actor.old_position[0] - rate * progress, actor.old_position[1])
			elif direction == "Right":
				actor.set_position(actor.old_position[0] + rate * progress, actor.old_position[1])

class ImagePane:

	def __init__(self, size, max_image_size, padding, background, timeline):
		self.x = size[0]
		self.y = size[1]
		self.max_image_size = max_image_size
		self.padding = padding
		self.stage = clutter.Stage()
		self.stage.set_size(size[0], size[1])
		self.stage.set_color(clutter.color_parse(background))
		self.timeline = timeline
		self.image_number = 0
		self.selection = 0
		self.old_selection = 0
		self.row_size = int(math.floor((size[0] - self.padding[0]) / (max_image_size[0] + self.padding[0])))
		print str(self.row_size)
		self.behaviours = []
		self.textures = []

	def add_image(self, filename, behaviour = []):
		try:
			pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
		except Exception:
			print "Unable to find " + filename
		else:
			texture = clutter.Texture(pixbuf)
			texture.newly_selected = False
			texture.unselected = False
			self.textures.append(texture)
			texture_size = texture.get_size()
			if texture_size[0] / self.max_image_size[0] > texture_size[1] / self.max_image_size[1]:
				texture.set_scale(self.max_image_size[0] / texture_size[0], self.max_image_size[0] / texture_size[0])
			else:
				texture.set_scale(self.max_image_size[1] / texture_size[1], self.max_image_size[1] / texture_size[1])
			texture.set_position((self.image_number % self.row_size) * (self.max_image_size[0] + self.padding[0]) + self.padding[0] + (self.max_image_size[0] / 2),\
				math.ceil(self.image_number / self.row_size) * (self.max_image_size[1] + self.padding[1]) + self.padding[1] + (self.max_image_size[1] / 2))
			texture.set_anchor_point(texture.get_size()[0] / 2, texture.get_size()[1] / 2)

			self.stage.add(texture)
			texture.show()
			texture.normal_scale = (self.max_image_size[0] / texture_size[0], self.max_image_size[0] / texture_size[0])
			self.image_number += 1
			for behaviour in behaviours:
				behaviour.apply(texture)
				self.behaviours.append(behaviour)
			print "Added image"

	def input_keys(self, stage, event):
		key = gtk.gdk.keyval_name(event.keyval)
		self.change_selection(key)
		self.timeline.start()
		self.old_selection = self.selection

	def change_selection(self, key):
		if key == "Left":
			if self.selection > 0:
				self.selection -= 1
		elif key == "Right":
			if self.selection < self.image_number:
				self.selection += 1
		elif key == "Up":
			if self.selection - self.row_size >= 0:
				self.selection -= self.row_size
		elif key == "Down":
			if self.selection + self.row_size <= self.image_number:
				self.selection += self.row_size
		if self.selection != self.old_selection:
			self.textures[self.selection].newly_selected = True
			self.textures[self.old_selection].unselected = True
		print str((self.selection, self.old_selection))

	def main(self):
		self.stage.show()
		self.stage.connect("key-press-event", self.input_keys)
		clutter.main()

if __name__ == '__main__':
	timeline = clutter.Timeline(fps=50, duration=500)
	timeline.set_loop(False)

	alpha = clutter.Alpha(timeline, clutter.smoothstep_inc_func)

	behaviours = []
	behaviours.append(BehaviourHighlight(alpha))

	#display = ImagePane((800.0, 600.0), (100.0, 100.0), (50.0, 50.0), "#E0DFDE", timeline)		# Makes an 800x600 Oxygen-coloured window
	display = ImagePane((1024.0, 600.0), (75.0, 75.0), (25.0, 25.0), "#000000", timeline)		# Makes an 800x600 black window

	filenames = os.listdir(os.getcwd() + "/images")

	for x in range(0, len(filenames)):
		display.add_image("images/" + filenames[x], behaviours)

	display.main()
