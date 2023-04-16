"""
Jocelyn Ju, Ceara Zhang
DS 3500 / Homework 5
Created April 10, 2023
Updated April 15, 2023
"""

import random as rnd
import copy


fsize = 50
OFFSPRING = 2  # Max offspring when a rabbit reproduces
grass_rate = 0.025  # Probability that grass grows back at any location in the next season.
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
        # if the animal ate that cycle,
        # reset counter to 0
        if self.eaten > 0:
            self.cycle = 0
            return True

        # ele animal hasn't eaten, so
        # if the animal has gone too many cycles
        # without eating, return "False" aka died
        else:
            if self.cycle <= self.starve:
                self.cycle += 1
                return True
            else:
                self.id = 0
                return False