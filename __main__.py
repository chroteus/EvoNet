import helpers, generator, json, os, random
from Network import Network
from Evo import Evo
def main():
    #demo
    evo = Evo(input_no=2,output_no=1,
              net_no = 300,
              chosen_no=100,
              mix_conns=False)

    def xor_fitness(evo,net):
        a = random.choice((0,1))
        b = random.choice((0,1))
        real_out = a ^ b #xor operator
        net.set_input([a,b])
        net_out = net.get_output()[0]

        return 1/((net_out-real_out)**2)

    evo.set_fitness_func(xor_fitness)

    for i in range(10):
        evo.evolve_for(1)
        top_net = evo.nets[0]
        top_net.set_input([1,0])
        out = top_net.get_output()[0]
        print("GEN " + str(i) + ": Expected 1, got " + str(out))


if __name__ == "__main__":
    main()
