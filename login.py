import clutter
import gtk
import math
import os

class BehaviourHighlight(clutter.Behaviour):

	__gtype_name__ = 'BehaviourHighlight'

	def __init__(self, alpha):
		clutter.Behaviour.__init__(self)
		self.set_alpha(alpha)
		self.bulge_angle = 90
		self.bulge_min = 67.5
		self.bulge_max = 112.5
		self.interval = self.bulge_max - self.bulge_min
		self.fraction = 180.0 / self.interval

	def do_alpha_notify (self, alpha_value):
		for actor in self.get_actors():
			if self.bulge_min <= actor.angle <= self.bulge_max:
				actor.set_opacity(int(255 * math.sin(math.radians((actor.angle - self.bulge_min) * self.fraction))))
			elif self.bulge_min - 360 <= actor.angle <= self.bulge_max - 360:
				actor.set_opacity(int(255 * math.sin(math.radians((actor.angle - (self.bulge_min - 360)) * self.fraction))))
			else:
				actor.set_opacity(0)


class BehaviourTurn(clutter.Behaviour):

	__gtype_name__ = 'BehaviourTurn'

	def __init__(self, alpha):
		clutter.Behaviour.__init__(self)
		self.set_alpha(alpha)

	def do_alpha_notify(self, alpha_value):
		for actor in self.get_actors():
			actor.set_rotation(clutter.Z_AXIS, actor.get_rotation(clutter.Z_AXIS)[0]  + 1, (actor.get_width() / 2), (actor.get_height() / 2), 0)


class BehaviourSpin(clutter.Behaviour):

	__gtype_name__ = 'BehaviourSpin'

	def __init__(self, alpha, direction = "clockwise", items = 1, item_number = 1):
		clutter.Behaviour.__init__(self)
		self.set_alpha(alpha)		# Apply the animation step to follow
		self.direction = direction		# Remember which way around to go
		self.bulge_angle = 90		# The angle at which we should be bigger
		self.bulge_min = 67.5		# The angles at which to start/end growing
		self.bulge_max = 112.5
		# The start and end angles tell us how fast to move around the ellipse
		# ie. the angle until the next stop
		if direction == "clockwise":
			self.angle_start = self.bulge_angle + (360.0 / items) * item_number
			self.angle_end = 360.0 + self.bulge_angle + (360.0 / items) * item_number
		else:
			self.angle_start = 360.0 + self.bulge_angle - (360.0 / items) * item_number
			self.angle_end = self.bulge_angle - (360.0 / items) * item_number
		self.angle = self.angle_start
		self.width = 500.0
		self.height = 75.0
		self.tilt = -10.0
		self.items = items
		self.item_number = item_number
		self.phase = 0.0		# Initial value to compare first alpha with

	def apply(self, actor):
		"""This sets the start position when the behaviour is applied"""
		clutter.Behaviour.apply(self, actor)
		actor.angle = self.angle		# Store the angle around the ellipse inside the actor so every behaviour on the actor is in sync
		# Set default positions and size
		actor.set_position(int(self.x_position(actor.angle)), int(self.y_position(actor.angle)))
		actor.set_scale(math.cos(math.radians((actor.angle / 2) - 45))**2 + 0.25, math.cos(math.radians((actor.angle / 2) - 45))**2 + 0.25)
		if self.bulge_min <= actor.angle <= self.bulge_angle:
			 actor.set_scale(math.cos(math.radians((actor.angle / 2) - 45))**2 + 0.25 + (actor.angle - self.bulge_min) / (self.bulge_angle - self.bulge_min), math.cos(math.radians((actor.angle / 2) - 45))**2 + 0.25 + (actor.angle - self.bulge_min) / (self.bulge_angle - self.bulge_min))
		elif self.bulge_angle < actor.angle <= self.bulge_max:
			 actor.set_scale(math.cos(math.radians((actor.angle / 2) - 45))**2 + 0.25 - (actor.angle - self.bulge_max) / (self.bulge_max - self.bulge_angle), math.cos(math.radians((actor.angle / 2) - 45))**2 + 0.25 - (actor.angle - self.bulge_max) / (self.bulge_max - self.bulge_angle))


	def x_position(self, angle):
		return self.width * math.cos(math.radians(angle)) * math.cos(math.radians(self.tilt)) - self.height * math.sin(math.radians(angle)) * math.sin(math.radians(self.tilt)) + 275

	def y_position(self, angle):
		return self.width * math.cos(math.radians(angle)) * math.sin(math.radians(self.tilt)) + self.height * math.sin(math.radians(angle)) * math.cos(math.radians(self.tilt)) + 200

	def do_alpha_notify (self, alpha_value):
		phase = (alpha_value + 0.0) / (clutter.MAX_ALPHA + 0.0)
		delta = self.phase - phase
		self.phase = phase
		increment = delta * (((self.angle_end - self.angle_start) / self.items))

		for actor in self.get_actors():
			if abs(increment) <= abs(((self.angle_end - self.angle_start) / self.items) / 2):
				actor.angle += increment
			if actor.angle > 360:
				actor.angle -= 360
			elif actor.angle < -360:
				actor.angle += 360
			actor.set_position(int(self.x_position(actor.angle)), int(self.y_position(actor.angle)))
			actor.set_scale(math.cos(math.radians((actor.angle / 2) - 45))**2 + 0.25, math.cos(math.radians((actor.angle / 2) - 45))**2 + 0.25)
			if self.bulge_min < actor.angle < self.bulge_max:
				if self.bulge_min <= actor.angle <= self.bulge_angle:
					actor.set_scale(math.cos(math.radians((actor.angle / 2) - 45))**2 + 0.25 + (actor.angle - self.bulge_min) / (self.bulge_angle - self.bulge_min), math.cos(math.radians((actor.angle / 2) - 45))**2 + 0.25 + (actor.angle - self.bulge_min) / (self.bulge_angle - self.bulge_min))
				elif self.bulge_angle < actor.angle <= self.bulge_max:
					actor.set_scale(math.cos(math.radians((actor.angle / 2) - 45))**2 + 0.25 - (actor.angle - self.bulge_max) / (self.bulge_max - self.bulge_angle), math.cos(math.radians((actor.angle / 2) - 45))**2 + 0.25 - (actor.angle - self.bulge_max) / (self.bulge_max - self.bulge_angle))
			elif self.bulge_min - 360 < actor.angle < self.bulge_max - 360:
				if self.bulge_min - 360 <= actor.angle <= self.bulge_angle - 360:
					actor.set_scale(math.cos(math.radians((actor.angle / 2) - 45))**2 + 0.25 + (actor.angle - (self.bulge_min - 360)) / (self.bulge_angle - self.bulge_min), math.cos(math.radians((actor.angle / 2) - 45))**2 + 0.25 + (actor.angle - (self.bulge_min - 360)) / (self.bulge_angle - self.bulge_min))
				elif self.bulge_angle - 360 < actor.angle <= self.bulge_max - 360:
					actor.set_scale(math.cos(math.radians((actor.angle / 2) - 45))**2 + 0.25 - (actor.angle - (self.bulge_max - 360)) / (self.bulge_max - self.bulge_angle), math.cos(math.radians((actor.angle / 2) - 45))**2 + 0.25 - (actor.angle - (self.bulge_max - 360)) / (self.bulge_max - self.bulge_angle))


class ClutterDisplay:

	def __init__(self, (size_x, size_y), background, timelines):
		self.x = size_x
		self.y = size_y
		#self.stage = clutter.stage_get_default()
		self.stage = clutter.Stage()
		self.stage.set_size(size_x, size_y)
		self.stage.set_color(clutter.color_parse(background))
		self.timelines = timelines

	def add_rectangle(self, (position_x, position_y), (size_x, size_y), color, border = 0, border_color = "#FFFFFF", behaviours = {}):
		rectangle = clutter.Rectangle()
		rectangle.set_position(position_x, position_y)
		rectangle.set_size(size_x, size_y)
		rectangle.set_color(clutter.color_parse(color))
		if border > 0:
			rectangle.set_border_width(border)
			rectangle.set_border_color(clutter.color_parse(border_color))
		self.stage.add(rectangle)
		for behaviour in behaviours.itervalues():
			behaviour.apply(rectangle)
		rectangle.show()

	def add_texture(self, filename, (position_x, position_y), (size_x, size_y), behaviours = {}):
		try:
			pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
		except Exception:
			print "Unable to find " + filename
		else:
			texture = clutter.Texture(pixbuf)
			texture.set_position(position_x, position_y)
			if size_x != 0:
				texture.set_size(size_x, size_y)
			self.stage.add(texture)
			for behaviour in behaviours.itervalues():
				behaviour.apply(texture)
			texture.behaviours = behaviours		# This is needed to stop the behaviours getting garbage-collected
			texture.show()

	def add_face(self, filename, (position_x, position_y), (size_x, size_y), behaviours = {}, spin_behaviours = []):
		try:
			pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
			pixbuf_sparkle = gtk.gdk.pixbuf_new_from_file("sparkle.png")
		except Exception:
			print "Unable to find " + filename
		texture = clutter.Texture(pixbuf)
		texture.set_position(position_x, position_y)
		texture.set_size(size_x, size_y)
		sparkle = clutter.Texture(pixbuf_sparkle)
		sparkle.set_position(position_x, position_y)
		sparkle.set_size(size_x, size_y)
		face = clutter.Group()
		face.add(sparkle)
		face.add(texture)
		self.stage.add(face)
		for behaviour in behaviours.itervalues():
			behaviour.apply(face)
		for behaviour in spin_behaviours:
			behaviour.apply(sparkle)
		face.show_all()

	def input_keys(self, stage, event):
		key = gtk.gdk.keyval_name(event.keyval)
		self.timelines[key].start()
		self.timelines["Opacity"].start()

	def delete_event(self, event, data=None):
		clutter.main_quit()

	def main(self):
		self.stage.show()
		self.stage.connect("key-press-event", self.input_keys)
		self.stage.connect("destroy-event", self.delete_event)
		clutter.main()

if __name__ == '__main__':
	timeline1 = clutter.Timeline(fps=50, duration=500)
	timeline1.set_loop(False)
	timeline2 = clutter.Timeline(fps=50, duration=500)
	timeline2.set_loop(False)
	timeline_opacity = clutter.Timeline(fps=50, duration=500)
	timeline2.set_loop(False)
	timeline_rotate = clutter.Timeline(fps=50, duration=5000)
	timeline_rotate.set_loop(True)

	timelines = {"Right":timeline1, "Left":timeline2, "Opacity":timeline_opacity}

	alpha1 = clutter.Alpha(timeline1, clutter.smoothstep_inc_func)
	alpha2 = clutter.Alpha(timeline2, clutter.smoothstep_inc_func)
	alpha_opacity = clutter.Alpha(timeline_opacity, clutter.smoothstep_inc_func)
	alpha_rotate = clutter.Alpha(timeline_rotate, clutter.ramp_inc_func)

	#display = ClutterDisplay((800, 600), "#E0DFDE", timelines)		# Makes an 800x600 Oxygen-coloured window
	display = ClutterDisplay((800, 600), "#000000", timelines)		# Makes an 800x600 black window

	spin_behaviours = [BehaviourTurn(alpha_rotate), BehaviourHighlight(alpha_opacity)]		# These are the highlight-specific behaviours

	filenames = os.listdir(os.getcwd() + "/faces")

	for x in range(0, len(filenames)):
		display.add_texture("sparkle.png", (x, x), (100, 100), {"Right":BehaviourSpin(alpha1, "anticlockwise", len(filenames), x + 1), "Left":BehaviourSpin(alpha2, "clockwise", len(filenames), x + 1), "Opacity":BehaviourHighlight(alpha_opacity), "Spin":BehaviourTurn(alpha_rotate)})
		display.add_texture("faces/" + filenames[x], (x, x), (0, 0), {"Right":BehaviourSpin(alpha1, "anticlockwise", len(filenames), x + 1), "Left":BehaviourSpin(alpha2, "clockwise", len(filenames), x + 1)})

	timeline_rotate.start()

	display.main()
