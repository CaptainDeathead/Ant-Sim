import pygame
import random
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()

# Set the width and height of the screen
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ant Simulation")

# Set up the clock for managing the frame rate
clock = pygame.time.Clock()

# Load the images
ant_sprite = pygame.image.load("Ant.png")
food_sprite = pygame.image.load("Food.png")
nest_sprite = pygame.image.load("Nest.png")

class Ant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = ant_sprite
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.speed = 1  # Adjust the speed as needed
        self.direction = random.randint(0, 359)  # Random initial direction (angle)
        self.exploring = True  # Start by exploring
        self.carrying_food = False
        self.time_away = 0
        self.to_nest = []
        self.to_food = []
        self.following_trail = None
        self.wants_other_trail = False

    def update(self):
        if self.exploring:
            self.add_checkpoint("nest")
            self.decide()
        else:
            if self.carrying_food:
                self.add_checkpoint("food")
                self.follow_trail(self.to_nest)
            else:
                self.add_checkpoint("nest")
                self.follow_trail(self.to_food)

        # Move the ant in the direction it's facing if it's exploring
        if self.exploring:
            self.move()

        # Bound the ant within the screen
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

        # Increment time away
        self.time_away += 1

        # Check if the ant has been away for too long
        if self.time_away > 100000:
            self.die()

        # Rotate the image based on the current direction
        self.image = pygame.transform.rotate(self.original_image, -self.direction - 90)

    def decide(self):
        random_number = random.random()

        if self.time_away > 1000:
            # 15% chance to follow another ant's food trail
            if random_number < 0.15:
                self.wants_other_trail = True
        else:
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
        for _ in range(random.randint(0, 10)):
            self.direction = (self.direction - 1) % 360

    def turn_right(self):
        for _ in range(random.randint(0, 10)):
            self.direction = (self.direction + 1) % 360

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, -self.direction)
        rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, rect.topleft)

    def die(self):
        self.kill()  # Remove the ant from the sprite group

    def add_checkpoint(self, checkpoint):
        if checkpoint == "nest":
            self.to_nest.append((self.x, self.y))
        elif checkpoint == "food":
            self.to_food.append((self.x, self.y))

    def follow_trail(self, trail):
        if len(trail) > 0:
            min_distance = float("inf")
            closest_checkpoint = None
            for checkpoint in trail:
                distance = abs(math.sqrt((self.x - checkpoint[0]) ** 2 + (self.y - checkpoint[1]) ** 2))
                if distance < min_distance:
                    min_distance = distance
                    closest_checkpoint = checkpoint

            if closest_checkpoint is not None:
                self.direction = (math.degrees(math.atan2(self.y - closest_checkpoint[1], self.x - closest_checkpoint[0]))) - 180
                self.move()
                self.rect.center = (self.x, self.y)

                if self.rect.collidepoint(closest_checkpoint):
                    trail.remove(closest_checkpoint)
                
                self.following_trail = trail
        else:
            self.to_food = []
            self.to_nest = []
            self.exploring = True
            self.wants_other_trail = False
            print("Trail finished")

    def follow_random_trail(self, ants):
        min_distance = float("inf")
        closest_trail = None

        for ant in ants:
            if ant.to_food:
                distance = math.sqrt((self.x - ant.x) ** 2 + (self.y - ant.y) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    closest_trail = ant.to_food.copy()

        if closest_trail:
            self.to_food = closest_trail
            self.following_trail = self.to_food
            self.exploring = False
            self.wants_other_trail = False

# Food class
class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = food_sprite
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.sprite = food_sprite
        self.health = 100

    def kill(self):
        super().kill()

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

        self.add_nest(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        for _ in range(10):
            self.spawn_new_food(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

        for _ in range(10):
            self.spawn_new_ant(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def run(self):
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for ant in self.ants:
                if ant.wants_other_trail:
                    ant.follow_random_trail(self.ants)

            # Update all sprites
            self.all_sprites.update()

            # Check for collisions between ants and food
            ant_food_collisions = pygame.sprite.groupcollide(
                self.ants, self.food, False, False
            )
            for ant, food_list in ant_food_collisions.items():
                if ant.carrying_food:
                    continue
                else:
                    ant.carrying_food = True
                    ant.exploring = False
                    ant.time_away = 0
                    ant.speed = 0.5
                    ant.to_food = []
                    food_list[0].health -= 1
                    if food_list[0].health <= 0:
                        food_list[0].kill()
                    

            # Check for collisions between ants and the nest
            ant_nest_collisions = pygame.sprite.spritecollide(
                self.nest.sprites()[0], self.ants, False
            )
            for ant in ant_nest_collisions:
                if ant.carrying_food:
                    ant.carrying_food = False
                    ant.exploring = True
                    ant.time_away = 0
                    ant.speed = 1
                    ant.to_nest = []
                    #self.spawn_new_ant(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    #self.spawn_new_food(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

            # Render the screen
            screen.fill(BLACK)
            self.all_sprites.draw(screen)
            pygame.display.flip()

            # Control the frame rate
            clock.tick(500)

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