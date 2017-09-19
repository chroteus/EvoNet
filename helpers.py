import os, json

def rel_path(*args):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)

def decode_net_str(data):
    weights_data,conns_data = data.split(",")
    weights_data = weights_data.rstrip(os.linesep)
    conns_data = conns_data.lstrip(os.linesep)

    #interpret weights
    weights_data = weights_data.split(os.linesep) #each item is a neuron now
    weights = []
    for ni,neuron in enumerate(weights_data):
        #split neuron into its weights (12 digits per weight)
        neuron = [neuron[i:i+12] for i in range(0, len(neuron), 12)]
        weights.append([])
        for wi,weight in enumerate(neuron):
            sign = int(weight[0]) #first digit represents sign of weight
            sign = -1 if sign < 5 else 1
            weight = weight[1:] #remove sign integer
            weight = weight[:1] + "." + weight[1:] #add decimal point
            weights[ni].append(float(weight)*sign) # finally, convert the string

    #interpret connections data
    conns_data = conns_data.split(os.linesep) #split per neuron
    for ci,conn in enumerate(conns_data):
        conns_data[ci] = [int(x) for x in conn.split(".")]

    return weights,conns_data



NETS_DIR = "nets"
def open_net_file(net_file):
    path = rel_path(NETS_DIR, net_file)
    assert os.path.isfile(path)

    with open(path) as f:
        # separate weight and connection data into
        # separate chunks
        data = f.read().rstrip(os.linesep)

    return decode_net_str(data)
