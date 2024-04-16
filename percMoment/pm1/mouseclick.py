import numpy as np
import random 

#code for a random seed generator

my_seed = random.randrange(1e6)
my_seed = 787892
print(my_seed)
random.seed(my_seed)

nums = random.randint(0,100)
print(nums)
