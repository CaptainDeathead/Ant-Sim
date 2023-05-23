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

ant_sprite = "Ant.png"

# Set up the clock for managing the frame rate
clock = pygame.time.Clock()

# Ant class
class Ant(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.original_image = image
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.speed = 1  # Adjust the speed as needed
        self.food = 0
        self.time_away = 0
        self.direction = random.randint(0, 359)  # Random initial direction (angle)
        self.exploring = True  # Start by exploring

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
        self.rect.x += self.speed * velocity_x
        self.rect.y += self.speed * velocity_y

    def turn_left(self):
        self.direction = (self.direction - 20) % 360

    def turn_right(self):
        self.direction = (self.direction + 20) % 360

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.original_image, -self.direction + 90)
        screen.blit(rotated_image, self.rect)

    def die(self):
        self.kill()  # Remove the ant from the sprite group

# Food class
class Food(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

# Nest class
class Nest(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2

# Game class
class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.food_sprites = pygame.sprite.Group()
        self.ant_sprites = pygame.sprite.Group()
        self.nest = Nest(pygame.image.load("Nest.png").convert_alpha())
        self.all_sprites.add(self.nest)

        self.food_image = pygame.image.load("Food.png").convert_alpha()
        for _ in range(10):
            food = Food(self.food_image)
            self.all_sprites.add(food)
            self.food_sprites.add(food)

        self.ant_image = pygame.image.load("Ant.png").convert_alpha()
        for _ in range(10):
            self.spawn_new_ant()

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
                self.ant_sprites, self.food_sprites, False, True
            )
            for ant, food_list in ant_food_collisions.items():
                ant.food += len(food_list)

            # Check for collisions between ants and the nest
            ant_nest_collisions = pygame.sprite.spritecollide(
                self.nest, self.ant_sprites, False
            )
            for ant in ant_nest_collisions:
                if ant.food > 0:
                    ant.food -= 1
                    self.spawn_new_ant()

            # Render the screen
            screen.fill(BLACK)
            self.all_sprites.draw(screen)
            pygame.display.flip()

            # Control the frame rate
            clock.tick(60)

        # Quit the game
        pygame.quit()

    def spawn_new_ant(self):
        ant = Ant(self.ant_image)
        nest_rect = self.nest.rect
        nest_center = nest_rect.center
        spawn_radius = 30  # Adjust the spawn radius as desired

        # Generate a random displacement within the spawn radius
        displacement_x = random.uniform(-spawn_radius, spawn_radius)
        displacement_y = random.uniform(-spawn_radius, spawn_radius)

        # Set the ant's position around the nest with the displacement
        ant.rect.centerx = nest_center[0] + displacement_x
        ant.rect.centery = nest_center[1] + displacement_y

        ant.exploring = True  # Set the ant to exploring mode

        self.all_sprites.add(ant)
        self.ant_sprites.add(ant)

# Create an instance of the game and run it
game = Game()
game.run()
