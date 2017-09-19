from Synapse import Synapse
from os import linesep
from math import tanh
"""
    Neuron class
"""

class Neuron:
    def __init__(self):
        self.value = 0
        self.inputs = []

    def addSynapse(self, neuron, weight):
        self.inputs.append(Synapse(neuron=neuron, weight=weight))

    def getSum(self):
        s_sum = 0
        for synapse in self.inputs:
            s_sum += synapse.getOutput()

        return s_sum

    def updateValue(self):
        self.value = tanh(self.getSum())

    def __str__(self):
        result = ""
        for synapse in self.inputs:
            result += str(synapse)

        return result + linesep
