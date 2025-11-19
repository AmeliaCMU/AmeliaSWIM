import random

airports = [
    "KATL", "KBDL", "KBOS", "KBWI", "KCLE", "KCLT", "KDCA", "KDEN",
    "KDFW", "KDTW", "KEWR", "KFLL", "KHOU", "KIAD", "KIAH", "KJFK",
    "KLAS", "KLAX", "KLGA", "KMCI", "KMCO", "KMDW", "KMEM", "KMIA",
    "KMKE", "KMSP", "KMSY", "KORD", "KPDX", "KPHL", "KPHX", "KPIT",
    "KPVD", "KSAN", "KSDF", "KSEA", "KSFO", "KSLC", "KSNA", "KSTL",
    "PANC", "PHNL",
]

assert len(airports) == 42, f"Expected 42 airports, got {len(airports)}"


idx = [i for i in range(1, 43)]
random.shuffle(idx)
bash_list = 'list=(\n'
for i, airport in enumerate(airports):
    bash_list += f'  "{airport.lower()} amelia42/amelia42_{idx[i]}"\n'
bash_list += ')'



print(bash_list)