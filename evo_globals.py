net_dir = "nets"

import helpers, os
if not os.path.exists(helpers.rel_path(net_dir)):
    try:
        os.mkdir(helpers.rel_path(net_dir))
    except OSError:
        pass

# max "hidden" neurons to add
# at 0, only input+output neurons will be generated
max_neurons = 120

##################
### Activators ###
import math
curr_activator = "sigmoid"
def activator(val):
    return activators[curr_activator](val)

activators = {}
activators["tanh"] = math.tanh

def sigmoid(val): return 1/(1+math.exp(-val))
activators["sigmoid"] = sigmoid

def relu(val): return max(0,val)
activators["relu"] = relu
