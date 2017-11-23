# EvoNet
EvoNet is an *experimental* project developed to train neural networks by evolving its topology and weights at the same time using a genetic algorithm.
Unlike usual layer-based neural nets, EvoNet has arbitrary connections between neurons and is thus pretty universal.  

# An example net
The net below is the top net from my tests on evolving nets to play Pong.
Neurons 0 and 1 are input neurons (ball's position) and neuron 8 is the output neuron (paddle's x position).
Blue connections are negative and red connections are positive.
The connection's width represent the weight of that connection.

The only way that input neurons differ from other neurons is that they additionally take input from user.

![Net](https://user-images.githubusercontent.com/5436911/31634628-de5421ca-b2cc-11e7-9f22-b98981106654.png)


# A very simple example of net training
Here, we try to predict the next step in sin wave.

```python
import math, random
import EvoNet as evonet
from matplotlib import pyplot

def test_func(x):
    x /= 10
    return math.sin(x)


evo = evonet.evo.Evo(input_no=10,
                     output_no=1,
                     net_no=400,
                     max_neurons_per_net=50,
                     elite_no=5,
                     mix_conns=True)

def sin_fitness(evo,net):
    fitness = 0
    for i in range(10): # repeat tests
        rand_start = random.randint(-99999,99999)
        # feed 10 samples of sin
        sin_wave = [test_func(x) for x in range(rand_start, rand_start+evo.input_no)]
        real_value = test_func((rand_start+evo.input_no))

        net.set_input(sin_wave)
        prediction = net.get_output()[0]
        net.reset_values()

        # the lower the difference, the closer the value is to 1
        fitness += math.exp(-abs(prediction-real_value))

    return fitness/10

evo.set_fitness_func(sin_fitness)

# evolve for 20 gens and see results
for i in range(20):
    evo.evolve_for(1)
    best_net = evo.nets[0]
    print(best_net.fitness)
    # predict
    real_values = []
    predicted_values = []
    for i in range(150):
        real_values.append(test_func(i))

        input_data = [test_func(x) for x in range(i-evo.input_no, i)]

        best_net.set_input(input_data)
        prediction = best_net.get_output()[0]
        best_net.reset_values()
        predicted_values.append(prediction)

    pyplot.plot(real_values)
    pyplot.plot(predicted_values)
    pyplot.show()

```

Here are outputs of network from Gen 1 and Gen 8, respectively:
![gen 1](https://user-images.githubusercontent.com/5436911/33179904-ad758d9a-d073-11e7-833a-a9f0e0899813.png)
![gen 8](https://user-images.githubusercontent.com/5436911/33179906-ada70afa-d073-11e7-9c7b-662cd51f41b2.png)

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
