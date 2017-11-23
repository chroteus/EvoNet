import random, json, os
from . import generator
from .network import Network
#from .alpha_evo import AlphaEvo
from operator import attrgetter # for network sorting
"""
    Main genetic algorithm module.
    For simpler applications using this class alone should suffice.

    input_no argument is not actually needed due to
    the nature of the network, however it makes sure that network
    generates atleast input_no+output_no neurons to prevent errors.
"""


class Evo:
    def __init__(self, net_no=500, input_no=1,output_no=1,
                 chosen_no=None, elite_no=None,
                 mix_conns=False, empty=False, custom_net_class=None,
                 max_neurons_per_net=500):
        self.net_no = net_no # nets per generation

        # nets chosen to breed
        self.chosen_no = chosen_no if chosen_no else round(self.net_no / 4)
        # nets passed unchanged
        self.elite_no = elite_no if elite_no else round(self.chosen_no/10)
        self.elite_no = min(self.elite_no,self.chosen_no)

        self.net_class = custom_net_class
        if custom_net_class == None:
            self.net_class = Network

        self.curr_net_i = 0
        self.nets = []
        self.current_gen = 0
        self.gen_record = 0
        self.best_record = 0
        self.input_no = input_no
        self.output_no = output_no
        self.mix_conns = mix_conns
        self.max_neurons_per_net = max_neurons_per_net

        self.reset_fitness_func_input()

        if not empty: self.fill_with_nets()

    """
        Fitness function is to be called on each net to
        determine its fitness.
        Fitness function MUST return a numeric value.
    """
    def set_fitness_func(self, func):
        self.fitness_func = func

    """
        Set arguments for fitness function.
    """
    def set_fitness_func_input(self, *args, **kwargs):
        self.fitness_args = args
        self.fitness_kwargs = kwargs

    """
        Reset fitness func args in case you need to change them.
    """
    def reset_fitness_func_input(self):
        self.fitness_args = ()
        self.fitness_kwargs = {}


    """
        Process specified number of generations.
    """
    def evolve_for(self, gen_no):
        for i in range(gen_no):
            for net in self.nets:
                fitness = self.fitness_func(self,net, *self.fitness_args,**self.fitness_kwargs)
                self.nets[self.curr_net_i].fitness = fitness

                self.best_record = max(fitness, self.best_record)
                self.gen_record = max(fitness, self.gen_record)
                self.curr_net_i += 1

            self.next_gen()

    """
        Process next generation.
        Leave top, or "elite" nets untouched for next generation,
        and another portion, "chosen" nets to pass on to next generation
        by "reproducing", or mixing each others' weights, and if specified,
        connections too.
    """
    def next_gen(self):
        self.curr_net_i = 0
        self.current_gen += 1
        self.gen_record = 0
        new_nets = []

        for net in self.nets:
            net.reset_values()

        self.nets.sort(key=attrgetter("fitness"), reverse=True)
        if hasattr(self, "alpha_evo"): # alpha nets enabled?
            self.alpha_evo = AlphaEvo(self)
            self.alpha_evo.evolve_for(self.alpha_gens)
            alpha_net = self.alpha_evo.nets[0]
            new_nets.append(self.alpha_evo.nets[0])

        for ni in range(self.elite_no):
            new_nets.append(self.nets[ni])

        for ni1 in range(self.elite_no, self.chosen_no):
            ni2 = random.randrange(self.chosen_no)
            new_net = self.nets[ni1].reproduce_with(self.nets[ni2], mix_conns=self.mix_conns, class_to_use=self.net_class)
            new_nets.append(new_net)

        self.nets = new_nets

        self.fill_with_nets() # fill empty spaces
        self.nets.sort(key=attrgetter("fitness"), reverse=True)

    """
        Alpha net is the top net.
        Alpha nets' weights will be improved with an additional GA applied to
        their weights, without modification of the topology.
        It uses the same fitness function as parent Evo
    """
    def enable_alpha_net(self,alpha_gens=10):
        assert self.fitness_func, "Define a fitness function before enabling alpha net!"
        self.alpha_evo = True #AlphaEvo itself is initialized at the end of gen
        self.alpha_gens = alpha_gens

    """
        Generate nets until reaches the limit (self.net_no)
    """
    def fill_with_nets(self):
        while len(self.nets) < self.net_no:
            neuron_number = self.input_no+self.output_no
            weights,conns = generator.network(min_n=neuron_number,max_n=self.max_neurons_per_net)
            self.nets.append(self.net_class(weights,conns, input_no=self.input_no,output_no=self.output_no))
            self.nets[-1].fitness = 0

    def get_current_net(self):
        return self.nets[self.curr_net_i]

    def save(self, path, max_nets=None):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        f = open(path, "w")
        if not max_nets: max_nets = len(self.nets)
        net_strs = [str(n) for n in self.nets[:max_nets]]
        json.dump(net_strs, f)
        f.close()

    def __str__(self):
        return "Gen " + str(self.current_gen) + ": " + str(self.curr_net_i) + "/" + str(self.net_no) \
        + "\nGen record: " + str(round(self.gen_record,2)) \
        + "\nAll-time record: " + str(round(self.best_record,2)) \
        + "\n\n" \
        + "Neuron number: " + str(len(self.get_current_net().neurons))


"""
    Improve weights of absolute top net using another genetic algorithm.
    Alpha nets (1 per gen) are elite of elites.
    This class is used internally by the main Evo class, and thus
    it's not recommended to use this class alone.
"""
class AlphaEvo(Evo):
    def __init__(self, evo):
        self.evo = evo
        super().__init__(input_no=evo.input_no,
                         output_no=evo.output_no,
                         net_no=50,chosen_no=10,
                         elite_no=2, custom_net_class=evo.net_class,
                         mix_conns=False,
                         empty=True)
        self.set_fitness_func(evo.fitness_func)
        alpha_net = evo.nets[0]
        self.nets.append(
            self.net_class(
                alpha_net.weights_data, alpha_net.connection_data,
                input_no=self.input_no,output_no=self.output_no)
        )
        self.fill_with_nets()

    def fill_with_nets(self):
        alpha_net = self.evo.nets[0]
        while len(self.nets) < self.net_no:
            weights = []

            # generate weights, but leave same topology
            for ni,conn in enumerate(alpha_net.connection_data):
                weights.append([])
                for wi in range(len(conn)):
                    weights[ni].append(generator.new_weight())

            self.nets.append(
                self.net_class(
                    weights,alpha_net.connection_data,
                    input_no=self.input_no,output_no=self.output_no
                )
            )
