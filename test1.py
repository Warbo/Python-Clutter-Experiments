import clutter

class BehaviourSpin (clutter.Behaviour):
	__gtype_name__ = 'BehaviourSpin'
	def __init__(self, alpha):
		clutter.Behaviour.__init__(self)
		self.set_alpha(alpha)
		self.angle_start = 0.0
		self.angle_end = 359.0

	def do_alpha_notify (self, alpha_value):
		angle = alpha_value \
			* (self.angle_end - self.angle_start) \
			/ clutter.MAX_ALPHA

		for actor in self.get_actors():
			actor.set_rotation(clutter.Z_AXIS, angle,
				actor.get_x(),
				actor.get_y(),
				0)

class ClutterDisplay:

	def __init__(self, (size_x, size_y), background, behaviours):
		self.x = size_x
		self.y = size_y
		self.stage = clutter.stage_get_default()
		self.stage.set_size(size_x, size_y)
		self.stage.set_color(clutter.color_parse(background))
		self.behaviours = behaviours

	def add_rectangle(self, (position_x, position_y), (size_x, size_y), color, border = 0, border_color = "#FFFFFF"):
		rectangle = clutter.Rectangle()
		rectangle.set_position(position_x, position_y)
		rectangle.set_size(size_x, size_y)
		rectangle.set_color(clutter.color_parse(color))
		if border > 0:
			rectangle.set_border_width(border)
			rectangle.set_border_color(clutter.color_parse(border_color))
		self.stage.add(rectangle)
		for behaviour in behaviours:
			behaviour.apply(rectangle)
		rectangle.show()

	def input_keys(self, arg2, arg3):
		print "Input width (zero to quit): ",
		width = input()
		if width == 0:
			clutter.main_quit()
			return
		print "Input height (zero to quit): ",
		height = input()
		if height == 0:
			clutter.main_quit()
			return
		print "Input x coordinate (0 to quit): ",
		x = input()
		if x == 0:
			clutter.main_quit()
			return
		while abs(x) > self.x:
			if x < 0:
				x +=self.x
			else:
				x -= self.x
		if x < 0:
			x = self.x - x
		print "Input y coordinate (0 to quit): ",
		y = input()
		if y == 0:
			clutter.main_quit()
			return
		while abs(y) > self.y:
			if y < 0:
				y +=self.y
			else:
				y -= self.y
		if y < 0:
			y = self.y - y
		print "Input colour in hexidecimal ('quit' to quit): #",
		color = "#" + raw_input()
		if color == "#quit":
			clutter.main_quit()
			return
		print "Enter a border width (0 to quit, negative for no border): ",
		border = input()
		if border == 0:
			clutter.main_quit()
			return
		has_border = False
		if border > 0:
			has_border = True
		if has_border:
			print "Enter the border colour ('quit' to quit): #",
			border_color = "#" + raw_input()
			if border_color == "#quit":
				clutter.main_quit()
				return
		print "Adding rectangle:"
		print "Width: " + str(width) + ", Height: " + str(height)
		print "Position: (" + str(x) + ", " + str(y) + ")"
		print "Colour: " + color
		if has_border:
			print "Border: Width: " + str(border) + ", Colour: " + border_color
			self.add_rectangle((x, y), (width, height), color, border, border_color)
		else:
			self.add_rectangle((x, y), (width, height), color)
		return

	def main(self):
		self.stage.show()
		self.stage.connect("key-press-event", self.input_keys)
		clutter.main()

if __name__ == '__main__':
	timeline = clutter.Timeline(fps=50, duration=3000)
	timeline.set_loop(True)
	alpha = clutter.Alpha(timeline, clutter.smoothstep_inc_func)

	knots = ((100, 100), (200, 100), (200, 200), (100, 200),)

	behaviours = [BehaviourSpin(alpha), clutter.BehaviourPath(alpha=alpha, knots=knots)]
	behaviours[1].append_knots((100, 100))

	display = ClutterDisplay((800, 600), "#E0DFDE", behaviours)

	timeline.start()

	display.add_rectangle((50, 50), (100, 100), "#0099FF", 10, "#FFFFFF")

	display.main()
