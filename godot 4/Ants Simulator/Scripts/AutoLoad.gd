extends Node

var nest_pheromone_trails = []
var food_pheromone_trails = []
var closest_food = null
var closest_nest = null
var closest_distance = 1000000
var closest_checkpoint = null
var distance = 0

func find_trail(id, type):
	if type == "nest":
		for trail in nest_pheromone_trails:
			if trail.id == id:
				return trail
	else:
		for trail in food_pheromone_trails:
			if trail.id == id:
				return trail

func find_closest_food(pos):
	closest_food = null
	closest_distance = 1000000
	for food in food_pheromone_trails:
		distance = find_closest_checkpoint(pos, food)
		if distance < closest_distance:
			closest_food = food
			closest_distance = distance
	return closest_food

func find_closest_nest(pos):
	closest_nest = null
	closest_distance = 1000000
	for nest in nest_pheromone_trails:
		distance = find_closest_checkpoint(pos, nest)
		if distance < closest_distance:
			closest_nest = nest
			closest_distance = distance
	return closest_nest

func find_closest_checkpoint(pos, checkpoints):
	closest_checkpoint = null
	closest_distance = 1000000
	for checkpoint in checkpoints:
		distance = pos.distance_to(checkpoint.position)
		if distance < closest_distance:
			closest_checkpoint = checkpoint
			closest_distance = distance
	return closest_distance
