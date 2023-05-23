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
        self.speed = 10
        self.food_collected = 0
        self.food_carried = 0
        self.carries_food = False
        self.sprite = ant_sprite
        
        self.freedom = 0.3
        
        self.food_trail_intensity = 255  # Intensity of food trail pheromone
        self.nest_trail_intensity = 255  # Intensity of nest trail pheromone

    def think(self, food_trails, nest_trails):
        if random.random() < self.freedom:
        # The ant wants to venture on its own
        self.move()
        self.turn_random()

    else:
        # The ant follows food or nest trails
        closest_food_trail = self.find_closest_trail(self.rect.center, food_trails)
        closest_nest_trail = self.find_closest_trail(self.rect.center, nest_trails)

        if closest_food_trail and closest_nest_trail:
            # Decide whether to follow food or nest trail based on their intensities and distances
            food_trail, food_intensity = closest_food_trail
            nest_trail, nest_intensity = closest_nest_trail

            food_distance = self.distance_to_trail(self.rect.center, food_trail)
            nest_distance = self.distance_to_trail(self.rect.center, nest_trail)

            if food_intensity > nest_intensity and food_distance < nest_distance:
                self.follow_trail(food_trail, "food")
            else:
                self.follow_trail(nest_trail, "nest")

        elif closest_food_trail:
            self.follow_trail(closest_food_trail[0], "food")
        elif closest_nest_trail:
            self.follow_trail(closest_nest_trail[0], "nest")

    # Leave a trail behind
    self.leave_trail(food_trails, self.food_trail_intensity)
    self.leave_trail(nest_trails, self.nest_trail_intensity)


    def move(self):
        # Calculate the movement vector based on the direction
        velocity_x = math.cos(math.radians(self.direction))
        velocity_y = math.sin(math.radians(self.direction))

        # Update the position using the movement vector
        self.x += self.speed * velocity_x
        self.y += self.speed * velocity_y
        self.rect.center = (self.x, self.y)  # Update the rect position

    def turn_left(self):
        self.direction = (self.direction - 20) % 360

    def turn_right(self):
        self.direction = (self.direction + 20) % 360

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

    def leave_trail(self, trails, intensity):
        trail = (self.x, self.y)
        trails.append((trail, intensity))

    def follow_trail(self, trails, trail_type):
        if trails:
            closest_trail = None
            closest_distance = float("inf")
            for trail, intensity in trails:
                distance = abs(math.sqrt((self.x - trail[0])**2 + (self.y - trail[1])**2))
                if distance < closest_distance:
                    closest_trail = trail
                    closest_distance = distance
            if closest_trail:
                trail_x, trail_y = closest_trail
                direction = math.degrees(math.atan2(trail_y - self.y, trail_x - self.x))
                self.direction = direction

                # Adjust the trail intensity based on the trail type
                if trail_type == "food":
                    self.food_trail_intensity += 10
                    self.food_trail_intensity = min(self.food_trail_intensity, 255)
                elif trail_type == "nest":
                    self.nest_trail_intensity += 10
                    self.nest_trail_intensity = min(self.nest_trail_intensity, 255)

                # Leave a trail behind
                self.leave_trail(trails, intensity)

                # Move towards the trail
                self.move()

class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.sprite = food_sprite
        self.health = 100

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
        self.discovered_food = []
        self.food_trails = []  # List to store food trails
        self.nest_trails = []  # List to store nest trails

    def reset(self, pop_size):
        self.ants = pygame.sprite.Group()  # Clear the ants list
        self.food = pygame.sprite.Group()  # Clear the food list
        self.nest = pygame.sprite.Group()
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.nest)
        # Reset other variables or objects to their initial states
        self.add_food(random.randint(100, 1820), random.randint(100, 1000))
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
            ant.think(self.food_trails, self.nest_trails)
            food_collisions = pygame.sprite.spritecollide(ant, self.food, True)
            if food_collisions:
                if not ant.carries_food:
                    ant.carries_food = True
                    ant.food_carried += 2
                    print("Food carried: " + str(ant.food_carried))
                    # reduce the health of the food
                    for food in food_collisions:
                        food.health -= 1
                        if food.health <= 0:
                            self.food.remove(food)
                            for ant in self.ants:
                                ant.discovered_food.remove(food)
                        else:
                            for ant in self.ants:
                                ant.discovered_food.append(food)
                            
                else:
                    ant.food_carried += 1
                    

        for nest_sprite in self.nest.sprites():
            for ant in self.ants:
                if pygame.sprite.collide_rect(ant, nest_sprite) and ant.carries_food:
                    ant.carries_food = False
                    ant.food_collected += 1
                    print("Food collected and stored: " + str(ant.food_collected))
        
        # Update the trail intensities and fade them over time
        for trail, intensity in self.food_trails:
            self.food_trails.remove((trail, intensity))
            intensity -= 1
            if intensity > 0:
                self.food_trails.append((trail, intensity))
        
        for trail, intensity in self.nest_trails:
            self.nest_trails.remove((trail, intensity))
            intensity -= 1
            if intensity > 0:
                self.nest_trails.append((trail, intensity))

    def draw(self):
        self.screen.fill((0, 0, 0))
        for ant in self.ants:
            ant.draw(self.screen)
        for food in self.food:
            food.draw(self.screen)
        self.nest.draw(self.screen)
        # Draw the food trails
        for trail, intensity in self.food_trails:
            pygame.draw.circle(self.screen, (255, 0, 0), trail, intensity // 10)
        # Draw the nest trails
        for trail, intensity in self.nest_trails:
            pygame.draw.circle(self.screen, (0, 0, 255), trail, intensity // 10)
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
    pygame.init()
    ant_sim = AntSim()
    ant_sim.reset(10)  # Set the population size of ants
    while ant_sim.running:
        ant_sim.handle_events()
        ant_sim.update()
        ant_sim.draw()
        ant_sim.clock.tick(60)
    pygame.quit()
