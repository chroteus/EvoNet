import random

"""
    Connect Neurons between each other and input value to parent neuron
    from output neuron
"""
class Synapse:
    def __init__(self, neuron, weight):
        if weight is None:
            weight = random.randint(0,9) + random.random()
            weight *= random.choice([-1,1])

        self.weight = weight
        self.neuron = neuron #from which neuron to get value

    def get_output(self):
        return self.neuron.value*self.weight

    def __str__(self):
        # synapses with positive weights have first integer >5
        result = "9" if self.weight > 0 else "0"

        split_weight = str(abs(self.weight)).split(".")
        result += split_weight[0] #integer part
        result += split_weight[1] #decimal

        result = result[:12] #truncate if >12 digits
        while len(result) < 12:
            result += "0"

        return result
