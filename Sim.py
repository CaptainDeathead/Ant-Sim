import pygame
import random
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()

# Set the width and height of the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ant Simulation")

# Set up the clock for managing the frame rate
clock = pygame.time.Clock()

# Load the images
ant_sprite = pygame.image.load("Ant.png")
food_sprite = pygame.image.load("Food.png")
nest_sprite = pygame.image.load("Nest.png")

# Ant class
class Ant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.speed = 1  # Adjust the speed as needed
        self.direction = random.randint(0, 359)  # Random initial direction (angle)
        self.exploring = True  # Start by exploring
        self.food = 0
        self.time_away = 0
        self.sprite = ant_sprite

    def update(self):
        if self.exploring:
            self.decide()

        # Move the ant in the direction it's facing
        self.move()

        # Bound the ant within the screen
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

        # Increment time away
        self.time_away += 1

        # Check if the ant has been away for too long
        if self.time_away > 100000:
            self.die()

        print("Rotation: " + str(self.direction))

    def decide(self):
        # Generate a random number between 0 and 1
        random_number = random.random()

        # 30% chance to turn left
        if random_number < 0.3:
            self.turn_left()

        # 30% chance to turn right
        elif random_number < 0.6:
            self.turn_right()

        # 40% chance to keep moving straight
        else:
            pass  # Do nothing, continue moving straight

    def move(self):
        # Calculate the movement vector based on the direction
        velocity_x = math.cos(math.radians(self.direction))
        velocity_y = math.sin(math.radians(self.direction))

        # Update the position using the movement vector
        self.x += self.speed * velocity_x
        self.y += self.speed * velocity_y
        self.rect.center = (self.x, self.y)

    def turn_left(self):
        self.direction = (self.direction - 20) % 360

    def turn_right(self):
        self.direction = (self.direction + 20) % 360

    def draw(self, screen):
        rotated_sprite = pygame.transform.rotate(self.sprite, -self.direction + 90)
        rect = rotated_sprite.get_rect(center=(self.x, self.y))
        screen.blit(rotated_sprite, rect.topleft)

    def die(self):
        self.kill()  # Remove the ant from the sprite group

# Food class
class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = food_sprite
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.sprite = food_sprite

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Nest class
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

# Game class
class Game:
    def __init__(self):
        self.nest = pygame.sprite.Group()
        self.ants = pygame.sprite.Group()
        self.food = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.nest)

        self.add_nest(400, 300)

        for _ in range(10):
            self.spawn_new_food(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

        for _ in range(10):
            self.spawn_new_ant(400, 300)

    def run(self):
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update all sprites
            self.all_sprites.update()

            # Check for collisions between ants and food
            ant_food_collisions = pygame.sprite.groupcollide(
                self.ants, self.food, False, True
            )
            for ant, food_list in ant_food_collisions.items():
                ant.food += len(food_list)

            # Check for collisions between ants and the nest
            ant_nest_collisions = pygame.sprite.spritecollide(
                self.nest.sprites()[0], self.ants, False
            )
            for ant in ant_nest_collisions:
                if ant.food > 0:
                    ant.food -= 1
                    self.spawn_new_ant(400, 300)

            # Render the screen
            screen.fill(BLACK)
            self.all_sprites.draw(screen)
            pygame.display.flip()

            # Control the frame rate
            clock.tick(165)

        # Quit the game
        pygame.quit()

    def spawn_new_ant(self, x, y):
        ant = Ant(x, y)
        self.ants.add(ant)
        self.all_sprites.add(ant)

    def spawn_new_food(self, x, y):
        food = Food(x, y)
        self.food.add(food)
        self.all_sprites.add(food)

    def add_nest(self, x, y):
        nest = Nest(x, y)
        self.nest.add(nest)
        self.all_sprites.add(nest)

# Create an instance of the game and run it
game = Game()
game.run()