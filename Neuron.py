from Synapse import Synapse
from os import linesep
from evo_globals import activator
"""
    Neuron class
"""

class Neuron:
    def __init__(self):
        self.value = 0
        self.inputs = []

    def add_synapse(self, neuron, weight):
        self.inputs.append(Synapse(neuron=neuron, weight=weight))

    def get_sum(self):
        s_sum = 0
        for synapse in self.inputs:
            s_sum += synapse.get_output()

        return s_sum

    def update_value(self):
        self.value = activator(self.get_sum())

    def __str__(self):
        result = ""
        for synapse in self.inputs:
            result += str(synapse)

        return result + linesep
