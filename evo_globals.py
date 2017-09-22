net_dir = "nets"

##################
### Activators ###
import math
curr_activator = "tanh"
def activator(val):
    return activators[curr_activator](val)

activators = {}
activators["tanh"] = math.tanh

def sigmoid(val): return 1/(1+math.exp(-val))
activators["sigmoid"] = sigmoid
