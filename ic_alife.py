import random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import copy
import seaborn as sns
import argparse as ap
from matplotlib import colors

SIZE = 500  # The dimensions of the field
fsize = 500
# OFFSPRING = 2  # Max offspring offspring when a rabbit reproduces
GRASS_RATE = 0.025  # Probability that grass grows back at any location in the next season.
WRAP = False  # Does the field wrap around on itself when rabbits move?


class Rabbit:
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
        """ Make a new rabbit at the same location.
         Reproduction is hard work! Each reproducing
         rabbit's eaten level is reset to zero. """
        self.eaten = 0
        return copy.deepcopy(self)

    def eat(self, amount):
        """ Feed the rabbit some grass """
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

    def survive(self):
        # return whether the animal will survive that cycle
        self.cycle += 1

        # if the animal ate that cycle, reset counter to 0
        if self.eaten > 0:
            self.cycle = 0
            return True

        # if the animal has gone too many cycles without eating, return "False"
        if self.cycle <= self.starve:
            return True
        else:
            return False
        


class Field:
    """ A field is a patch of grass with 0 or more rabbits hopping around
    in search of grass """

    def __init__(self, size):
        """ Create a patch of grass with dimensions SIZE x SIZE
        and initially no rabbits """
        self.rabbits = []
        self.nrabbits = []
        self.nfoxes = []
        self.ngrass = []
        self.size = size
        # self.field = np.full(shape=(self.size, self.size), fill_value=2, dtype=int)
        self.field = np.ones(shape=(self.size, self.size), dtype=int)

    def add_rabbit(self, rabbit):
        """ A new rabbit is added to the field """
        self.rabbits.append(rabbit)

    def move(self):
        """ Rabbits move """
        for r in self.rabbits:
            r.move()

    def eat(self):
        """ Rabbits eat (if they find grass where they are) """
        # for rabbit in self.rabbits:
        #     rabbit.eat(self.field[rabbit.x, rabbit.y])
        #     self.field[rabbit.x, rabbit.y] = 0
        for animal in self.rabbits:
            # check pixel of field's current value
            if self.field[animal.x, animal.y] in animal.eats:
                animal.eat(self.field[animal.x, animal.y])
                self.field[animal.x, animal.y] = 0

    def survive(self):
        """ Rabbits who eat some grass live to eat another day """
        # self.rabbits = [r for r in self.rabbits if r.eaten > 0]
        self.rabbits = [r for r in self.rabbits if r.survive()]

    def reproduce(self):
        """ Rabbits reproduce like rabbits. """
        born = []
        for rabbit in self.rabbits:
            for _ in range(rnd.randint(1, rabbit.max_offspring)):
                born.append(rabbit.reproduce())
        self.rabbits += born

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

    def get_rabbits(self):
        rabbits = np.zeros(shape=(self.size, self.size), dtype=int)
        for r in self.rabbits:
            rabbits[r.x, r.y] = r.id
        return rabbits

    def num_animals(self):
        """ How many rabbits are there in the field ? """
        num_dict = {}

        # add empty lists to the dict for each id present
        for r in self.rabbits:
            num_dict[r.id] = []

        for r in self.rabbits:
            num_dict[r.id] += [r]

        return num_dict
        # return len([r for r in self.rabbits if r.id == 2])

    def amount_of_grass(self):
        return self.field.sum()

    def generation(self):
        """ Run one generation of rabbits """
        self.move()
        self.eat()
        self.survive()
        self.reproduce()
        self.grow()

    def history(self, showTrack=True, showPercentage=True, marker='.'):

        plt.figure(figsize=(6, 6))
        plt.xlabel("# Rabbits")
        plt.ylabel("# Grass")

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

        if showTrack:
            plt.plot(xs, ys, marker=marker)
            plt.plot(xf, ys, marker=marker)
        else:
            plt.scatter(xs, ys, marker=marker)

        plt.grid()

        plt.title("Rabbits vs. Grass: GROW_RATE =" + str(GRASS_RATE))
        plt.savefig("history.png", bbox_inches='tight')
        plt.show()

    def history2(self):
        xs = self.nrabbits[:]
        ys = self.ngrass[:]

        sns.set_style('dark')
        f, ax = plt.subplots(figsize=(7, 6))

        sns.scatterplot(x=xs, y=ys, s=5, color=".15")
        sns.histplot(x=xs, y=ys, bins=50, pthresh=.1, cmap="mako")
        sns.kdeplot(x=xs, y=ys, levels=5, color="r", linewidths=1)
        plt.grid()
        plt.xlim(0, max(xs) * 1.2)

        plt.xlabel("# Rabbits")
        plt.ylabel("# Grass")
        plt.title("Rabbits vs. Grass: GROW_RATE =" + str(GRASS_RATE))
        plt.savefig("history2.png", bbox_inches='tight')
        plt.show()


def animate(i, field, im):
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

# clist = ['white', 'red', 'blue', 'green']
clist = ['white', 'green', 'blue', 'red']
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
        field.add_rabbit(Rabbit(2, 1, 1, 1, (1,), fsize))

    # add fox
    for _ in range(3):
        field.add_rabbit(Rabbit(3, 1, 2, 1, (2,), fsize))

    array = np.ones(shape=(fsize, fsize), dtype=int)
    fig = plt.figure(figsize=(5, 5))
    im = plt.imshow(array, cmap=my_cmap, interpolation='hamming', aspect='auto', vmin=0, vmax=1)
    anim = animation.FuncAnimation(fig, animate, fargs=(field, im,), frames=1000000, interval=1, repeat=True)
    plt.show()

    field.history()
    field.history2()


if __name__ == '__main__':
    main()

"""
def main():

    # Create the ecosystem
    field = Field()
    for _ in range(10):
        field.add_rabbit(Rabbit())


    # Run the world
    gen = 0

    while gen < 500:
        field.display(gen)
        if gen % 100 == 0:
            print(gen, field.num_rabbits(), field.amount_of_grass())
        field.move()
        field.eat()
        field.survive()
        field.reproduce()
        field.grow()
        gen += 1

    plt.show()
    field.plot()

if __name__ == '__main__':
    main()

SOURCES:

help with parsers- https://docs.python.org/3/library/argparse.html 
"""
