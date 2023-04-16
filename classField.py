"""
Jocelyn Ju, Ceara Zhang
DS 3500 / Homework 5
Created April 10, 2023
Updated April 15, 2023
"""

import random as rnd
import matplotlib.pyplot as plt
import numpy as np

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
        if animal is not None:
            self.animals.append(animal)
        #self.field[animal.x][animal.y] = animal.id

    def move(self):
        """ Animals move """
        for r in self.animals:
            r.move()

    def eat(self):
        """ Animals eat (if they find grass where they are) """
        for animal in self.animals:
            for other in self.animals:
                # if other animal is prey, eat
                if other != animal and other.id in animal.eats and animal.x == other.x and animal.y == other.y:
                    animal.eat(other.id)
                    #self.field[animal.x][animal.y] = animal.id
            # if the thing at the current position is what the animal
            # eats, then animal will eat the thing and the current
            # position becomes whatever the animal is
            if self.field[animal.x][animal.y] in animal.eats:
                animal.eat(self.field[animal.x][animal.y])
                self.field[animal.x][animal.y] = 0

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