
import random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import copy
import seaborn as sns
""" TRYING TO CREATE SEPARATE FOX AND BUNNY CLASSES """

SIZE = 500  # The dimensions of the field
R_OFFSPRING = 2 # Max offspring when a rabbit reproduces
F_OFFSPRING = 2 # Max offspring when a fox reproduces
GRASS_RATE = 0.025 # Probability that grass grows back at any location in the next season.
WRAP = False # Does the field wrap around on itself when rabbits move?

EMPTY = 0
GRASS_CELL = 1
RABBIT_CELL = 2
FOX_CELL = 3


# only take in one class, "animal"
# make parameters-- max offspring, speed, starve, eats(what # they can eat, like rabbits are 1)
# only foxes that eat can reproduce
# 0 IS EMPTY LAND, 1 is GRASS, 2 IS BUNNY, 3 IS FOX

class Rabbit:
    """ A furry creature roaming a field in search of grass to eat.
    Mr. Rabbit must eat enough to reproduce, otherwise he will starve. """

    def __init__(self):
        self.x = rnd.randrange(0, SIZE)
        self.y = rnd.randrange(0, SIZE)
        self.eaten = 0

    def reproduce(self):
        """ Make a new rabbit at the same location.
         rabbit's eaten level is reset to zero. """
        self.eaten = 0
        offspring = rnd.randint(0, R_OFFSPRING)
        for _ in range(offspring):
            return copy.deepcopy(self)

    def eat(self, amount):
        """ Feed the rabbit some grass """
        self.eaten += amount

    def move(self):
        """ Move up, down, left, right randomly """

        if WRAP:
            self.x = (self.x + rnd.choice([-1,0,1])) % SIZE
            self.y = (self.y + rnd.choice([-1,0,1])) % SIZE
        else:
            self.x = min(SIZE-1, max(0, (self.x + rnd.choice([-1, 0, 1]))))
            self.y = min(SIZE-1, max(0, (self.y + rnd.choice([-1, 0, 1]))))

class Fox:
    """ A furry creature roaming a field in search of grass to eat.
    Mr. Rabbit must eat enough to reproduce, otherwise he will starve. """
    def __init__(self):
        """
        x: describing where fox can move
        y: describing where fox can move
        eaten: number of rabbits fox has eaten\
        cycle: keep track of number of cycles fox gone since it ate
        starve: specify max number of cycles fox can go without eating
        """
        self.x = rnd.randrange(0, SIZE)
        self.y = rnd.randrange(0, SIZE)
        self.eaten = 0
        self.cycle = 0
        self.starve = 3


    def reproduce(self):
        """ Make a new Fox at the same location.
         fox's eaten level is reset to zero. """
        self.eaten = 0
        offspring = rnd.randint(0, F_OFFSPRING)
        for _ in range(offspring):
            return copy.deepcopy(self)

    def eat(self, amount):
        """ Fox eats rabbit"""
        self.eaten += amount

    # def move(self):
    #     """ Move up, down, left, right randomly """
    #     max_move = self.speed + 1
    #     move_list = [i for i in range(max_move)]
    #
    #     if WRAP:
    #         self.x = (self.x + rnd.choice(move_list)) % SIZE
    #         self.y = (self.y + rnd.choice(move_list)) % SIZE
    #     else:
    #         self.x = min(SIZE-1, max(0, (self.x + rnd.choice(move_list))))
    #         self.y = min(SIZE-1, max(0, (self.y + rnd.choice(move_list))))
    def move(self):
        """ Move up, down, left, right randomly """

        if WRAP:
            self.x = (self.x + rnd.choice([-1, 0, 1])) % SIZE
            self.y = (self.y + rnd.choice([-1, 0, 1])) % SIZE
        else:
            self.x = min(SIZE-1, max(0, (self.x + rnd.choice([-1, 0, 1]))))
            self.y = min(SIZE-1, max(0, (self.y + rnd.choice([-1, 0, 1]))))

    def survive(self):
        """Checks if fox has survived"""
        if self.cycle <= self.starve:
            self.cycle += 1
            return True
        else:
            return False


# class Animal:
#     """ A furry creature roaming a field in search of something to eat.
#     Mr. Animal must eat enough to reproduce, otherwise he will starve. """
#
#     def __init__(self, id, max_offspring, speed, starve, eats):
#         self.x = rnd.randrange(0, SIZE)
#         self.y = rnd.randrange(0, SIZE)
#         self.eaten = 0
#         self.id = id
#         self.max_offspring = max_offspring
#         self.speed = speed
#         self.starve = starve
#         self.eats = eats
#
#     def reproduce(self):
#         """ Make a random number of new animal(s) at the same location
#          given the maximum offspring that animal can have.
#          Reproduction is hard work! Each reproducing
#          animal's eaten level is reset to zero. """
#         self.eaten = 0
#         offspring = rnd.randint(0, self.max_offspring)
#         for _ in range(offspring):
#             return copy.deepcopy(self)
#
#     def eat(self, amount):
#         """ Feed the animal some of whatever it eats """
#         self.eaten += amount
#
#     def move(self):
#         """ Move up, down, left, right randomly """
#         max_move = self.speed + 1
#         move_list = [i for i in range(max_move)]
#
#         if WRAP:
#             self.x = (self.x + rnd.choice(move_list)) % SIZE
#             self.y = (self.y + rnd.choice(move_list)) % SIZE
#         else:
#             self.x = min(SIZE-1, max(0, (self.x + rnd.choice(move_list))))
#             self.y = min(SIZE-1, max(0, (self.y + rnd.choice(move_list))))



class Field:
    """ A field is a patch of grass with 0 or more rabbits hopping around
    in search of grass """

    def __init__(self):
        """ Create a patch of grass with dimensions SIZE x SIZE
        and initially no rabbits """
        self.rabbits = []
        self.foxes = []
        self.field = np.ones(shape=(SIZE, SIZE), dtype=int)
        self.nrabbits = []
        self.nfoxes = []
        self.ngrass = []


    def add_rabbit(self, rabbit):
        """ A new rabbit is added to the field """
        self.rabbits.append(rabbit)

    def add_fox(self, fox):
        """A new fox is added to the field"""
        self.foxes.append(fox)

    def move(self):
        """ Animals move """
        for r in self.rabbits:
            r.move()
        for f in self.foxes:
            f.move()

    def foxEatRabbit(self):
        """
        Foxes eat rabbits (if they find any)
        """
        for fox in self.foxes:
            possible_victims = [rabbit for rabbit in self.rabbits if rabbit.x == fox.x and rabbit.y == fox.y]
        if len(possible_victims) > 0:
            victim = rnd.choice(possible_victims)
            self.rabbits.remove(victim)
            fox.eaten += 1


    def rabbitEatGrass(self):
        """ Rabbits eat (if they find grass where they are) """

        for rabbit in self.rabbits:
            if self.field[rabbit.x, rabbit.y] == 1:
                rabbit.eat(self.field[rabbit.x,rabbit.y])
                self.field[rabbit.x,rabbit.y] = 0
        #
        #
        # # check id of new spot
        # # if edible, eat. if not, don't
        # for animal in self.animals:
        #     if self.field[animal.x, animal.y] in range(animal.eats):
        #         animal.eat(self.field[animal.x,animal.y])
        #     self.field[animal.x,animal.y] = 0

    def survive(self):
        """ Rabbits who eat some grass live to eat another day """
        self.rabbits = [r for r in self.rabbits if r.eaten > 0]
        self.foxes = [r for r in self.foxes if r.survive is True]

    def reproduce(self):
        """ Rabbits and foxes reproduce if they have eaten enough. """

        # rabbits reproduce
        born_rabbits = []
        rabbit_reproduce_threshold = 10
        for rabbit in self.rabbits:
            if rabbit.eaten >= rabbit_reproduce_threshold:
                for _ in range(rnd.randint(1, R_OFFSPRING)):
                    born_rabbits.append(rabbit.reproduce())
        self.rabbits += born_rabbits

        # Foxes reproduce
        born_foxes = []
        fox_reproduce_threshold = 10
        for fox in self.foxes:
            if fox.eaten >= fox_reproduce_threshold:
                for _ in range(rnd.randint(1, F_OFFSPRING)):
                    born_foxes.append(fox.reproduce())
        self.foxes += born_foxes

        # Capture field state for historical tracking
        self.nfoxes.append(self.num_foxes())
        self.nrabbits.append(self.num_rabbits())
        self.ngrass.append(self.num_grass())

    def grow(self):
        """ Grass grows back with some probability """
        growloc = (np.random.rand(SIZE, SIZE) < GRASS_RATE) * 1
        self.field = np.maximum(self.field, growloc)


    def get_rabbits(self):
        """creates 2D array where each element represents presence/absence of rabbit"""
        rabbits = np.zeros(shape=(SIZE,SIZE), dtype=int)
        for r in self.rabbits:
            rabbits[r.x, r.y] = 1
        return rabbits

    def get_foxes(self):
        foxes = np.zeros(shape=(SIZE, SIZE), dtype=int)
        for r in self.foxes:
            foxes[r.x, r.y] = 1
        return foxes

    def num_foxes(self):
        """How many foxes are there in the field?"""
        return len(self.foxes)

    def num_rabbits(self):
        """How many rabbit are there in the field?"""
        return len(self.rabbits)

    def num_grass(self):
        """How much grass is on the field?"""
        return self.field.sum()

    def generation(self):
        """ Run one generation"""
        self.move()
        self.foxEatRabbit()
        self.rabbitEatGrass()
        self.survive()
        self.reproduce()
        self.grow()

    # def history(self, showTrack=True, showPercentage=True, marker='.'):
    #
    #     plt.figure(figsize=(6,6))
    #     plt.xlabel("# Rabbits")
    #     plt.ylabel("# Grass")
    #
    #     xs = self.nrabbits[:]
    #     if showPercentage:
    #         maxrabbit = max(xs)
    #         xs = [x/maxrabbit for x in xs]
    #         plt.xlabel("% Rabbits")
    #
    #     ys = self.ngrass[:]
    #     if showPercentage:
    #         maxgrass = max(ys)
    #         ys = [y/maxgrass for y in ys]
    #         plt.ylabel("% Grass")
    #
    #     zs = self.nfoxes[:]
    #     if showPercentage:
    #         maxfox = max(zs)
    #         zs = [z/maxfox for z in zs]
    #         plt.ylabel("% Foxes")
    #
    #     if showTrack:
    #         plt.plot(xs, ys, marker=marker, label="Rabbits")
    #         plt.plot(zs, ys, marker=marker, label="Foxes")
    #     else:
    #         plt.scatter(xs, ys, marker=marker, label="Rabbits")
    #         plt.scatter(zs, ys, marker=marker, label="Foxes")
    #
    #     plt.grid()
    #
    #     plt.title("Rabbits vs. Grass vs. Foxes: GROW_RATE =" + str(GRASS_RATE))
    #     plt.legend(loc="upper left")
    #     plt.savefig("history.png", bbox_inches='tight')
    #     plt.show()
    #
    # def history2(self):
    #     xs = self.nanimals[:]
    #     ys = self.ngrass[:]
    #     zs = self.nfoxes[:]
    #
    #     sns.set_style('dark')
    #     f, ax = plt.subplots(figsize=(7, 6))
    #
    #     sns.scatterplot(x=xs, y=ys, hue=zs, s=5, palette='viridis')
    #     sns.histplot(x=xs, y=ys, bins=50, pthresh=.1, cmap="mako")
    #     sns.kdeplot(x=xs, y=ys, levels=5, color="r", linewidths=1)
    #     plt.grid()
    #     plt.xlim(0, max(xs)*1.2)
    #
    #     plt.xlabel("# Rabbits")
    #     plt.ylabel("# Grass")
    #     plt.title("Rabbits and Foxes vs. Grass: GROW_RATE =" + str(GRASS_RATE))
    #     plt.legend(title="Number Foxes")
    #     plt.savefig("history2.png", bbox_inches='tight')
    #     plt.show()


def animate(i, field, im):

    # generate field
    field.generation()

    # get cells that contain each
    rabbits = field.field == RABBIT_CELL
    foxes = field.field == FOX_CELL
    grass = field.field == GRASS_CELL

    # create new array with 3 color channels
    new_array = np.zeros(shape=(SIZE, SIZE, 3))
    new_array[:, :, 0] = grass #red
    new_array[:, :, 1] = rabbits #green
    new_array[:, :, 2] = foxes #blue

    # update image with the new array
    im.set_array(new_array)

    # set title of plot to show current generation
    plt.title("generation = " + str(i))
    return im,


def main():

    # Create the ecosystem
    field = Field()

    for _ in range(20):
        field.add_rabbit(Rabbit())
        field.add_fox(Fox())
        field.grow()
        #field.add_animal(Fox(3, 1, 2, 10, (0,)))



    array = np.ones(shape=(SIZE, SIZE, 3), dtype=int)
    fig = plt.figure(figsize=(5,5))
    im = plt.imshow(array, cmap='PiYG', interpolation='hamming', aspect='auto', vmin=0, vmax=1)
    anim = animation.FuncAnimation(fig, animate, fargs=(field, im,), frames=1000000, interval=1, repeat=True)
    plt.show()

    # field.history()
    # field.history2()


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

class Field:
     A field is a patch of grass with 0 or more rabbits hopping around
    in search of grass 

    def __init__(self):
         Create a patch of grass with dimensions SIZE x SIZE
        and initially no rabbits 
        # self.rabbits = []
        self.animals = []
        self.field = np.ones(shape=(SIZE,SIZE), dtype=int)
        self.nrabbits = []
        self.ngrass = []


    # def add_rabbit(self, rabbit):
    #     A new rabbit is added to the field 
    #     self.rabbits.append(rabbit)

    def add_animal(self, animal):
        self.animals.append(animal)

    def move(self):
        Animals move 
        for r in self.animals:
            r.move()

    def eat(self):
       Rabbits eat (if they find grass where they are

        # for rabbit in self.rabbits:
        #     rabbit.eat(self.field[rabbit.x,rabbit.y])
        #     self.field[rabbit.x,rabbit.y] = 0
        # if the animal eats grass
        if food == 0:
            for animal in self.animals:
                animal.eat(self.field[animal.x, animal.y])

            # if find grass
            self.field[animal.x, animal.y] = 0

    def survive(self):
      Rabbits who eat some grass live to eat another day 
        # self.rabbits = [r for r in self.rabbits if r.eaten > 0]
        self.animals = [r for r in self.animals if r.eaten > 0]

    def reproduce(self):
        Rabbits reproduce like rabbits. 
        born = []
        for animal in self.animals:
            for _ in range(rnd.randint(1, animal.max_offspring)):
                born.append(animal.reproduce())
        self.animals += born

        # Capture field state for historical tracking
        self.nrabbits.append(self.num_rabbits())
        self.ngrass.append(self.amount_of_grass())

    def grow(self):
       Grass grows back with some probability 
        growloc = (np.random.rand(SIZE, SIZE) < GRASS_RATE) * 1
        self.field = np.maximum(self.field, growloc)

    def get_rabbits(self):
        rabbits = np.zeros(shape=(SIZE,SIZE), dtype=int)
        for r in self.rabbits:
            rabbits[r.x, r.y] = 1
        return rabbits

    def num_rabbits(self):
         How many rabbits are there in the field ? 
        return len(self.rabbits)

    def amount_of_grass(self):
        return self.field.sum()

    def generation(self):
        Run one generation of rabbits 
        self.move()
        self.eat()
        self.survive()
        self.reproduce()
        self.grow()

    def history(self, showTrack=True, showPercentage=True, marker='.'):


        plt.figure(figsize=(6,6))
        plt.xlabel("# Rabbits")
        plt.ylabel("# Grass")

        xs = self.nrabbits[:]
        if showPercentage:
            maxrabbit = max(xs)
            xs = [x/maxrabbit for x in xs]
            plt.xlabel("% Rabbits")

        ys = self.ngrass[:]
        if showPercentage:
            maxgrass = max(ys)
            ys = [y/maxgrass for y in ys]
            plt.ylabel("% Rabbits")

        if showTrack:
            plt.plot(xs, ys, marker=marker)
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
        plt.xlim(0, max(xs)*1.2)

        plt.xlabel("# Rabbits")
        plt.ylabel("# Grass")
        plt.title("Rabbits vs. Grass: GROW_RATE =" + str(GRASS_RATE))
        plt.savefig("history2.png", bbox_inches='tight')
        plt.show()
"""





