import random
import evolve
from datetime import datetime
from configparser import ConfigParser
from evolve import EvolvePool

config = ConfigParser()
config.read("config.ini")

output = open("output.txt", "a")
output.write("New run\n")
start = datetime.now()
output.write("started: "+ str(start)+"\n")


pool = EvolvePool(genes=config.get("config", "genes"), pop_size=int(config.get("config", "pop_size")), target=config.get("config", "target"), mut_rate=float(config.get("config", "mutation_rate")))
result, generations = pool.evolve_pool()
end = datetime.now()
output.write("ended: "+ str(end)+"\n")

computation_time = end - start

output.write("computation time: "+ str(computation_time) +", "+ str(generations) +" generations")
output.write("\n\n=====================================================================\n")
