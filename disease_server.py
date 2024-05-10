#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 13:10:15 2019

@author: dan
"""

from disease_model_AH import Disease_Model
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider
from mesa.visualization.modules import ChartModule

def agent_portrayal(agent):
    # Set up portrayal dictionary
    portrayal = {"Shape":"circle", "Filled":"true", "r":0.5}
    
    # Specify visual characteristics for infected agents & non-infected agents
    if agent.infected == True:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
        
    return portrayal

# Set up visualisation elements
grid = CanvasGrid(agent_portrayal,10,10,500,500)
# Set up a chart to represent the total infected over time.  We instantiate a
# ChartModule for this, and pass in a dictionary containing the label for the
# data we're plotting and the colour of the line for that data, along with the
# name of the datacollector we want the chart to link to ('datacollector' here)
total_compartments_graph = ChartModule(
        [{"Label":"Total_Infected", "Color":"red"},
        ], #{"Label":"Total_Susceptible", "Color":"blue"}
        data_collector_name='datacollector'
        )

# Set up user sliders
number_of_agents_slider = Slider(
    "Number of Agents", 100, 2, 200, 1)
initial_infection_slider = Slider(
    "Probability of Initial Infection", .05, 0, .1, .01)
transmissibility_slider = Slider(
    "Transmissibility", 0.25, 0.01, 1, 0.01)
level_of_movement_slider = Slider(
    "Level of Movement", 0.9, 0.01, 1, 0.01)
mean_length_of_disease_slider = Slider(
    "Mean Length of Disease (days)", 7, 1, 100, 1)

#################### ADDED #################################
risk_factor_slider = Slider(
    "Risk Factor", 0.4, 0, 1, 0.1)
local_pro_factor_slider = Slider(
    "Local Pro-vaccine Factor", 1.01, 1, 2, 0.01)
local_anti_factor_slider = Slider(
    "Local Anti-vaccine Factor", 0.99, 0, 1, 0.01)
global_pro_factor_slider = Slider(
    "Global Pro-vaccine Factor", 1.01, 1, 2, 0.01)
global_pro_factor_threshold_slider = Slider(
    "Global Pro-vaccine Factor Threshold", 0.5, 0, 1, 0.1)
############################################################


server = ModularServer(Disease_Model, 
                       [grid, total_compartments_graph],
                       "Disease Spread Model", 
                       {"N":number_of_agents_slider, "width":10, "height":10, 
                        "initial_infection":initial_infection_slider, 
                        "transmissibility":transmissibility_slider, 
                        "level_of_movement":level_of_movement_slider, 
                        "mean_length_of_disease":mean_length_of_disease_slider,
                        ################ ADDED ##################################
                        "risk_factor":risk_factor_slider,
                        "local_pro_factor":local_pro_factor_slider,
                        "local_anti_factor":local_anti_factor_slider,
                        "global_pro_factor":global_pro_factor_slider,
                        "global_pro_factor_threshold":global_pro_factor_threshold_slider}
                        #########################################################
                       )

