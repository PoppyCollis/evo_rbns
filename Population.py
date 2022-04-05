#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 12:57:04 2021
Population class initialises a population of associative connection matrices 
and sets an initial state for a single evolutionary run.
@author: Poppy Collis
"""
import random
import itertools
import numpy as np
from numpy.random import choice


class Population():
    
    def __init__(self, nodes, k_inputs, p_value, pop_size, self_inputs):
        self.nodes = nodes
        self.k_inputs = k_inputs
        self.p_value = p_value
        self.pop_size = pop_size
        self.self_inputs = self_inputs
    
        self.prob_dist = 1-self.p_value, self.p_value
        
        # get truth table combinations
        self.tt_inputs = self.get_truth_table()
        
        # initialise the populations
        self.pop_connections = self.initialise_population_connections()
        
        # don't need to initialise the truth table output population
        # as this will be done by the GA
        #self.population = self.initialise_population_genes()
        
        # get initial state
        self.initial_state = np.random.choice([0, 1], self.nodes)

    def get_truth_table(self): 
        combinations = np.array(list(itertools.product([0, 1], repeat = self.k_inputs)))
        return combinations
    
    def get_tt_outputs(self):
        # number of combinanations from truth table is 2^k
        outputs = choice([0, 1], (2**self.k_inputs), self.prob_dist)
        return outputs
    
    def get_node_connections(self):
        conn_array = np.zeros([self.nodes, self.k_inputs], dtype='uint8')
        for i in range(self.nodes):
            if self.self_inputs == True:
                to_exclude = []
            else:
                to_exclude = [i]
            a = random.sample(list(set([x for x in range(self.nodes)]) - set(to_exclude)), k = self.k_inputs)
            conn_array[i]= a
            # this part can be uncommented in order to change the ratio of self-loops
            #sl_ratio = 6 #out of nodes number
            #indexes = random.sample(range(self.nodes), sl_ratio) 
            #for index in indexes:
                #conn_array[index][0] = index
        return conn_array
    
    def initialise_population_genes(self):
        pop = np.zeros([self.pop_size,2**self.k_inputs], dtype='int8')
        for i in range(self.pop_size):
            pop[i] = self.get_tt_outputs()
        return pop
    
    def initialise_population_connections(self):
        pop_conns = np.zeros([self.pop_size,self.nodes,self.k_inputs], dtype='uint8')
        for i in range(self.pop_size):
            pop_conns[i] = self.get_node_connections()
        return pop_conns