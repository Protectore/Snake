from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import (Color, Rectangle)

width = 15
height = width


class RootLayout(BoxLayout):
	pass


class SnakePanel(Widget):
	pass


class SnakeScreen(GridLayout):
	snake_map = [[] for i in range(height)]
	def __init__(self, **kwargs):
		super(SnakeScreen, self).__init__(**kwargs)

		self.cols = width
		self.rows = height
		self.height = 20
		self.spacing = 1
		for i in range(width):
			for j in range(height):
				SnakeScreen.snake_map[i].append(SnakePanel())
				self.add_widget(self.snake_map[i][j])


class SnakeApp(App):
	def build(self):
		return RootLayout()


if __name__ == '__main__':
	Window.clearcolor = (.95, 1, .59, 1)
	SnakeApp().run()