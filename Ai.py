import neat
import World
import random
import time

class Ai:
    def __init__(self, config):
        self.fitness_values = []
        self.config = config
        self.world = World.AntSim()
        self.world.add_food(random.randint(0, 800), random.randint(0, 600))
        self.world.add_nest(400, 300)
        self.genomes = []
        self.pop_size = self.config.pop_size  # Get the population size from the config
        for i in range(self.pop_size):
            self.world.add_ant(400, 300, 0)
            self.genomes.append(neat.DefaultGenome(0))

    def run(self):
        p = neat.Population(self.config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        p.add_reporter(neat.Checkpointer(5))
        winner = p.run(self.eval_genomes, 1000)
        print("Best genome:\n{!s}".format(winner))

    def eval_genomes(self, genomes, config):
        self.train_ai(genomes)  # Train the AI
        max_food_carried = max(ant.food_carried for ant in self.world.ants.sprites())
        for genome_id, genome in genomes:
            genome.fitness = max_food_carried

    def train_ai(self, genomes):
        self.world.reset(self.pop_size)
        self.world.running = True
        start = time.time()
        while self.world.running:
            if time.time() - start > 10:
                self.world.running = False
                return

            ants = self.world.ants.sprites()  # Get the list of sprites from the 'ants' group
            for i, (_, genome) in enumerate(genomes):
                if len(ants) <= 1:
                    print("No ants")
                    self.world.running = False
                    return
                ant = ants[i % len(ants)]
                net = neat.nn.FeedForwardNetwork.create(genome, self.config)
                output = net.activate((ant.direction, ant.distance_to_food(self.world.food), ant.distance_to_nest(self.world.nest)))
                decision = output.index(max(output))  # Get the index of the highest output value
                if decision == 0:
                    ant.turn_left()
                elif decision == 1:
                    ant.turn_right()
                elif decision == 2:
                    pass
                ant.move()

                if ant.food_collected > 0:
                    ant.food_collected = 0
                    self.world.add_random_food()

            self.world.clock.tick(165)
            self.world.handle_events()
            self.world.update()
            self.world.draw()


if __name__ == "__main__":
    ai = Ai(neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, "config-feedforward.txt"))
    ai.run()
