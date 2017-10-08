import random, evo_globals
"""
    Generate weights and connections data for Network.
"""
def network(min_neuron_number=20):
    neuron_number = min_neuron_number + random.randint(0, evo_globals.max_neurons)

    connections = []
    weights = []
    for i in range(neuron_number):
        connections.append([])
        max_conn = random.randint(1,round(neuron_number/2))

        while len(connections[i]) < max_conn:
            connections[i].append(random.randrange(0,round(neuron_number,0)))

        weights.append([])
        while len(weights[i]) < max_conn:
            weight = random.randint(0,3)+random.random()
            weight *= random.choice((-1,1))
            weights[i].append(weight)

    return weights,connections
