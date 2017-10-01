import random
def network(min_neuron_number=20):
    neuron_number = min_neuron_number + random.randint(0,100)

    connections = []
    weights = []
    for i in range(neuron_number):
        connections.append([])
        max_conn = random.randint(1,round(neuron_number/2))

        while len(connections[i]) < max_conn:
            connections[i].append(random.randrange(0,round(neuron_number,0)))

        weights.append([])
        while len(weights[i]) < max_conn:
            weight = random.randint(0,1)+random.random()
            weight *= random.choice([-1,1])
            weights[i].append(weight)

    return weights,connections
