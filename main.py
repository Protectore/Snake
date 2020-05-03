from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import (Color, Rectangle)
from kivy.factory import Factory
from kivy.clock import Clock
from random import randint
from copy import deepcopy
import json

background_color = (.95, 1, .59, 1)
width = 15
height = width
enumerate_ = False
empty_color = (1, 0, 0, 1)
body_color = (.3, .9, 0, 1)
head_color = (0, .8, 0, 1)
food_color = (1, .91, 0, 1)
start_tickrait = 1
tor = False
ai = False
audio = True
nick = "Player"

# there are some pattenrs of snake
#len 10
extra_snake = [[height-9, 1, 'down'], [height-8, 1, 'down'], [height-7, 1, 'down'],
				[height-6, 1, 'down'], [height-5, 1, 'down'], [height-4, 1, 'down'],
				[height-3, 1, 'down'], [height-2, 1, 'right'], [height-2, 2, 'right'],
				[height-2, 3, 'right']]
#len 3
base_snake = [[height-2, 1, 'right'], [height-2, 2, 'right'], [height-2, 3, 'right']]
current_snake = base_snake

mul_coef = 0.9
def mul_speed(score, coef=mul_coef):
	return start_tickrait/(score*coef)

def sub_speed(score):
	return start_tickrait - (start_tickrait * score) / (min([height, width])*5)

current_change_speed = sub_speed


class RootLayout(BoxLayout):		# Main widget, all wigets stacked on him
	def __init__(self, **kwargs):
		super(RootLayout, self).__init__(**kwargs)


class SnakePanel(Label):			# Widget for cell of snake screen
	pass


class MySettings(Popup):			# Settings
	def set_settings(self):
		global empty_color, tor, nick, music, ai, food_color, body_color, head_color, audio
		# colors
		empty_color = self.field_color.text.split(', ')
		body_color = self.body_color.text.split(', ')
		head_color = self.head_color.text.split(', ')
		food_color = self.food_color.text.split(', ')
		# misc
		tor = self.tor_enabled.active
		ai = self.ai_enabled.active
		nick = self.player_nickname.text
		audio = self.audio_enabled.active

		self.dismiss()


class Snake:
	def __init__(self, snake=current_snake):
		self.snake = deepcopy(snake)
		self.map = [[0 for i in range(width)] for i in range(height)]
		self.food = None
		self.score = 0
		self.spawn_food()

	def get_map_status(self):	# update map with values for panels colors
		for i in range(height):
			for j in range(width):
				self.map[i][j] = 0 # Cleaning curent status

		for i in range(len(self.snake)-1):
			self.map[self.snake[i][0]][self.snake[i][1]] = 1 # marking body

		self.map[self.snake[-1][0]][self.snake[-1][1]] = 2	# marking head

		if self.food != None:
			self.map[self.food[0]][self.food[1]] = 3	# 3 marking food

		return self.map

	def move(self):		# move snake by 1 tick
		for i in range(len(self.snake)):
			self.snake[i][0], self.snake[i][1] = Snake.get_next_cell(self.snake[i])
			if i + 1 < len(self.snake):
				self.snake[i][2] = self.snake[i+1][2]

	def spawn_food(self):	# Creates food by adding it on snake's map
		if len(self.snake) >= width*height:
			return
		x, y = randint(0, width-1), randint(0, height-1)
		status = self.get_map_status()
		while status[y][x] != 0:
			x, y = randint(0, width-1), randint(0, height-1)
		print('food spawned')
		self.map[y][x] = 3
		self.food = (y, x)

	@classmethod
	def get_next_cell(self, cell):
		if cell[2] == 'right':
			if (tor and (cell[1]+1 >= width)):
				return cell[0], 0
			else:
				return cell[0], cell[1]+1
		elif cell[2] == 'left':
			if (tor and (cell[1]-1 < 0)):
				return cell[0], width-1
			else:
				return cell[0], cell[1]-1
		elif cell[2] == 'up':
			if (tor and (cell[0]-1 < 0)):
				return height-1, cell[1]
			else:
				return cell[0]-1, cell[1]
		elif cell[2] == 'down':
			if (tor and (cell[0]+1 >= height)):
				return 0, cell[1]
			else:
				return cell[0]+1, cell[1]

	def is_game_over(self):
		y, x = Snake.get_next_cell(self.snake[-1])
		if not tor:
			return ((x < 0) or (x >= width) or (y < 0) or (y >= height))
		for i in range(len(self.snake)-1):
			y1, x1 = Snake.get_next_cell(self.snake[i])
			if ((x==x1) and (y==y1)):
				return True
		return False

	def eat(self):
		y, x = Snake.get_next_cell(self.snake[-1])
		if ((y == self.food[0]) and (x == self.food[1])):
			self.food = None
			self.snake.append([y, x, self.snake[-1][2]])
			self.score += 1
			self.spawn_food()
			return True
		return False


class SnakeScreen(GridLayout):		# Widget for snake playground
	def __init__(self, **kwargs):
		super(SnakeScreen, self).__init__(**kwargs)

		self.snake = Snake()
		self.panels = [[] for i in range(height)]
		self.cols = width
		self.rows = height
		self.height = 20
		self.spacing = 1
		num = ""
		for i in range(height):
			for j in range(width):
				if enumerate_:
					num = f"{i} {j}"
				self.panels[i].append(SnakePanel(text=num))
				self.add_widget(self.panels[i][j])
		self.redraw()

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
				elif (status[i][j] == 3):
					self.panels[i][j].background_color = food_color


class SnakeApp(App):
	def build(self):
		root = RootLayout()
		self.root = root
		self.tickrait = start_tickrait
		self.snake_screen = root.snake_screen
		self.snake = self.snake_screen.snake
		self.top_5 = [0, 0, 0, 0, 0]
		self.started = False	# Variable that show started timer or not
		Window.bind(on_key_down=self.controls)
		with open("scores.json", "r") as file:
			self.data = json.load(file)
		self.root.top_5_label.text = self.get_top_5() 

		return root

	def msg(self, text):		# Update text on message label
		self.root.message_label.text = text

	def get_top_5(self):
		scores = self.data["top_5_scores"]
		names = self.data["top_5_names"]
		result = f'''Top 5 scores\n\n1. {names[0]} - {scores[0]}\n\n2. {names[1]} - {scores[1]}\n\n3. {names[2]} - {scores[2]}\n\n4. {names[3]} - {scores[3]}\n\n5. {names[4]} - {scores[4]}'''
		return result

	def game_over(self):
		score = self.stop()
		scores = self.data["top_5_scores"]
		names = self.data["top_5_names"]
		if scores[4] < score:
			scores[4] = score
			names[4] = nick
			for i in range(4):
				i = 4-i
				if scores[i] > scores[i-1]:
					scores[i], scores[i-1] = scores[i-1], scores[i]
					names[i], names[i-1] = names[i-1], names[i]
					print('swaped', i)
			self.root.top_5_label.text = self.get_top_5()
			with open("scores.json", "w") as file:
				json.dump(self.data, file)
		self.msg("Game over :(")

	def start(self):			# Start timer
		if not self.started:
			self.started = True
			self.root.score_label.text = f"Score = {self.snake.score}"
			Clock.schedule_interval(self.update, self.tickrait)
			print('timer started!')
			self.msg("Game started!")

	def stop(self):				# Stop timer
		if self.started:
			Clock.unschedule(self.update)
			print('timer stoped')
			self.started = False
			score = self.snake.score
			self.snake_screen.snake = Snake()
			self.snake = self.snake_screen.snake
			return score

	def change_speed(self):
		Clock.unschedule(self.update)
		Clock.schedule_interval(self.update, current_change_speed(self.snake.score))

	def update(self, _):		# Function for timer update
		if self.snake.is_game_over():
			self.game_over()
			return
		food_eated = self.snake.eat()
		if food_eated:
			self.root.score_label.text = f"Score = {self.snake.score}"
			self.msg("+1!")
			self.change_speed()
		else:
			self.snake.move()
			msg_text = self.snake.snake[-1][2]
			msg_text = msg_text[0].upper() + msg_text[1:]
			self.msg(msg_text)
		print(self.snake.map)
		print(self.snake.snake)
		self.snake_screen.redraw()

	def controls(self, event, keyboard, keycode, text, modifiers): # Key events
		snake = self.snake.snake
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
