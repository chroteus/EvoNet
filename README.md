# EvoNet
EvoNet is an *experimental* project developed to train neural networks by evolving its topology and weights at the same time using a genetic algorithm.
Unlike usual layer-based neural nets, EvoNet has arbitrary connections between neurons and is thus pretty universal.  

# An example net
The net below is the top net from my tests on evolving nets to play Pong.
Neurons 0 and 1 are input neurons (ball's position) and neuron 8 is the output neuron (paddle's x position).
Blue connections are negative and red connections are positive.
The connection's width represent the weight of that connection.

The only way that input neurons differ from other neurons is that they additionally take input from user.

![Net](https://user-images.githubusercontent.com/5436911/31633344-c0f7f146-b2c8-11e7-95b7-440b3c32173c.png)

In this particular network, the first (and only) route from 0 is to 6, with a very insignificant weight. From 6, the data is sent to other neurons and especially to 0, getting augmented by big weight along the way.
The first question you might ask is why do input neurons get input from other neurons.
Honestly, I don't know. It just works™.

# A very simple example of net training
```python
import evonet

# init the main class
evo = evonet.evo.Evo(input_no=2,output_no=1,
                     net_no=300, # nets per generation
                     chosen_no=100, # nets to be bred per generation
                     mix_conns=False)
# evolve a net to approximate XOR operator
def xor_fitness(evo,net):
    a = random.choice((0,1))
    b = random.choice((0,1))
    real_out = a ^ b #xor operator
    net.set_input([a,b])
    net_out = net.get_output()[0]

    # return the fitness value to Evo
    return 1/(abs(net_out-real_out)**2)

evo.set_fitness_func(xor_fitness)

for i in range(10):
    evo.evolve_for(1)
    top_net = evo.nets[0]
    top_net.set_input([1,0])
    out = top_net.get_output()[0]
    print("GEN " + str(i) + ": Expected 1, got " + str(out))
```

Here are some (truncated) outputs for 1^0 (per generation trained):
```
GEN 0: Expected 1, got 0.002
GEN 1: Expected 1, got 0.001
GEN 2: Expected 1, got 0.000
GEN 3: Expected 1, got 0.002
GEN 4: Expected 1, got 0.000
GEN 5: Expected 1, got 0.999
GEN 6: Expected 1, got 0.000
GEN 7: Expected 1, got 0.000
GEN 8: Expected 1, got 0.999
GEN 9: Expected 1, got 0.999
```
As you can see from gen 6, algorithm discarded the nets that didn't work consistently, causing the result to drop to 0 again, but it quickly recovered.

# Precautions
Genetic algorithms are a much, **MUCH** slower method of training neural nets compared to backpropagation, and due to the random nature of generation, you may reach an optimal net within just 10 generations or if you're unlucky, within 100 generations. It all depends on the task at hand.

# What EvoNet has been used for so far
### Successful uses:
* **Pong**

Needed around 10 generations to learn, it could consistently beat me, 10 to 1.
The movement of the paddle was also quite natural.

* **Predicting Euro's rise/fall (still in testing)**

As this is a much harder problem and the fact that market is unpredictable, I evolve 12000 nets per hour on the USD/EUR exchange data. So far, there have been 4 million nets created. Top nets (~20 nets) predict change of Euro correctly %70 of the time. However it has yet to be seen whether the predictions are consistent over months and whether nets can predict big changes.

### Unsuccessful uses:
* **Game of 2048**
No matter the training, no net has ever broken the record of 256.
