import random
import evolve
from evolve import EvolvePool

target = "testta"#input("Target string:")

pool = EvolvePool(500, target)
pool.evolve_pool()
