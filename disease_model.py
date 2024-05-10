#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:42:28 2019

@author: dan

Adapted by Alisa Hamilton Dec. 2023
"""

# Resources for original model by HSMA
# HSMA Video Tutorial: https://www.youtube.com/watch?v=VeQkhfDYyMc
# HSMA GitHub: https://github.com/hsma-programme/6b_agent_based_simulation_using_mesa/tree/main/6B_Agent_Based_Simulation_using_MESA_Part_1

import numpy as np
from mesa import Agent, Model
from mesa.time import RandomActivation                                         # random order of agent actions
from mesa.space import MultiGrid                                               # multiple agents per cell
from mesa.datacollection import DataCollector
import random
np.random.seed(34)

# N = 100                                                                      # These are sliders. See disease_server_AH.py.
# risk_factor = 0.4                                                            
# local_pro_factor = 1.01
# local_anti_factor = 0.99
# global_pro_factor = 1.01
# global_pro_factor_threshold = 0.5

class Person_Agent(Agent):                                                     # Agent class with slider inputs
    def __init__(self, unique_id, model, initial_infection, transmissibility, 
                 level_of_movement, mean_length_of_disease,
                 ##################### ADDED ####################
                 risk_factor,local_pro_factor,local_anti_factor,               # These are sliders I added.         
                 global_pro_factor,global_pro_factor_threshold, ): 
                 ################################################
        super().__init__(unique_id, model)
        self.transmissibility = transmissibility                               # Probability of getting infected if in contact with infected person.
        self.level_of_movement = level_of_movement                             # Probability of movement each step.
        self.mean_length_of_disease = mean_length_of_disease                   # Mean length of disease in days.
        ######################## ADDED ##############################
        self.risk_factor = risk_factor                                         # If vaccinated, multiply the infection chance by this number.
        self.local_pro_factor = local_pro_factor                               # If most of my nearest neighbors are vaccinated, multiply the probababilty of getting vaccinated by this number.
        self.local_anti_factor = local_anti_factor                             # If most of my nearest neighbors are not vaccinated, multiply the probability of getting vaccinated by this number.
        self.global_pro_factor = global_pro_factor                             # If the population infection prevalence is more than the global-pro-factor-threshold, multiply the probability of getting vaccinated by this number.
        self.global_pro_factor_threshold = global_pro_factor_threshold         # If the infection prevalence above this number, multiply the probability of getting vaccinated by the global-pro-factor
        self.vaccine_prob = random.uniform(0, 1)                               # Probability between 0 and 1, which represents their propensity to get vaccinated
        #############################################################
        self.susceptible = True                                                # Initially, everyone is susceptible and 
        self.recovered = False                                                 # No one is recovered and
        self.vaccinated = False
        # No one is vaccinated.
        if random.uniform(0, 1) < initial_infection:                           # initial_infection is the probablity of starting out infected.
            self.infected = True                                               # Some people start out infected
            self.susceptible = False
            self.disease_duration = int(round(
                    random.expovariate(1.0 / self.mean_length_of_disease), 0)) # The disease duration is decremented for those who start out infected.
        else:
            self.infected = False
            self.susceptible = True
            
    def move(self):                                                            # Agents move each step using the Moore Neighborhood (8 possible moves, including diagonals)
        possible_steps = self.model.grid.get_neighborhood(                     # Find possible neighbouring cells to which to move.
                self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)                           # Select new position at random
        self.model.grid.move_agent(self, new_position)                         # Move the agent
        
    def infect(self):                                                          # Agent infection function
        #################### ADDED ##################
        self.temp_risk_factor = 1 
        self.temp_transmissibility = 1 
        if self.vaccinated == True: 
            self.temp_risk_factor = self.risk_factor
        #############################################
        cellmates = self.model.grid.get_cell_list_contents([self.pos])         # Get list of agents in this cell
        if len(cellmates) > 1:                                                 # Check if there are other agents here.
            for inhabitant in cellmates:                                       # For each agent in the cell,
                if ((inhabitant.infected == False) &                           # infect the agent with a given probability (transmissibility)
                    (inhabitant.recovered == False)):                          # if they're not already infected.
                    if random.uniform(0, 1) < (self.transmissibility * self.temp_risk_factor):           
                        inhabitant.infected = True
                        inhabitant.susceptible = False
                        inhabitant.disease_duration = int(round(
                                random.expovariate(
                                        1.0 / self.mean_length_of_disease), 0))
                        
    def vaccine_prob_inc(self):
        if (sum(agent.infected == True for agent in self.model.schedule.agents) / self.model.num_agents) > self.global_pro_factor_threshold:   # sum(agent.infected == True for agent in Model.schedule.agents)
            self.vaccine_prob *= self.global_pro_factor
    
    def vaccinate(self):
        if self.susceptible==True:
             if self.vaccine_prob>0.9:
                 self.vaccinated = True

    def step(self):
        if random.uniform(0, 1) < self.level_of_movement:                      # Step function
            self.move()                                                        # Move with given probability
        
        self.vaccine_prob_inc()
        self.vaccinate()
        
        if self.infected == True:                                              # Begin infecting cellmates (if agent is infected) and
            self.infect()
            self.disease_duration -= 1                                         # decrement remaining disease duration by one time unit.
            if self.disease_duration <= 0:                                     # If disease has now run its course, flag that the agent is no 
                self.infected = False                                          # longer infected.
        
class Disease_Model(Model):
    def __init__(self, N, width, height, initial_infection, transmissibility,  # 2D Model initialisation function - initialise with N agents, and 
                 level_of_movement, mean_length_of_disease, 
                 ################### ADDED ########################
                 risk_factor, local_pro_factor, local_anti_factor,
                 global_pro_factor,global_pro_factor_threshold):                   # specified width and height.
                 ####################################################
        self.running = True                                                    # Required for BatchRunner.
        self.num_agents = N                                                    # Assign number of agents at initialisation.
        self.grid = MultiGrid(width, height, True)                             # Setup Toroidal multi-grid.
        self.schedule = RandomActivation(self)                                 # Set up a scheduler with random order of agents being activated each turn. 
        for i in range(self.num_agents):                                       # Create agents up to number specified.
            a = Person_Agent(i, self, initial_infection, transmissibility,     # Create agent with ID taken from for loop.
                             level_of_movement, mean_length_of_disease, 
                             risk_factor, local_pro_factor, local_anti_factor,
                             global_pro_factor,global_pro_factor_threshold)
            self.schedule.add(a)                                               # Add agent to the schedule.
            try:                                                               # Try adding the agent to a random empty cell
                start_cell = self.grid.find_empty()
                self.grid.place_agent(a, start_cell)
            except:                                                            # If you can't find an empty cell, just pick any cell at random
                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)
                self.grid.place_agent(a, (x,y))
                
# Create a new datacollector, and pass in a model reporter as a
# dictionary entry, with the index value as the name of the result
# (which we'll refer to by this name elsewhere) and the lookup value
# as the name of the function we created below that will calculate
# the result we're reporting
        self.datacollector = DataCollector(
                model_reporters={"Total_Infected":calculate_number_infected,
                                 "Total_Recovered":calculate_number_recovered,
                                 "Total_Susceptible":calculate_number_susceptible,
                                 "Total_Vaccinated":calculate_number_vaccinated}, #"Proportion_Infected":calculate_prop_infected
                agent_reporters={})
                
    def step(self):                                                            # Function to advance the model by one step
        self.schedule.step()                                                   # Tell the datacollector to collect data from the specified model
        self.datacollector.collect(self)                                       # and agent reporters

# Function to calculate total number infected in the model
# The function takes as an input a model object for which we want to calculate
# these results
def calculate_number_infected(model):
    total_infected = 0                                                         # set up a counter with default value of 0 that will keep count of the total number infected
    infection_report = [agent.infected for agent in model.schedule.agents]     # use list comprehension to establish a new list that contains the infected variable value of each agent in the model
    
    # loop through the stored variable values which indicate whether each
    # agent is infected, and for each one that is True incremenent the total
    # number of infected by 1
    for x in infection_report:
        if x == True:
            total_infected += 1
            
    
    return total_infected                                                      # Return the total number of infected as the output from the function

def calculate_number_recovered(model):
    total_recovered = 0
    recovered_report = [agent.recovered for agent in model.schedule.agents]
    for x in recovered_report:
        if x == True:
            total_recovered += 1
    return total_recovered

def calculate_number_susceptible(model):
    total_susceptible = 0
    susceptible_report = [agent.susceptible for agent in model.schedule.agents]
    for x in susceptible_report:
        if x == True:
            total_susceptible += 1
    return total_susceptible

##################### ADDED ##############################
def calculate_number_vaccinated(model):
    total_vaccinated = 0
    vaccinated_report = [agent.vaccinated for agent in model.schedule.agents]
    for x in vaccinated_report:
        if x == True:
            total_vaccinated += 1
    return total_vaccinated
#########################################################




