import random
from . import evo_globals

"""
    Generate weights and connections data for Network.
"""

def new_weight():
    weight = random.randint(0,1)+random.random()
    weight *= random.choice((-1,1))
    return weight

def network(min_n=20,max_n=500):
    neuron_number = min_n + random.randint(0, max_n-min_n)

    connections = []
    weights = []
    for i in range(neuron_number):
        connections.append([])
        m = neuron_number #round(max(neuron_number/5, 40))
        max_conn = random.randint(1,m)

        while len(connections[i]) <= max_conn:
            rand_n = random.randrange(0,round(neuron_number,0))
            if i != rand_n: #prevent self-referential neurons
                connections[i].append(rand_n)

        weights.append([])
        while len(weights[i]) <= max_conn:
            weights[i].append(new_weight())


    return weights,connections
