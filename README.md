##Background
Adaptive human behavior was largely absent from COVID-19 models used for decision making despite knowledge of its importance in the spread of infectious disease. Human behavior may be incorporated into disease models either exogenously or endogenously. A model with exogenous human behavior may input longitudinal mobility data or change parameters at fixed time points. Correlations between mobility data and health burden may change over time, and changing parameters at fixed time points does not anticipate future behavioral responses. In contrast, including behavior endogenously (as a function of another time-dependent variable within the model) attempts to capture the fluctuating nature of human behavior in response to a changing epidemic. 

A common approach to include endogenous behavior is using a feedback loop where behavior changes as a function of disease prevalence. For this project, I adapted a simple SIR model to include a vaccinated state (V). Individuals choose to get vaccinated based on local and global information about the number of vaccinated and infected individuals, respectively. I first adapted the epiDem model in NetLogo and then I adapted a similar model by HSMA in python.

•	epiDem:https://ccl.northwestern.edu/netlogo/models/epiDEMBasic
•	HSMA: https://github.com/hsma-programme/6b_agent_based_simulation_using_mesa/tree/main/6B_Agent_Based_Simulation_using_MESA_Part_1

This project was completed as part of an independent study on agent-based modeling for a PhD in Systems Engineering at Johns Hopkins University.

##NetLogo

The NetLogo code was adapted from the epiDem NetLogo model by Yang and Wilenskey 2011.

Based on the Kermack-McKendrick model, the epiDem model is an introductory model of infectious disease spread that assumes a closed population, homogenous mixing, no latent or dormant periods, and no viral mutation. Each time step represents one hour, but this could be any time unit. I adapted the model to include vaccination and two risk groups. In the adapted model, individuals decide to get vaccinated based on local information (vaccinated links) and global information (infection prevalence at time t). I also added code to record the epidemic peak (maximum number of hourly infections) and the peak day.

**Turtles**

Each turtle has an infection state (susceptible, infected, cured, or vaccinated) as well as a risk group and a vaccination probability ('vaccine_prob'). By default, all turtles are in risk group 1. Some turtles are then assigned to risk group 2, which has a higher infection chance than risk group 1. To begin, turtles are randomly assigned a vaccination probability between 0 and 1, which represents their propensity to get vaccinated. The probability of vaccination increases in one of two ways: 1) when the prevalence of infections reaches a 50% and 2) when the majority of in-coming links are vaccinated. The probability of vaccination decreases when the majority of incoming links are not vaccinated. When the vaccination probability is greater than 0.9, the turtle moves to the vaccinated state. Vaccinated turtles have a lower infection chance.

**Input variables**

The following parameters are from the initial epiDEM model: population size ('initial-people'), infection-chance, recovery-chance, and average-recovery-time. To include a process of vaccination, I added the following input variables: 
•	risk_prob: If vaccinated, multiply the infection chance by this number.
•	local-pro-factor: If most of my nearest neighbors are vaccinated, multiply the probability of getting vaccinated by this number.
•	local-anti-factor: If most of my nearest neighbors are not vaccinated, multiply the probability of getting vaccinated by this number.
•	global-pro-factor: If the population infection prevalence is more than the global-pro-factor-threshold, multiply the probability of getting vaccinated by this number.
•	global-pro-factor-threshold: If the infection prevalence above this number, multiply the probability of getting vaccinated by the global-pro-factor

**Setup procedures**

Turtles are randomly assigned an x and y coordinate in the 25x25 grid space. To begin, all turtles are susceptible and none are vaccinated. Out of the 100 turtles in the population, 50 are assigned to risk group 2. The recovery time for each turtle is set to be random around an average recovery time with a normal distribution. Each turtle has a 5% chance of starting out infected. Turtles create links with 8 other turtles. The random seed is set at 42.

**Go procedures**

At each time step, turtles move around the space at random and potentially change state. Infection occurs based on nearby infections. Vaccination occurs based on local and global information as described above. Recovery can occur if the turtle has been infected more than the average recovery time. Finally, the basic reproduction number is calculated using the transmission and recovery rates. The epidemic peak (maximum number of infections/hour) and the peak hour are also recorded. In the NetLogo code, original epiDEM comments are to the left and use ';;' while my comments are to the right and use ';'.

**Run NetLogo**

Open ABM_epiDem_v2.nlogo and click setup and go on the interface tab. To run a version without vaccination, comment out the vaccine_prob_inc and vaccinate functions in the to-go procedure.

##Python
The python code was apdapted from a model by HSMA which uses the mesa library (a library for ABMs) to include a vaccinated state. Individuals are assigned a random vaccine probability which increases by a factor of 1.01 for every time-step the infection prevalence is over 50%. Once their vaccine probability reaches 90%, they enter the vaccinated state, which has a reduced infection chance. 

The python model is similar to the NetLogo model except the time step is in days instead of hours and it uses a different movement pattern. In python, agents move forward through a grid (Moore Neighborhood - 8 directions including diagonals) each day, whereas in NetLogo, they move forward with a 0¬¬–360 degree rotation each hour. I have not yet included the impact of local information (vaccinated peers) or incorporated a second risk group in the python version. 

**Run Python**
Open all three .py files at once and run disease_run_AH.py. This will open a browser; press start. To run a version without vaccination, comment out self.vaccine_prob_inc() and self.vaccinate() in the Agent class step function (lines 100 and 101) in the file disease_model_AH.py. You may need to close the browser and restart the kernel between each run. !

