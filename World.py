# The beginning of the ant-sim program
import pygame
import math
import random

ant_sprite = pygame.image.load("Ant.png")
food_sprite = pygame.image.load("Food.png")
nest_sprite = pygame.image.load("Nest.png")

class Ant(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()  # Create a rect attribute for collision detection
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 30
        self.food_collected = 0
        self.food_carried = 0
        self.carries_food = False
        self.sprite = ant_sprite

    def move(self):
        # Calculate the movement vector based on the direction
        velocity_x = math.cos(math.radians(self.direction))
        velocity_y = math.sin(math.radians(self.direction))

        # Update the position using the movement vector
        self.x += self.speed * velocity_x
        self.y += self.speed * velocity_y
        self.rect.center = (self.x, self.y)  # Update the rect position

    def turn_left(self):
        self.direction = (self.direction - 30) % 360

    def turn_right(self):
        self.direction = (self.direction + 30) % 360

    def draw(self, screen):
        rotated_sprite = pygame.transform.rotate(self.sprite, -self.direction + 90)
        rect = rotated_sprite.get_rect(center=(self.x, self.y))
        screen.blit(rotated_sprite, rect.topleft)

    def distance_to_food(self, food):
        min_distance = float("inf")
        for f in food.sprites():  # Iterate over the sprites in the 'food' group
            distance = abs(math.sqrt((self.x - f.x)**2 + (self.y - f.y)**2))
            if distance < min_distance:
                min_distance = distance
        return min_distance
    
    def distance_to_nest(self, nest):
        nest_sprite = nest.sprites()[0]  # Retrieve the sprite object from the 'nest' group
        return abs(math.sqrt((self.x - nest_sprite.x)**2 + (self.y - nest_sprite.y)**2))

class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.sprite = food_sprite

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

class Nest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = nest_sprite
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.sprite = nest_sprite

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class AntSim:
    def __init__(self):
        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.ants = pygame.sprite.Group()
        self.food = pygame.sprite.Group()
        self.nest = pygame.sprite.Group()
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.nest)

    def reset(self, pop_size):
        self.ants = pygame.sprite.Group()  # Clear the ants list
        self.food = pygame.sprite.Group()  # Clear the food list
        self.nest = pygame.sprite.Group()
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.nest)
        # Reset other variables or objects to their initial states
        self.add_food(random.randint(0, 1920), random.randint(0, 1080))
        self.add_nest(400, 300)
        for i in range(pop_size):
            self.add_ant(400, 300, 0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def update(self):
        for ant in self.ants.sprites():
            food_collisions = pygame.sprite.spritecollide(ant, self.food, True)
            if food_collisions:
                if not ant.carries_food:
                    ant.carries_food = True
                    ant.food_carried += 1
                    print("Food carried: " + str(ant.food_carried))
                    # Move the food sprite to a random position
                    food_sprite = Food(random.randint(0, 1920), random.randint(0, 1080))
                    self.food.add(food_sprite)  # Add the new food sprite to the group
                    

        for nest_sprite in self.nest.sprites():
            if pygame.sprite.collide_rect(ant, nest_sprite) and ant.carries_food:
                ant.carries_food = False
                ant.food_collected += 1
                print("Food collected and stored: " + str(ant.food_collected))


    def draw(self):
        self.screen.fill((0,0,0))
        for ant in self.ants:
            ant.draw(self.screen)
        for food in self.food:
            food.draw(self.screen)
        self.nest.draw(self.screen)
        pygame.display.flip()

    def add_ant(self, x, y, direction):
        ant = Ant(x, y, direction)
        self.ants.add(ant)
        self.all_sprites.add(ant)

    def add_nest(self, x, y):
        nest = Nest(x, y)
        self.nest.add(nest)
        self.all_sprites.add(nest)

    def add_food(self, x, y):
        food = Food(x, y)
        self.food.add(food)
        self.all_sprites.add(food)

    def add_random_food(self):
        self.add_food(random.randint(0, 1920), random.randint(0, 1080))

    def add_random_ant(self):
        self.add_ant(random.randint(0, 1920), random.randint(0, 1080), random.randint(0, 360))

    def add_random_nest(self):
        self.add_nest(random.randint(0, 1920), random.randint(0, 1080))

if __name__ == "__main__":
    exec(open("Ai.py").read())