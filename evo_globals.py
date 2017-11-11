net_dir = "nets"
import os
from . import helpers

if not os.path.exists(helpers.rel_path(net_dir)):
    try:
        os.mkdir(helpers.rel_path(net_dir))
    except OSError:
        pass

##################
### Activators ###
import math
curr_activator = "tanh" # tanh is preferred
def activator(val):
    return activators[curr_activator](val)

activators = {}
activators["tanh"] = math.tanh

def sigmoid(val): return 1/(1+math.exp(-val))
activators["sigmoid"] = sigmoid

def relu(val): return max(0,val)
activators["relu"] = relu

###################
### Derivatives ###

def derivative(val):
    return derivatives[curr_activator](val)

derivatives = {}
def dtanh(x):
    return 1 - (math.tanh(x)**2)
derivatives["tanh"] = dtanh

def dsigmoid(x):
    return x * (1 - x)
derivatives["sigmoid"] = dsigmoid

def drelu(x):
    if x >= 0:
        return 1
    else:
        return 0
derivatives["relu"] = drelu
