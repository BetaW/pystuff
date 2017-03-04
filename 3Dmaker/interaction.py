from collections import defaultdict
from OpenGL.GLUT import glutGet, glutKeyboardFunc, glutMotionFunc, glutMouseFunc, glutPassiveMotionFunc, \
                        glutPostRedisplay, glutSpecialFunc
from OpenGL.GLUT import GLUT_LEFT_BUTTON, GLUT_RIGHT_BUTTON, GLUT_MIDDLE_BUTTON, \
                        GLUT_WINDOW_HEIGHT, GLUT_WINDOW_WIDTH, \
                        GLUT_DOWN, GLUT_KEY_UP, GLUT_KEY_DOWN, GLUT_KEY_LEFT, GLUT_KEY_RIGHT
import trackball

class Interaction(object):
	def __init__(self):
		self.press = None
		self.trackball = trackball.Trackball(theta = -25, distance=15)
		self.mouse_loc = None
		self.callbacks = defaultdict(list)
		self.register()

	def register(self):
		glutMouseFunc(self.handle_mouse_button)
		glutMotionFunc(self.handle_mouse_move)
		glutKeyboardFunc(self.handle_keystroke)
		glutSpecialFunc(self.handle_keystroke)

	def handle_mouse_button(self, button, mode, x, y):
		xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
		y = ySize - y
		self.mouse_loc = (x, y)

		if mode == GLUT_DOWN:
			self.press = button
			if button == GLUT_RIGHT_BUTTON:
				pass
			elif button == GLUT_LEFT_BUTTON:
				self.trigger('pick', x, y)
		else:
			self.press = None

		glutPostRedisplay()

	def handle_mouse_move(self, x, screen_y):
		xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
		y = ySize - screen_y 
		if self.press is not None:
			dx = x - self.mouse_loc[0]
			dy = y - self.mouse_loc[1]
			if self.press == GLUT_RIGHT_BUTTON and self.trackball is not None:
				self.trackball.drag_to(self.mouse_loc[0], self.mouse_loc[1], dx, dy)
			elif self.press == GLUT_LEFT_BUTTON:
				self.trigger('move', x, y)
			elif self.press == GLUT_MIDDLE_BUTTON:
				self.translate(dx/60.0, dy/60.0, 0)
			else:
				pass
			glutPostRedisplay()
		self.mouse_loc = (x, y)

	def handle_keystroke(self, key, x, screen_y):
		xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
		y = ySize - screen_y
		if key == 's':
			self.trigger('place', 'sphere', x, y)
		elif key == 'c':
			self.trigger('place', 'cube', x, y)
		elif key == GLUT_KEY_UP:
			self.trigger('scale', up=True)
		elif key == GLUT_KEY_DOWN:
			self.trigger('scale', up=False)
		elif key == GLUT_KEY_LEFT:
			self.trigger('rotate_color', forward=True)
		elif key == GLUT_KEY_RIGHT:
			self.trigger('rotate_color', forward=False)
		glutPostRedisplay()

	def trigger(self, name, *args, **kwargs):
		for func in self.callbacks[name]:
			func(*args, **kwargs)

	def register_callback(self, name, func):
		self.callbacks[name].append(func)
	


