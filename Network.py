#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 16:41:29 2021
Runs the GA which assesses fitness by running each network instantiation using
the network class
@author: Poppy Collis
"""
import numpy as np
import math
import random
import matplotlib.pyplot as plt
from numpy.random import choice
from Population import Population
import time

# RBN parameters
n = 20
k = 3
p_value = 0.788675
prob_dist = prob_dist = 1-p_value, p_value
iterations = 1000 #network iters
target_len = 50

# GA parameters
pop_size = 30
genes_no = n
tournaments_no = 2000
deme_size = 6 #make sure even number
mut_rate =  90 #out of max 100%
cross_rate = 0.5 #out of 1

#fit = np.zeros(tournaments_no,)


# -----------------------------------------------------------------------------
#                                   RUN NETWORK
#------------------------------------------------------------------------------

class Network():
    
    def __init__(self, nodes, k_inputs, iter_num, population, indiv_index, target_length):
        self.nodes = nodes
        self.k_inputs = k_inputs
        self.iter_num = iter_num
        self.population = population
        self.indiv_index = indiv_index
        self.target_length = target_length
        
        # load in arrays and nodes
        self.tt_inputs = np.load('tt_inputs.npy')
        self.connection_matrix = np.load('connections.npy')
        self.state = np.load('initial_state.npy')
        
        self.tt_outputs = self.population[self.indiv_index]
        self.node_conns = self.connection_matrix[self.indiv_index]
        
        self.fitness = self.get_fitness(self.run_network())
                
    def get_converted_conns(self): # can I take out for loops?
        converted_conns = np.copy(self.node_conns)
        for i in range(self.nodes):
            for j in range(self.k_inputs):
                converted_conns[i][j] = self.state[self.node_conns[i][j]]
        return converted_conns
    
    def get_next_state(self,converted_conns): # can I take out for loops?
        new_node_values = np.zeros(self.nodes, dtype='uint8')
        # take each row of converted connections 1 at a time
        for i in range(self.nodes):
            node_inputs = converted_conns[i]
            # find index of the row of the truth table that matches converted connection row
            index = np.where(np.all(self.tt_inputs==node_inputs,axis=1))
            index = index[0][0]
            # check that they both match, should all return True
            #print(node_inputs==tt_inputs[index])
            # finally, get the boolean value of index of the ttable_outputs
            new_value = self.tt_outputs[index]
            new_node_values[i] = new_value
        return new_node_values
    
    def run_network(self):
        network = np.zeros((self.iter_num, self.nodes), dtype=np.uint8)
        state = self.state
        for i in range(self.iter_num):
            network[i] = self.state
            converted_connections = self.get_converted_conns()
            self.state = self.get_next_state(converted_connections)
        return network
    
    def get_fitness(self,network): 
        unq, count = np.unique(network, axis=0, return_counts=True)
        try:
            attractor_state = unq[count>1][0]
            indexes = np.where(np.all(network==attractor_state,axis=1))
            length = indexes[0][1]-indexes[0][0]
            #print("length:", length)
            error = abs(length - self.target_length)
            fitness = math.pow((1 + error), -1)
            if fitness == 1:
                print('max fitness found!')
            return fitness
        except IndexError:
            #print("No attractor found")
            return 0
        
# -----------------------------------------------------------------------------
#                                   GA
#------------------------------------------------------------------------------

def initialise_population_genes(k_inputs, population_size, probability_dist):
    population = np.zeros([population_size,2**k_inputs], dtype='int8')
    for i in range(population_size):
        population[i] = choice([0, 1], (2**k_inputs), probability_dist)
    return population

def pick_inds(population_size, deme_len):
    n = random.randint(0,(population_size-1))
    n2 = random.randint((n-(0.5*deme_len)), (n+(0.5*deme_len)))
    if n == n2: # to stop them from being the same n
        n2 = n2 + 1
    if n2 > (population_size-1): #loop round demes so continuous
        n2 = n2-(population_size-1)
    first = n
    second = n2
    return first, second #this just returns the index number of the individuals

def find_fitness(n, k, iter_num, pop, individual_ind, target_len):
    net = Network(n, k, iter_num, pop, individual_ind, target_len)
    return net.fitness

def tourn(first_ind, second_ind, nodes, k_inputs, population, target_length, iter_num, i, fit):
    fit_1st = find_fitness(nodes, k_inputs, iter_num, population, first_ind, target_length)
    fit_2nd = find_fitness(nodes, k_inputs, iter_num, population, second_ind, target_length)
    
    if fit_1st == 1 or fit_2nd == 1:
        #just fill in the rest with ones if maximum has been reached
        fit[i:] = 1
        return False
    
    if fit_1st > fit_2nd:
        win = first_ind
        los = second_ind
        if fit_1st > np.amax(fit):
            fit[i] = fit_1st
        else:
            fit[i] = np.amax(fit)
    else:
        win = second_ind
        los = first_ind
        if fit_2nd > np.amax(fit):
            fit[i] = fit_2nd
        else:
            fit[i] = np.amax(fit)
            
    return win, los

def recombine_mut(win, los, population, nodes, crossover_rate, mutation_rate):
    # recombination with 50% probability (crossover)
    # this overwrites half the losers genes with the winners
    l = int(2**k * crossover_rate)
    if l > 0:
        population[los][:l] = population[win][:l]
    if random.randint(0,100) < mutation_rate: #with a probability flip random bit of genome
        j = random.randint(0, ((2**k)-1)) #chose one at random to mutate
        if population[los][j] == 1:
            population[los][j] = 0
        else:
            population[los][j] = 1
    return population

#------------------------------------------------------------------------------

def main():
    
    # define number of independent runs
    runs = 15
    start = time.time()

    # initialise max reached list
    max_reached = []
    
    for i in range(runs):
        
        # initialise a new population (connections, tt_inputs, initial states)
        my_pop = Population(20, 3, 0.788675, 30, False)

        #np.save("saved/population", my_pop.population)
        np.save("tt_inputs", my_pop.tt_inputs)
        np.save("connections", my_pop.pop_connections)
        np.save("initial_state", my_pop.initial_state)


        # initialise the corresponding population of tt_outputs to be evolved
        global pop 
        pop = initialise_population_genes(k, pop_size, prob_dist)
        # initialise empty fitness matrix for storing fitness values
        fit = np.zeros(tournaments_no,)
        
        # for however many tournaments, do...
        for i in range(tournaments_no):
            
            # pick individuals at random within a given deme
            global a, b
            a, b = pick_inds(pop_size, deme_size)
            try:
                # get the fitness and assign winner or a loser
                winner, loser = tourn(a,b,n,k,pop,target_len,iterations, i, fit)
                # overwrite losers genes with half of winners DNA
                pop = recombine_mut(winner, loser, pop, n, cross_rate, mut_rate)
            except TypeError:
                # given that tourn returns False when 1 (max fitness) is reached
                # this causes a typeerror - in this case...
                # then just plot max from then on to save time
                max_reached.append(i)
                break
            
        # if it never reaches max fitness
        print("The highest fitness found")
        print(np.amax(fit))
        print("index of highest")
        print(np.argmax(fit))
        x = np.linspace(0,tournaments_no-1, num=tournaments_no)
        plt.plot(x, fit)
        
    plt.xlabel("Tournaments")
    plt.ylabel("Fitness")
    plt.title(f'Target length: {target_len}')
    
    plt.ylim(ymax=1)

    plt.show()
    
    # return the proportion of successful runs reached
    # also plot the average time that the max fitness is reached
    if runs > 0:
        proportion = len(max_reached) / runs
        print("% of successful runs:", proportion)
    else:
        print(0)
    
    
    
    end = time.time()
    print("Execution time", end - start, "seconds")
    print((end-start)/60, "minutes")
    print((end-start)/60/60, "hours")

    print("Tournaments:", tournaments_no)
    print("Runs:", runs)

    return pop
        
if __name__ == "__main__":
    main()







