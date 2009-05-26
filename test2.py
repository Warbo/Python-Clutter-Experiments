import clutter
import gtk
import math

class BehaviourSpin(clutter.Behaviour):

	__gtype_name__ = 'BehaviourSpin'

	def __init__(self, alpha, width, height, tilt, (offset_x, offset_y), start_angle = 0):
		clutter.Behaviour.__init__(self)		# Call the superclass constructor
		self.set_alpha(alpha)		# Set the tick of the animation
		self.angle_start = start_angle		# Where abouts on the ellipse we start
		self.angle_end = start_angle - 359.0		# Where abouts on the ellipse we are aiming for
		self.angle = self.angle_start		# This stores the angle traversed around the ellipse
		self.width = width		# The width of the ellipse
		self.height = height		# The height of the ellipse (can be changed with Up/Down)
		self.tilt = tilt		# The angle in degrees to tile the ellipse anticlockwise
		self.offset = (offset_x, offset_y)		# Where the centre of the ellipse should be
		self.phase = 0.0		# Initialise this to zero for comparisons later

	def x_position(self, angle):
		"""Calculates the horizontal position on the screen at a given angle around the ellipse"""
		# This is a standard mathematical description of a tilted ellipse
		return self.width * math.cos(math.radians(angle)) * math.cos(math.radians(self.tilt)) - self.height * math.sin(math.radians(angle)) * math.sin(math.radians(self.tilt)) + self.offset[0]

	def y_position(self, angle):
		"""Calculates the vertical position on the screen at a given angle around the ellipse"""
		# This is a standard mathematical description of a tilted ellipse
		return self.width * math.cos(math.radians(angle)) * math.sin(math.radians(self.tilt)) + self.height * math.sin(math.radians(angle)) * math.cos(math.radians(self.tilt)) + self.offset[1]

	def do_alpha_notify (self, alpha_value):
		phase = (alpha_value + 0.0) / (clutter.MAX_ALPHA + 0.0)		# Get a value from 0.0 - 1.0 of our progress
		delta = self.phase - phase		# Calculate the difference since the last time
		self.phase = phase		# Update our last known position
		increment = delta * (((self.angle_end - self.angle_start)))		# Calculate how much angle we should move
		self.angle += increment		# Add it to the current angle

		# This prevents the values becoming too large by making every turn the first one
		if self.angle > 360:
			self.angle -= 360
		elif self.angle < -360:
			self.angle += 360

		for actor in self.get_actors():
			# Update the position and size based on the new angle
			actor.set_position(self.x_position(self.angle), self.y_position(self.angle))
			actor.set_scale(math.cos(math.radians((self.angle / 2) - 45))**2 + 0.25, math.cos(math.radians((self.angle / 2) - 45))**2 + 0.25)

	def turn(self, angle):
		"""This tilts the ellipse anticlockwise by the given number of degrees"""
		self.tilt += angle

	def stretch(self, amount):
		"""This adds the given number onto the ellipse height"""
		self.height += amount

class ClutterDisplay:

	def __init__(self, (size_x, size_y), background):
		self.x = size_x
		self.y = size_y
		self.stage = clutter.stage_get_default()
		self.stage.set_size(size_x, size_y)
		self.stage.set_color(clutter.color_parse(background))
		self.behaviours = []

	def add_rectangle(self, (position_x, position_y), (size_x, size_y), color, border, border_color, behaviour):
		rectangle = clutter.Rectangle()
		rectangle.set_position(position_x, position_y)
		rectangle.set_size(size_x, size_y)
		rectangle.set_color(clutter.color_parse(color))
		if border > 0:
			rectangle.set_border_width(border)
			rectangle.set_border_color(clutter.color_parse(border_color))
		self.stage.add(rectangle)
		self.behaviours.append(behaviour)
		behaviour.apply(rectangle)
		rectangle.show()

	def input_keys(self, stage, event):
		key = gtk.gdk.keyval_name(event.keyval)
		if key == "Left":
			for behaviour in self.behaviours:
				behaviour.turn(5)
		elif key == "Right":
			for behaviour in self.behaviours:
				behaviour.turn(-5)
		elif key == "Up":
			for behaviour in self.behaviours:
				behaviour.stretch(5)
		elif key == "Down":
			for behaviour in self.behaviours:
				behaviour.stretch(-5)

	def main(self):
		self.stage.show()
		self.stage.connect("key-press-event", self.input_keys)
		clutter.main()

if __name__ == '__main__':
	timeline1 = clutter.Timeline(fps=50, duration=2500)
	timeline1.set_loop(True)
	display = ClutterDisplay((800, 600), "#000000")
	alpha1 = clutter.Alpha(timeline1, clutter.ramp_inc_func)
	for x in range(0, 10):
		display.add_rectangle((10, 250), (10, 10), "#FFFFFF", 0, "#000000", BehaviourSpin(alpha1, 300, 100, 0, (400, 300), 36 * x))

	timeline1.start()
	display.main()
