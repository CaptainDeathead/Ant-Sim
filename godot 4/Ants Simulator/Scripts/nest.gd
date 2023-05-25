extends Area2D

var ant = preload("res://ant.tscn")
var food = preload("res://food.tscn")

func _ready():
	for i in range(10):
		spawn_ant(i)
	for i in range(10):
		spawn_food()

func spawn_ant(id):
	var ant_instance = ant.instantiate()
	ant_instance.id = id
	ant_instance.add_to_group("ants")
	add_child(ant_instance)

func spawn_food():
	var food_instance = food.instantiate()
	food_instance.add_to_group("food")
	food_instance.position = Vector2(randf_range(-800, 800), randf_range(-600, 600))
	add_child(food_instance)
