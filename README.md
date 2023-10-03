# fox-rabbit-simulation

This is a simulation of foxes, rabbits, and grass in pixel form, with each pixel representing one organism. The rabbits must eat grass, the foxes must eat rabbits, and the grass must regrow.

The repository contains the following:
- main.py : a Python file animating the field and the animals
- classAnimal.py : a Python file containing the Animal class, which includes both foxes and rabbits. This file controls where the animal moves, whether the animal has eaten, reproduction, and whether the animal survived the cycle.
- classField.py : a Python file containing the Field class, which controls the behavior of the field, as well as keeping track of and storing the history of the field.
- history.png : a png image of foxes, rabbits, and grass plotted against generations.

You must run main.py in the terminal, with a command as follows: python3 main.py grass_growth fox_k field_size init_fox init_rabbit
Variables are:
- grass_growth : (float) the probability that grass grows back at any location in the next cycle
- fox_k : (int) the number of generations a fox can go without eating
- field_size : (int) the length and width of the square field in pixels
- init_fox : (int) the initial number of fox pixels to populate on the field
- init_rabbit : (int) the initial number of rabbit pixels to populate on the field

Rabbits must eat every cycle or they die, but the foxes have a bit more leeway (depending on the k-value chosen). 
