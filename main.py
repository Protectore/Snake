from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import (Color, Rectangle)
from kivy.clock import Clock
from random import randint

background_color = (.95, 1, .59, 1)
width = 15
height = width
show_position = True
empty_color = (1, 0, 0, 1)
body_color = (.3, .9, 0, 1)
head_color = (0, .8, 0, 1)
food_color = (1, .91, 0, 1)
tickrait = 1


class RootLayout(BoxLayout):		# Main widget, all wigets stacked on him
	def __init__(self, **kwargs):
		super(RootLayout, self).__init__(**kwargs)


class SnakePanel(Label):			# Widget for cell of snake screen
	pass


class Snake:
	def __init__(self):
		self.snake = [[height-2, 1, 'right'], [height-2, 2, 'right'], [height-2, 3, 'right']]
		self.map = [[0 for i in range(width)] for i in range(height)]
		self.food = ()

	def get_map_status(self):	# update map with values for panels colors
		for i in range(height):
			for j in range(width):
				self.map[i][j] = 0 # Cleaning cuurent status

		for i in range(len(self.snake)-1):
			self.map[self.snake[i][0]][self.snake[i][1]] = 1 # marking body

		self.map[self.snake[-1][0]][self.snake[-1][1]] = 2	# marking head

		if self.food != ():
			self.map[self.food[0]][self.food[1]] = 3	# 3 marking food

		return self.map

	def move(self):		# move snake by 1 tick
		for i in range(len(self.snake)):
			self.snake[i][0], self.snake[i][1] = Snake.get_next_cell(self.snake[i])
			if i + 1 < len(self.snake):
				self.snake[i][2] = self.snake[i+1][2]

	@classmethod
	def get_next_cell(self, cell):
		if cell[2] == 'right':
			return cell[0], cell[1]+1
		elif cell[2] == 'left':
			return cell[0], cell[1]-1
		elif cell[2] == 'up':
			return cell[0]-1, cell[1]
		elif cell[2] == 'down':
			return cell[0]+1, cell[1]


class SnakeScreen(GridLayout):		# Widget for snake playground
	def __init__(self, **kwargs):
		super(SnakeScreen, self).__init__(**kwargs)

		self.snake = Snake()
		self.panels = [[] for i in range(height)]
		self.cols = width
		self.rows = height
		self.height = 20
		self.spacing = 1
		txt = ""
		for i in range(height):
			for j in range(width):
				if show_position:
					txt = f"{i} {j}"
				self.panels[i].append(SnakePanel(text=txt))
				self.add_widget(self.panels[i][j])
		self.redraw()

	def spawn_food(self):	# Creates food by adding it on snake's map
		x, y = randint(0, width-1), randint(0, height-1)
		while self.snake.map[x][y] != 0:
			x, y = randint(0, width-1), randint(0, height-1)
		print('food spawned')
		self.snake.map[y][x] = 3
		self.snake.food = (y, x)

	def redraw(self):	# Paint panels on playground in dependence from value on snake's map
		status = self.snake.get_map_status()
		for i in range(height):
			for j in range(width):
				if status[i][j] == 0:
					self.panels[i][j].background_color = empty_color
				elif status[i][j] == 1:
					self.panels[i][j].background_color = body_color
				elif status[i][j] == 2:
					self.panels[i][j].background_color = head_color
				elif (self.snake.food != ()) and (status[i][j] == 3):
					self.panels[i][j].background_color = food_color


class SnakeApp(App):
	def build(self):
		root = RootLayout()
		self.root = root
		self.snake_screen = root.snake_screen
		self.started = False	# Variable that show started timer or not
		Window.bind(on_key_down=self.control)

		return root

	def msg(self, text):		# Update text on message label
		self.root.message_label.text = text

	def start(self):			# Start timer
		if not self.started:
			self.started = True
			self.snake_screen.spawn_food()
			self.snake_screen.redraw()
			Clock.schedule_interval(self.update, tickrait)
			print('timer started!')
			self.msg("Game started!")

	def stop(self):				# Stop timer
		if self.started:
			Clock.unschedule(self.update)
			print('timer stoped')
			self.started = False
			self.snake_screen.snake = Snake()

	def update(self, _):		# Function for timer update
		x, y = Snake.get_next_cell(self.snake_screen.snake.snake[-1])
		print(x, y)
		if ((x < 0) or (x >= width) or (y < 0) or (y >= height)):
			self.stop()
			self.msg("Game over :(")
			return
		self.snake_screen.snake.move()
		print(self.snake_screen.snake.map)
		print(self.snake_screen.snake.snake)
		self.snake_screen.redraw()

	def control(self, event, keyboard, keycode, text, modifiers): # Key events
		snake = self.snake_screen.snake.snake
		head = snake[-1]
		pre_head = snake[-2]
		if ((keycode == 82) and (pre_head[2] != 'down')): #Arrow up to move snake up
			head[2] = 'up'
		elif ((keycode == 81) and (pre_head[2] != 'up')): #Arrow down to move snake down
			head[2] = 'down'
		elif ((keycode == 80) and (pre_head[2] != 'right')): #Arrow left to move snake left
			head[2] = 'left'
		elif ((keycode == 79) and (pre_head[2] != 'left')): #Arrow right to move snake right
			head[2] = 'right'


if __name__ == '__main__':
	Window.clearcolor = background_color
	SnakeApp().run()





