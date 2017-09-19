from Neuron import Neuron
"""
    Network class.
    Arguments:
    neurons: List of weights of neurons. neurons[ neuron1[ weight1[1.343..,0.12..] ]]
    connections:
    neurons are connected according to their index.
    ex:[[1,3,4], ...]
    So, in this case, 0th neuron gets input from 4th, 3rd
    and 1st neurons.
    Last neurons in list are considered output neurons
    and vice versa for input.

    See docs for more info.
    Another note:
"""
from os import linesep
import random,itertools

class Network:
    def __init__(self, weights, connections, input_no=1,output_no=1):
        self.neurons = []
        self.connection_data = connections #store for serialization purposes
        self.weights_data = weights #for reproduction
        self.input_no = input_no
        self.output_no = output_no

        # add empty neurons
        for neuron in weights:
            self.neurons.append(Neuron())

        # connect those neurons and set weights
        for ni,conns in enumerate(connections):
            for ci, inputn_i in enumerate(conns): #index of neuron to connect
                weight = weights[ni][ci]
                input_neuron = self.neurons[int(inputn_i)]
                self.neurons[ni].addSynapse(weight=weight, neuron=input_neuron)

    def set_input(self, input_data):
        for i,data in enumerate(input_data):
            self.neurons[i].value = input_data[i]

    def get_output(self, custom_output_no=None):
        for neuron in self.neurons:
            neuron.update_value()

        result = []
        out_no = self.output_no if not custom_output_no else custom_output_no
        for out_neuron in self.neurons[-out_no:]:
            result.append(out_neuron.value)
        return result

    def reproduce_with(self, mate, mix_conns=True):
        big = self if len(self.neurons) > len(mate.neurons) else mate
        small = mate if self is big else self

        #combine weights randomly, giving preference to larger topology (for now)
        new_weights = []
        for neur_a,neur_b in itertools.zip_longest(self.weights_data,mate.weights_data, fillvalue=[]):
            new_weights.append([])
            for syn_a,syn_b in itertools.zip_longest(neur_a,neur_b, fillvalue="x"):
                new_w = random.choice([syn_a,syn_b])
                new_weights[-1].append(new_w)

        for ni,neuron in enumerate(new_weights):
            for si,syn in enumerate(neuron):
                if syn == "x":
                    new_weights[ni][si] = (random.randint(0,3) + random.random())*random.choice([-1,1])

        new_connections = []
        for bci,bconn in enumerate(big.connection_data):
            sconn = small.connection_data[bci] if bci < len(small.connection_data) else None
            new_neural_in = [] if sconn else bconn #default to big net's topology
            if not mix_conns:
                new_neural_in = bconn
            elif sconn:
                for ni,neuron_index in enumerate(max(sconn,bconn)):
                    sconni = sconn[ni] if ni < len(sconn) else random.randint(0,len(new_weights)-1) # a bit of mutation
                    bconni = bconn[ni] if ni < len(bconn) else random.randint(0,len(new_weights)-1) # a bit of mutation
                    new_neural_in.append(random.choice([sconni, bconni]))

            new_connections.append(new_neural_in)

        return Network(weights=new_weights,connections=new_connections, input_no=big.input_no,output_no=big.output_no)

    def get_weight_str(self):
        neurons = [str(x) for x in self.neurons]
        s = "".join(neurons)

        return s

    def get_conn_str(self):
        s = ""
        # connection information
        for conn in self.connection_data:
            conn = [str(s) for s in conn] #convert all integers to strings
            s += ".".join(conn) + linesep #condense them into a single string
        return s

    def __str__(self):
        s = ["",
             self.get_weight_str(),
             "," + linesep,
             self.get_conn_str()]

        s = "".join(s) #more efficent this way
        return s.rstrip(linesep)
