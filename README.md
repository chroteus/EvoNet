# EvoNet
EvoNet is an *experimental* project developed to train neural networks by evolving its topology and weights at the same time using a genetic algorithm.
Unlike usual layer-based neural nets, EvoNet has arbitrary connections between neurons, sometimes neurons can even be self-connecting, which means the net has a very basic form of memory, and thus its output depends on the output of its previous runs.

*TODO: Add visualisation of an example network*

# Example of net training
```python
import evonet

# init the main class
evo = evonet.Evo.Evo(input_no=2,output_no=1,
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
    return 1/((net_out-real_out)**2)

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

As this is a much harder problem and the fact that market is unpredictable, I evolve 12000 nets per hour on the USD/EUR exchange data. So far, there have been 4 million nets created. Top nets (~20 nets) predict change of Euro correctly %70 of the time. However it has yet to be seen whether the predictions are consistent and whether nets can predict big changes.

### Unsuccessful uses:
* **Game of 2048**
No matter the training, no net has ever broken the record of 256.
