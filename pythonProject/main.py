import random
import evolve
from evolve import EvolvePool

target = "test"#input("Target string:")

pool = EvolvePool(500, target)
pool.get_pop()
print(str(pool.get_pop().sort()))
