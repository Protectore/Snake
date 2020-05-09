import json
import random

vision = 5
width = 1 + 2 * vision
height = width

defenition = {
	'up': 0,
	'down': 1,
	'left': 2,
	'right': 3
}

def load_weights():
	food_weights, wall_weights = None, None
	with open("data/food_weights.json", "r") as file:
		food_weights = json.load(file)
	with open("data/wall_weights.json", "r") as file:
		wall_weights = json.load(file)

	print("Weights loaded!")
	return food_weights, wall_weights

def save_weights(food_weights, wall_weights):
	with open("data/food_weights.json", "w") as file:
		json.dump(food_weights, file)

	with open("data/wall_weights.json", "w") as file:
		json.dump(wall_weights, file)

		print("Weights saved!")

def get_dirrection(active_cells, food_weights, wall_weights):
	mind_state = [0, 0, 0, 0]
	# up, down, left, right

	if active_cells != []:
		for i, j, type in active_cells:
			# for food
			if type == 3:
				for n in range(4):
					mind_state[n] += food_weights[i][j][n]
			# for walls
			else:
				for n in range(4):
					mind_state[n] += wall_weights[i][j][n]

	dirrection = [0]
	max_weight = mind_state[0]
	for i in range(1, 4):
		if mind_state[i] > max_weight:
			max_weight, dirrection = mind_state[i], [i]
		elif mind_state[i] == max_weight:
			dirrection.append(i)

	dirrection = random.choice(dirrection)
	if dirrection == 0:
		return 'up'
	elif dirrection == 1:
		return 'down'
	elif dirrection == 2:
		return 'left'
	else:
		return 'right'

def get_active_cells(map_status, visible_area):
	active_cells = []
	n = 0
	for i in range(height):
		for j in range(width):
			visible_area[n].extend([i, j])
			n += 1

	for i, j, y, x in visible_area:
		if map_status[i][j] == 1:
			active_cells.append([y, x, 1])
		elif map_status[i][j] == 3:
			active_cells.append([y, x, 3])

	return active_cells

def learn(food_weights, wall_weights, active_cells, choice, snake_choice):
	#active_cells = get_active_cells(map_status, visible_area)

	if snake_choice != choice:
		print(choice, snake_choice)
		print("Correcting weights...")
		for i, j, type in active_cells:
			if type == 3:
				food_weights[i][j][defenition[snake_choice]] -= 1
				food_weights[i][j][defenition[choice]] += 1
			else:
				wall_weights[i][j][defenition[snake_choice]] -= 1
				wall_weights[i][j][defenition[choice]] += 1
