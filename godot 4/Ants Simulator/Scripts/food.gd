extends Area2D

var health = 100


func _on_body_entered(body):
	if body.is_in_group("ants") and body.carrying_food == false:
		health -= 1
		body.carrying_food = true
		if health <= 0:
			queue_free()
