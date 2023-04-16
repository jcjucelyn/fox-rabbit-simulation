"""
Jocelyn Ju, Ceara Zhang
DS 3500 / Homework 5
Created April 10, 2023
Updated April 15, 2023
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib import colors
from classAnimal import Animal
from classField import Field

fsize = 50
OFFSPRING = 2  # Max offspring when a rabbit reproduces
grass_rate = 0.025  # Probability that grass grows back at any location in the next season.
WRAP = False  # Does the field wrap around on itself when rabbits move?
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
    while i <= 500:
        field.generation()
        # print("AFTER: ", i, np.sum(field.field), len(field.nfoxes))
        im.set_array(field.field)
        im.set_cmap(my_cmap)
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

    # add rabbits
    for _ in range(100):
        rabbit = Animal(2, 2, 1, 1, (1,), fsize)
        field.add_animal(rabbit)

    # add foxes
    for _ in range(20):
        fox = Animal(3, 1, 2, 10, (2, ), fsize)
        field.add_animal(fox)

    # create the initial array of grass (value = 1)
    array = np.ones(shape=(fsize, fsize), dtype=int)

    #(id, max_offspring, speed, starve, eats, fsize):

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