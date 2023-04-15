import random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import copy
import seaborn as sns
import argparse as ap
from matplotlib import colors

SIZE = 50  # The dimensions of the field
fsize = 50
# OFFSPRING = 2  # Max offspring when a rabbit reproduces
GRASS_RATE = 0.025  # Probability that grass grows back at any location in the next season.
WRAP = False  # Does the field wrap around on itself when rabbits move?


class Field:
    """ A field is a patch of grass with 0 or more rabbits hopping around
    in search of grass """

    def __init__(self, size):
        """ Create a patch of grass with dimensions SIZE x SIZE
        and initially no rabbits """
        self.animals = []
        self.nrabbits = []
        self.nfoxes = []
        self.ngrass = []
        self.size = size
        # self.field = np.full(shape=(self.size, self.size), fill_value=2, dtype=int)
        self.field = np.ones(shape=(self.size, self.size), dtype=int)

    def add_animal(self, animal):
        """ A new animal is added to the field """
        self.animals.append(animal)

    def move(self):
        """ Animals move """
        for r in self.animals:
            r.move()

    # def eat(self):
    #     """ Animals eat (if they find grass where they are) """
    #     for animal in self.animals:
    #         # check pixel of field's current value
    #         if self.field[animal.x, animal.y] == animal.eats:
    #             # animal.eat(1)
    #             animal.eat(self.field[animal.x, animal.y])
    #             self.field[animal.x, animal.y] = 0

    def eat(self):
        """ Animals eat (if they find grass or rabbits where they are) """
        for animal in self.animals:
            # check pixel of field's current value
            if self.field[animal.x, animal.y] == animal.eats:
                if animal.eats == 1:  # rabbit eating grass
                    animal.eat(self.field[animal.x, animal.y])
                    self.field[animal.x, animal.y] = 0
                elif animal.eats == 2: # fox eating rabbit
                    for rabbit in self.animals:
                        if rabbit.id == 2 and rabbit.x == animal.x and rabbit.y == animal.y:
                            self.animals.remove(rabbit)
                            self.field[animal.x, animal.y] = 3
                        break
                    animal.eat(2)


    def survive(self):
        """ Rabbits who eat some grass live to eat another day """
        self.animals = [r for r in self.animals if r.animal_survive()]

    def reproduce(self):
        """ Rabbits reproduce like rabbits. """
        born = [animal.reproduce() for animal in self.animals for _ in range(rnd.randint(0, animal.max_offspring))]
        # born = []
        # for animal in self.animals:
        #     for _ in range(rnd.randint(1, animal.max_offspring)):
        #         born.append(animal.reproduce())
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
        """ Grass grows back with some probability """
        growloc = (np.random.rand(self.size, self.size) < GRASS_RATE) * 1
        self.field = np.maximum(self.field, growloc)

    def get_animals(self):
        """2D array where each element represents presence/absence of animal w/ ID"""
        animals = np.ones(shape=(self.size, self.size), dtype=int)
        for r in self.animals:
            animals[r.x, r.y] = r.id
        return animals

    def num_animals(self):
        """ How many animals are there in the field?"""
        num_dict = {}

        # add empty lists to the dict for each id present
        for r in self.animals:
            num_dict[r.id] = []

        for r in self.animals:
            num_dict[r.id] += [r]
        return num_dict

    def amount_of_grass(self):
        """How much grass is there?"""
        return self.field.sum()

    def generation(self):
        """ Run one generation of rabbits """
        self.move()
        self.eat()
        self.survive()
        self.reproduce()
        self.grow()

    def history(self, showTrack=True, showPercentage=True, marker='.'):
        xs = self.nrabbits[:]
        if showPercentage:
            maxrabbit = max(xs)
            xs = [x / maxrabbit for x in xs]
            plt.xlabel("% Rabbits")

        xf = self.nfoxes[:]
        if showPercentage:
            maxfox = max(xf)
            xf = [x / maxfox for x in xf]
            plt.xlabel("% Foxes")

        ys = self.ngrass[:]
        if showPercentage:
            maxgrass = max(ys)
            ys = [y / maxgrass for y in ys]
            plt.ylabel("% Rabbits")

        xli = [_ for _ in range(len(xf))]

        if showTrack:
            plt.plot(xli, xf, marker=marker, label='Foxes')
            plt.plot(xli, xs, marker=marker, label='Rabbits')
            plt.plot(xli, ys, marker=marker, label='Grass')
        else:
            plt.scatter(xli, xf, marker=marker, label='Foxes')
            plt.scatter(xli, xs, marker=marker, label='Rabbits')
            plt.scatter(xli, ys, marker=marker, label='Grass')

        plt.grid()

        plt.title("Foxes vs. Rabbits vs. Grass: GROW_RATE =" + str(GRASS_RATE))
        plt.legend()
        plt.savefig("history.png", bbox_inches='tight')
        plt.show()
        


class Animal:
    """ A furry creature roaming a field in search of grass to eat.
    Mr. Rabbit must eat enough to reproduce, otherwise he will starve. """

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
        """Feed the animal"""
        self.eaten += amount

    def move(self):
        """ Move up, down, left, right randomly """
        max_move = self.speed + 1
        min_move = max_move * -1 + 1
        move_list = [i for i in range(min_move, max_move)]

        if WRAP:
            self.x = (self.x + rnd.choice(move_list)) % self.fsize
            self.y = (self.y + rnd.choice(move_list)) % self.fsize
        else:
            self.x = min(self.fsize-1, max(0, (self.x + rnd.choice(move_list))))
            self.y = min(self.fsize-1, max(0, (self.y + rnd.choice(move_list))))

    def animal_survive(self):

        # if the animal ate that cycle, reset counter to 0
        if self.eaten > 0:
            self.cycle = 0
            return True
        else:
            # if the animal has gone too many cycles without eating, return "False"
            if self.cycle <= self.starve:
                self.cycle += 1
                return True
            else:
                return False





def animate(i, field, im):

    while i <= 100:
        field.generation()
        # print("AFTER: ", i, np.sum(field.field), len(field.rabbits))
        im.set_array(field.field)
        plt.title("generation = " + str(i))
        return im,




# make a custom color map where
#       Unoccupied = white
#       Grass      = green
#       Rabbits    = blue
#       Foxes      = red
# ccm = colors.LinearSegmentedColormap.from_list('fox-rabbit-cm', ['white', 'red', 'blue', 'green'])
# size = (fsize, fsize)
# field = np.random.randint(0, 2, size, dtype=int)          # 1 = grass, 0 = bare earth
# rabbits = np.random.randint(0, 2, size, dtype=int) * 2  # 2 = rabbit
# foxes = np.random.randint(0, 2, size, dtype=int) * 3   # 3 = foxes
#
# total = np.maximum(field, np.maximum(rabbits, foxes))
# print(field, "\n\n", rabbits, "\n\n", foxes, "\n\n", total)


#clist = ['white', 'red', 'blue', 'green']
# clist = ['red', 'purple', 'green']
# clist = ['blue', 'red', 'white', 'green']
clist = ['blue', 'red', 'white', 'green']
my_cmap = colors.ListedColormap(clist)

# plt.imshow(total, cmap=my_cmap, interpolation='none')
# plt.show()



def main():
    # parser = ap.ArgumentParser()
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
    # grass_rate = args.grass_growth
    # fox_k = args.fox_k
    # fsize = args.field_size
    # init_fox = args.init_fox
    # init_rabbit = args.init_rabbit
    #
    # Create the ecosystem
    field = Field(fsize)

    # # id, max_offspring, speed, starve, eats, fsize
    # for _ in range(init_rabbit):
    #     field.add_rabbit(Rabbit(2, 1, 1, 1, (1,), fsize))
    #
    # # add fox
    # for _ in range(init_fox):
    #     field.add_rabbit(Rabbit(3, 1, 1, fox_k, (2,), fsize))

    # add rabbit
    for _ in range(10):
        field.add_animal(Animal(2, 2, 1, 2, (1,), fsize))

    # add fox
    for _ in range(10):
        field.add_animal(Animal(3, 1, 2, 10, (2,), fsize))

        #(id, max_offspring, speed, starve, eats, fsize):

    array = np.zeros(shape=(fsize, fsize), dtype=int)
    fig = plt.figure(figsize=(5, 5))
    im = plt.imshow(array, cmap=my_cmap, interpolation='hamming', aspect='auto', vmin=0.5, vmax=1)
    anim = animation.FuncAnimation(fig, animate, fargs=(field, im,), frames=1000000, interval=1, repeat=True)
    plt.show()

    field.history()


if __name__ == '__main__':
    main()

"""
SOURCES:

help with parsers- https://docs.python.org/3/library/argparse.html 
"""
