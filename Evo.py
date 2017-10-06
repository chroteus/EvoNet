import random, generator
from Network import Network
from operator import attrgetter # for network sorting

class Evo:
    def __init__(self, net_no=500, chosen_no=200, input_no=1,output_no=1,
                 mix_conns=True, empty=False):
        self.net_no = net_no # nets per generation

        if not chosen_no: self.chosen_no = round(self.net_no / 3)
        self.chosen_no = chosen_no # nets chosen to breed
        if chosen_no > net_no: chosen_no = net_no

        self.elite_no = round(chosen_no/10) # nets passed unchanged

        self.curr_net_i = 0
        self.nets = []
        self.current_gen = 1
        self.gen_record = 0
        self.best_record = 0
        self.input_no = input_no
        self.output_no = output_no
        self.mix_conns = mix_conns
        if not empty: self.fill_with_nets()

    #fitnessFunc MUST return a fitness
    def set_fitness_func(self, func):
        self.fitness_func = func

    def evolve(self): #evolve, nonstop
        for net in self.nets:
            fitness = self.fitness_func(self,net)
            self.nets[self.curr_net_i].fitness = fitness

            self.best_record = max(fitness, self.best_record)
            self.gen_record = max(fitness, self.gen_record)
            self.curr_net_i += 1

        self.next_gen()

    def evolve_for(self, gen_no):
        self.gen_limit = gen_no
        self.evolve()

    def next_gen(self):
        self.curr_net_i = 0
        self.current_gen += 1

        self.gen_record = 0
        new_nets = []
        self.nets.sort(key=attrgetter("fitness"), reverse=True)

        if not self.gen_limit or self.gen_limit <= self.current_gen:
            for ni in range(self.elite_no):
                new_nets.append(self.nets[ni])

            for ni1 in range(self.elite_no, self.chosen_no+self.elite_no):
                ni2 = random.randrange(self.elite_no, self.chosen_no+self.elite_no)
                new_net = self.nets[ni1].reproduce_with(self.nets[ni2], mix_conns=self.mix_conns)
                new_nets.append(new_net)

            self.fill_with_nets()
            self.evolve()

    def fill_with_nets(self):
        while len(self.nets) < self.net_no:
            neuron_number = self.input_no+self.output_no
            weights,conns = generator.network(min_neuron_number=neuron_number)
            self.nets.append(Network(weights,conns, input_no=self.input_no,output_no=self.output_no))
            self.nets[-1].fitness = 0

    def get_current_net(self):
        return self.nets[self.curr_net_i]

    from os import linesep
    def __str__(self):
        return "Gen " + str(self.current_gen) + ": " + str(self.curr_net_i) + "/" + str(self.net_no) \
        + "\nGen record: " + str(round(self.gen_record,2)) \
        + "\nAll-time record: " + str(round(self.best_record,2)) \
        + "\n\n" \
        + "Neuron number: " + str(len(self.get_current_net().neurons))
