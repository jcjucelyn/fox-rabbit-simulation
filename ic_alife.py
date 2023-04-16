"""
Jocelyn Ju & Ceara Zhang
DS3500 // Predator Prey
HW05
14 April 2023
"""

# import necessary libraries
import random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import copy
import seaborn as sns
import argparse as ap
from matplotlib import colors

# SIZE = 50  # The dimensions of the field
fsize = 50
OFFSPRING = 2  # Max offspring when a rabbit reproduces
grass_rate = 0.025  # Probability that grass grows back at any location in the next season.
# establish necessary constants
WRAP = False  # Does the field wrap around on itself when rabbits move?


class Animal:
    """ A creature in a field searching for something to eat. This animal
     is adjustable with id, maximum offspring possible, speed at which it
     moves, amount of cycles before it starves, and what it eats"""

    def __init__(self, id, max_offspring, speed, starve, eats, fsize):
        """
        id : the id number of the animal
            empty ground = 0
            grass        = 1
            rabbit       = 2
            fox          = 3
        max_offspring: the maximum amount of offspring the animal can have
        speed: the maximum number of pixels that an animal can move in one cycle
        starve: the number of cycles an animal can go without eating
        eats: the id #s of the animal's food
        fsize: the size of the field
        """
        self.fsize = fsize
        self.x = rnd.randrange(0, self.fsize)
        self.y = rnd.randrange(0, self.fsize)
        self.eaten = 0
        self.id = id
        self.max_offspring = max_offspring
        self.speed = speed
        self.starve = starve
        self.cycle = 0
        self.eats = eats

    def reproduce(self):
        """ Make a new animal at the same location.
         Reproduction is hard work! Each reproducing
         rabbit's eaten level is reset to zero. """
        self.eaten = 0
        return copy.deepcopy(self)

    def eat(self, amount):
        """Feed the animal, taking in the amount"""
        self.eaten += amount
        if self.id == 3:
            print(self.id, self.eaten)

    def move(self):
        """ Move up, down, left, right randomly """
        max_move = self.speed + 1
        min_move = max_move * -1 + 1
        move_list = [i for i in range(min_move, max_move)]

        # account for the field wrapping around
        if WRAP:
            self.x = (self.x + rnd.choice(move_list)) % self.fsize
            self.y = (self.y + rnd.choice(move_list)) % self.fsize
        else:
            self.x = min(self.fsize-1, max(0, (self.x + rnd.choice(move_list))))
            self.y = min(self.fsize-1, max(0, (self.y + rnd.choice(move_list))))

    def survive(self):
        """ Returns whether the animal will survive that cycle
        taking into account the number of cycles the animal can
        go without starving """
        # if the animal ate that cycle, reset counter to 0
        if self.eaten > 0:
            self.cycle = 0
            return True

        # if the animal has gone too many cycles without eating, return "False"
        else:
            if self.cycle < self.starve:
                self.cycle += 1
                return True
            else:
                return False


class Field:
    """ A field is a patch of grass with 0 or more rabbits and foxes
     roaming around in search of food """

    def __init__(self, size, grass_rate):
        """ Create a patch of grass with dimensions fsize x fsize
        and initially no animals

        animals : a list of the animals in the field
        nrabbits: a list of the number of rabbits at each generation
        nfoxes: a list of the number of foxes at each generation
        ngrass: a list of the number of grass pixels at each generation
        size: the size of the visualization
        field: an array of none of size (size x size)
        grass_rate: the probability that grass grows back at any given
            location the next season
        """
        self.animals = []
        self.nrabbits = []
        self.nfoxes = []
        self.ngrass = []
        self.size = size
        self.field = np.ones(shape=(self.size, self.size), dtype=int)
        self.grass_rate = grass_rate

    def add_animal(self, animal):
        """ Add a new animal to the field """
        self.animals.append(animal)
        self.field[animal.x][animal.y] = animal.id
        print(f"Added animal {animal.id} at ({animal.x}, {animal.y})")
        print(self.field)

    def move(self):
        """ Animals move """
        for r in self.animals:
            r.move()

    # def eat(self):
    #     """ Animals eat (if they find grass where they are) """
    #     for animal in self.animals:
    #         self.field[animal.x, animal.y] = animal.id
    #
    #         if self.field[animal.x, animal.y] in animal.eats: # rabbit eating grass
    #             animal.eat(self.field[animal.x, animal.y])
    #             self.field[animal.x, animal.y] = 0
    def eat(self):
        """ Animals eat (if they find grass where they are) """
        for animal in self.animals:
            for other in self.animals:
                if other != animal and other.id in animal.eats and animal.x == other.x and animal.y == other.y:
                    # animal can eat other_animal
                    #print(f"Animal {animal.id} found food at ({animal.x}, {animal.y})")
                    animal.eat(other.id)
                    self.field[animal.x][animal.y] = animal.id
                    print("fox eating rabbit")
            # if self.field[animal.x][animal.y] in animal.eats:
            #     if animal.id == 2:
            #         animal.eat(self.field[animal.x][animal.y])
            #         self.field[animal.x][animal.y] = 0

            # if the thing at the current position is what the animal
            # eats, then animal will eat the thing and the current
            # position becomes whatever the animal is
            if self.field[animal.x][animal.y] in animal.eats:
                #print(f"Animal {animal.id} found food at ({animal.x}, {animal.y})")

                if animal.id == 3:
                    animal.eat(self.field[animal.x][animal.y])
                    self.field[animal.x][animal.y] = animal.id
                    print(f"Fox {animal.id} is eating Rabbit")
                else:
                    animal.eat(self.field[animal.x][animal.y])
                    self.field[animal.x][animal.y] = 0
                    # print(f"Bunny {animal.id} is eating grass")

    def survive(self):
        """ Animals who eat may live to eat another day, depending on their cycle survivals """
        self.animals = [r for r in self.animals if r.survive()]

    def reproduce(self):
        """ Animals reproduce if they have eaten """
        reproduce_anim = [animal for animal in self.animals if animal.eaten > 0]
        born = [animal.reproduce() for animal in reproduce_anim for _ in range(rnd.randint(0, animal.max_offspring))]
        self.animals.extend(born)

        # Capture field state for historical tracking
        # capture the number of rabbits
        if 2 in self.num_animals():
            self.nrabbits.append(len(self.num_animals()[2]))
        else:
            self.nrabbits.append(0)

        # capture the number of foxes
        if 3 in self.num_animals():
            self.nfoxes.append(len(self.num_animals()[3]))
        else:
            self.nfoxes.append(0)

        # capture the grass amount
        self.ngrass.append(self.amount_of_grass())

    def grow(self):
        """ Grass grows back with some user-inputted probability """
        growloc = (np.random.rand(self.size, self.size) < self.grass_rate) * 1
        self.field = np.maximum(self.field, growloc)

    def get_animals(self, id):
        """2D array where each element represents presence/absence of animal w/ ID"""
        animals = np.zeros(shape=(self.size, self.size), dtype=int)
        for r in self.animals:
            if r.id == id:
                animals[r.x, r.y] = r.id
        return animals

    def num_animals(self):
        """ How many animals are there in the field?"""
        num_dict = {}

        # add empty lists to the dict for each id present
        for r in self.animals:
            num_dict[r.id] = []

        # add the animal to its respective list in the dict
        for r in self.animals:
            num_dict[r.id] += [r]

        # return the dictionary
        return num_dict

    def amount_of_grass(self):
        """How much grass is there?"""
        return self.field.sum()

    def generation(self):
        """ Run one generation of rabbits """
        self.eat()
        self.move()
        self.survive()
        self.reproduce()
        self.grow()

    def history(self, showTrack=True, showPercentage=True, marker='.'):
        """ Keep track of and store the history of the field as a png
        Input:
            showTrack (Boolean): whether to connect points or not
            showPercentage (Boolean): whether to display the values of each animal
                    in terms of percentage of the maximum values
            marker (str): what marker to use for the plot

        Return:
            a plot of the number of animals and grass over time saved as a png
        """
        # set the size and labels of the plot
        plt.figure(figsize=(6, 6))
        plt.xlabel("Generations")
        plt.ylabel("% Organisms")

        # obtain the rabbits' scale through identifying the
        # maximum value and setting it to 100%
        xs = self.nrabbits[:]
        if showPercentage:
            maxrabbit = max(xs)
            xs = [x / maxrabbit for x in xs]

        # obtain the foxes' scale through identifying the
        # maximum value and setting it to 100%
        xf = self.nfoxes[:]
        if showPercentage:
            maxfox = max(xf)
            xf = [x / maxfox for x in xf]

        # obtain the grass' scale through identifying the
        # maximum value and setting it to 100%
        ys = self.ngrass[:]
        if showPercentage:
            maxgrass = max(ys)
            ys = [y / maxgrass for y in ys]

        # create the x-axis of generations
        xli = [_ for _ in range(len(xf))]

        # plot connected lines if showTrack
        if showTrack:
            plt.plot(xli, xf, marker=marker)
            plt.plot(xli, xs, marker=marker)
            plt.plot(xli, ys, marker=marker)
        # and a scatterplot if not showTrack
        else:
            plt.scatter(xli, xf, marker=marker)
            plt.scatter(xli, xs, marker=marker)
            plt.scatter(xli, ys, marker=marker)

        plt.grid()

        # add the title and legend to the plot
        plt.title("Foxes vs. Rabbits vs. Grass: GROW_RATE =" + str(self.grass_rate))
        plt.legend(['Foxes', 'Rabbits', 'Grass'])
        plt.savefig("history.png", bbox_inches='tight')
        plt.show()


def animate(i, field, im):
    """
    Animate the field of rabbits and foxes
    Input:
        i (int): the iteration/generation
        field (field): the field for which to simulate for
        im (image): the image to output

    Return:
        im (image) an updated image
    """
    # stopping criterion of 1000 iterations
    while i <= 1000:
        field.generation()
        # print("AFTER: ", i, np.sum(field.field), len(field.nfoxes))
        im.set_array(field.field)
        rabbits = field.get_animals(2)
        foxes = field.get_animals(3)
        total = np.maximum(field.field, np.maximum(rabbits, foxes))
        im = plt.imshow(total, cmap=my_cmap, interpolation='none', vmin=0, vmax=4)
        plt.title("generation = " + str(i))
        return im,


# make a custom color map where
#       0 Unoccupied = white
#       1 Grass      = green
#       2 Rabbits    = blue
#       3 Foxes      = red

clist = ['white', 'green', 'blue', 'red']
my_cmap = colors.ListedColormap(clist)


def main():
    # create a parser to support command-line arguments
    # parser = ap.ArgumentParser()
    #
    # # add grass growth rate, fox k value, field size, num initial foxes and rabbits
    # parser.add_argument('grass_growth', type=float,
    #                     help='the probability that grass grows back at any location in the next season')
    # parser.add_argument('fox_k', type=int,
    #                     help='the number of generations a fox can go without eating')
    # parser.add_argument('field_size', type=int,
    #                     help='the size of the field')
    # parser.add_argument('init_fox', type=int,
    #                     help='the starting amount of foxes')
    # parser.add_argument('init_rabbit', type=int,
    #                     help='the starting amount of rabbits'),
    # args = parser.parse_args()
    #
    # # assign variables to the inputs
    # grass_rate = args.grass_growth
    # fox_k = args.fox_k
    # fsize = args.field_size
    # init_fox = args.init_fox
    # init_rabbit = args.init_rabbit
    #
    # # Create the ecosystem
    # field = Field(fsize, grass_rate)
    #
    # # add rabbits (id, max_offspring, speed, starve, eats, fsize)
    # for _ in range(init_rabbit):
    #     field.add_animal(Animal(2, 1, 1, 1, (1,), fsize))
    #
    # # add foxes (id, max_offspring, speed, starve, eats, fsize)
    # # with user inputs for fox_k and fsize
    # for _ in range(init_fox):
    #     field.add_animal(Animal(3, 1, 1, fox_k, (2,), fsize))

    # Create the ecosystem
    field = Field(fsize, grass_rate)

    # # add rabbit
    # for _ in range(5):
    #     field.add_animal(Animal(2, 3, 1, 2, (1,), fsize))
    #
    # # add fox
    # for _ in range(10):
    #     field.add_animal(Animal(3, 1, 2, 75, (2,), fsize))
    #
    #     #(id, max_offspring, speed, starve, eats, fsize):

    for _ in range(10):
        rabbit = Animal(2, 2, 1, 1, (1,), fsize)
        field.add_animal(rabbit)
        field.field[rabbit.x][rabbit.y] = 2

    # add foxes
    for _ in range(1):
        fox = Animal(3, 1, 2, 15, (2, ), fsize)
        field.add_animal(fox)
        field.field[fox.x][fox.y] = 3

    # create the initial array of grass (value = 1)
    array = np.ones(shape=(fsize, fsize), dtype=int)

    # plot the figure
    fig = plt.figure(figsize=(5, 5))
    rabbits = field.get_animals(2)
    foxes = field.get_animals(3)
    total = np.maximum(array, np.maximum(rabbits, foxes))
    im = plt.imshow(total, cmap=my_cmap, interpolation='none', vmin=0, vmax=3)
    # animate the figure
    anim = animation.FuncAnimation(fig, animate, fargs=(field, im,), frames=1000000, interval=1, repeat=True)

    # display the plot and save the history
    plt.show()
    field.history()


if __name__ == '__main__':
    main()

"""
SOURCES:

help with parsers- https://docs.python.org/3/library/argparse.html 
help with command line- https://tacc.github.io/ctls2017/docs/intro_to_python/intro_to_python_101_argparse.html 
"""
