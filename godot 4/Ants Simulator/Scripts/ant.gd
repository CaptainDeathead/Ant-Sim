extends CharacterBody2D

var speed = 30;
var carrying_food = false;
var exploring = true;
var moving_to_food = false;
var moving_to_nest = false;
var target = null;
var target_checkpoints = [];
var food_pheromones = [];
var nest_pheromones = [];
var id = 0;

var food_pheromone = preload("res://pheromone_food.tscn")
var nest_pheromone = preload("res://pheromone_nest.tscn")

func turn_left():
	rotation_degrees -= 10;
	rotation_degrees = int(rotation_degrees) % 360;
	rotation = rotation_degrees * PI / 180;
	print(rotation_degrees)

func turn_right():
	rotation_degrees += 10;
	rotation_degrees = int(rotation_degrees) % 360;
	rotation = rotation_degrees * PI / 180;
	print(rotation_degrees)

func go_to_food(target):
	moving_to_food = true;
	moving_to_nest = false;
	exploring = false;
	if target == null:
		target = AutoLoad.find_closest_food(position)
		if target == null:
			exploring = true
			return
		for checkpoint in target:
			target_checkpoints.append(checkpoint)
	else:
		var direction = target - position
		rotation = direction.angle()
		if position.distance_to(target) < 10:
			target_checkpoints.pop(0)
			if len(target_checkpoints) == 0:
				target = null
				target_checkpoints = []
			else:
				target = target_checkpoints[0]

func go_to_nest(target):
	moving_to_food = false;
	moving_to_nest = true;
	exploring = false;
	if target == null:
		target = AutoLoad.find_closest_nest(position)
		if target == null:
			exploring = true
			return
		for checkpoint in target:
			target_checkpoints.append(checkpoint)
	else:
		var direction = target - position
		rotation = direction.angle()
		if position.distance_to(target) < 10:
			target_checkpoints.pop(0)
			if len(target_checkpoints) == 0:
				target = null
				target_checkpoints = []
			else:
				target = target_checkpoints[0]

func _physics_process(delta):
	if exploring:
		# generate a random number between 0 and 1
		var random_number = randf()
		if random_number < 0.3:
			turn_left()
		elif random_number < 0.6:
			turn_right()
		else:
			pass
		print("exploring")
	elif moving_to_food:
		# follow pheromones
		go_to_food(target)
	elif moving_to_nest:
		# follow pheromones
		go_to_nest(target)
	else:
		var random_number = randf()
		if random_number < 0.8:
			exploring = true
		else:
			go_to_food(target)

	if carrying_food:
		moving_to_nest = true
		moving_to_food = false
		exploring = false

	# leave pheromones
	if moving_to_food:
		if len(food_pheromones) > 0:
			var distance_to_last_pheromone = position.distance_to(food_pheromones[-1].position)
			if distance_to_last_pheromone > 20:
				var pheromone = food_pheromone.instantiate()
				pheromone.position = position
				pheromone.strength = 60
				get_tree().get_root().add_child(pheromone)
				food_pheromones.append(pheromone)
				# replace the tail in the AutoLoad.food_pheromone_trails[<id>] with the updated trail
				if [id] in AutoLoad.food_pheromone_trails:
					AutoLoad.food_pheromone_trails[id] = food_pheromones
				else:
					AutoLoad.food_pheromone_trails.append(food_pheromones)
		else:
			var pheromone = food_pheromone.instantiate()
			pheromone.position = position
			pheromone.strength = 60
			get_tree().get_root().add_child(pheromone)
			food_pheromones.append(pheromone)
			# replace the tail in the AutoLoad.food_pheromone_trails[<id>] with the updated trail
			if [id] in AutoLoad.food_pheromone_trails:
				AutoLoad.food_pheromone_trails[id] = food_pheromones
			else:
				AutoLoad.food_pheromone_trails.append(food_pheromones)
	elif moving_to_nest:
		if len(nest_pheromones) > 0:
			var distance_to_last_pheromone = position.distance_to(nest_pheromones[-1].position)
			if distance_to_last_pheromone > 20:
				var pheromone = nest_pheromone.instantiate()
				pheromone.position = position
				pheromone.strength = 60
				get_tree().get_root().add_child(pheromone)
				nest_pheromones.append(pheromone)
				# replace the tail in the AutoLoad.nest_pheromone_trails[<id>] with the updated trail
				if [id] in AutoLoad.nest_pheromone_trails:
					AutoLoad.nest_pheromone_trails[id] = nest_pheromones
				else:
					AutoLoad.nest_pheromone_trails.append(nest_pheromones)
		else:
			var pheromone = nest_pheromone.instantiate()
			pheromone.position = position
			pheromone.strength = 60
			get_tree().get_root().add_child(pheromone)
			nest_pheromones.append(pheromone)
			# replace the tail in the AutoLoad.nest_pheromone_trails[<id>] with the updated trail
			if [id] in AutoLoad.nest_pheromone_trails:
				AutoLoad.nest_pheromone_trails[id] = nest_pheromones
			else:
				AutoLoad.nest_pheromone_trails.append(nest_pheromones)
	else:
		if len(food_pheromones) > 0:
			var distance_to_last_pheromone = position.distance_to(food_pheromones[-1].position)
			if distance_to_last_pheromone > 20:
				# leave moving_to_food pheromones
				var pheromone = food_pheromone.instantiate()
				pheromone.position = position
				pheromone.strength = 60
				get_tree().get_root().add_child(pheromone)
				food_pheromones.append(pheromone)
				# replace the tail in the AutoLoad.food_pheromone_trails[<id>] with the updated trail
				if [id] in AutoLoad.food_pheromone_trails:
					AutoLoad.food_pheromone_trails[id] = food_pheromones
				else:
					AutoLoad.food_pheromone_trails.append(food_pheromones)
		else:
			var pheromone = food_pheromone.instantiate()
			pheromone.position = position
			pheromone.strength = 60
			get_tree().get_root().add_child(pheromone)
			food_pheromones.append(pheromone)
			# replace the tail in the AutoLoad.food_pheromone_trails[<id>] with the updated trail
			if [id] in AutoLoad.food_pheromone_trails:
				AutoLoad.food_pheromone_trails[id] = food_pheromones
			else:
				AutoLoad.food_pheromone_trails.append(food_pheromones)

	velocity = Vector2(speed, 0).rotated(rotation - PI / 2)
	position += velocity * delta
	move_and_slide()

func _process(delta):
	for pheromone in food_pheromones:
		pheromone.strength -= 0.1
		if pheromone.strength <= 0:
			pheromone.queue_free()
			food_pheromones.erase(pheromone)

	for pheromone in nest_pheromones:
		pheromone.strength -= 0.1
		if pheromone.strength <= 0:
			pheromone.queue_free()
			nest_pheromones.erase(pheromone)
