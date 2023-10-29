#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
This module provides functions for simulating alternative universes
with randomized data on cheaters' behaviour and calculating how the
number of teams with several cheaters, the number of 'victim cheaters',
and the number of 'observer cheaters' varies.
'''

import random
from collections import defaultdict
from numpy import std

from reading_files import *
from statistical_methods import *
from cheaters_teaming_up import *
from cheaters_interactions import *
from team_randomization import *
from kills_randomization import *


def cheaters_teaming_up_simulation(n):
    ''' Calculates the expected value and confidence intervals for the
    number of teams with 0, 1, 2, 3, and 4 cheaters, based on data from
    n simulations.
    
    Takes as argument an integer n, which defines the number of simulations
    to perform.
    
    Returns 5 strings and 5 integer values, which correspond to the
    confidence intervals and expected values of the number of teams
    with 0, 1, 2, 3, and 4 cheaters.
    ''' 
    
    # Firstly, so that the simulations work on their own, I obtain
    # the data directly from the text files.
    cheaters = get_cheaters()
    teams = get_teams()

    # Then, I create lists which will hold the estimates of each simulation.
    zero_cheaters_list = []
    one_cheater_list = []
    two_cheaters_list = []
    three_cheaters_list = []
    four_cheaters_list = []

    # Then, I go through with the simulation.
    for i in range(n):
        
        # I start by updating the teams list with the new randomized data.
        teams = get_shuffled_teams(teams)

        # Then, I obtain the counts of teams with 0, 1, 2, 3, or 4 cheaters
        # assuming the new shuffled data.
        zero_cheaters, one_cheater, two_cheaters, three_cheaters, four_cheaters =         get_cheater_counters(cheaters, teams)
                
        # Finally, I store the relevant information in the previously created lists.
        zero_cheaters_list.append(zero_cheaters)
        one_cheater_list.append(one_cheater)
        two_cheaters_list.append(two_cheaters)
        three_cheaters_list.append(three_cheaters)
        four_cheaters_list.append(four_cheaters)

    # Once that is done, I can present the confidence intervals and means for 
    # each of the counters.
    ci_zero_cheaters = confidence_interval(zero_cheaters_list)
    ci_one_cheater = confidence_interval(one_cheater_list)
    ci_two_cheaters = confidence_interval(two_cheaters_list)
    ci_three_cheaters = confidence_interval(three_cheaters_list)
    ci_four_cheaters = confidence_interval(four_cheaters_list)
    
    mean_zero_cheaters = mean(zero_cheaters_list)
    mean_one_cheater = mean(one_cheater_list)
    mean_two_cheaters = mean(two_cheaters_list)
    mean_three_cheaters = mean(three_cheaters_list)
    mean_four_cheaters = mean(four_cheaters_list)
    
    return ci_zero_cheaters, mean_zero_cheaters, ci_one_cheater, mean_one_cheater,             ci_two_cheaters, mean_two_cheaters, ci_three_cheaters, mean_three_cheaters,               ci_four_cheaters, mean_four_cheaters


def victim_cheaters_simulation(n):
    ''' Calculates the expected value and confidence intervals for the
    number of players that started cheating only after having been killed
    by an a player that was already cheating.
    
    Takes as argument an integer n, which defines the number of simulations
    to perform.
    
    Returns 1 strings and 1 integer value, which correspond to the confidence
    interval and expected value of the number of these 'victim cheaters'.
    ''' 
    
    # Firstly, so that the simulations work on their own, I obtain
    # the data directly from the text files.
    cheaters = get_cheaters()
    teams = get_teams()
    kills = get_kills()

    # Then, I create a list which will hold the estimates of each simulation.
    vic_cheaters_ev_list = []

    # Then, I go through with the simulation.
    for i in range(n):
        
        # I start by updating the kills list with the new randomized data.
        kills = get_shuffled_kills(kills)

        # Then, I obtain the estimated number of 'victim cheaters'.
        matches_start = match_starting_time(kills)
        vic_cheaters_ev = counter_victim_cheaters(kills, matches_start, cheaters)
        
        # Finally, I store the relevant information in the previously created list.
        vic_cheaters_ev_list.append(vic_cheaters_ev)

    # Now, I can compute the confidence intervals and mean from the estimates.
    ci_victim_cheaters = confidence_interval(vic_cheaters_ev_list)
    mean_victim_cheaters = mean(vic_cheaters_ev_list)
    
    return ci_victim_cheaters, mean_victim_cheaters


def observer_cheaters_simulation(n):
    ''' Calculates the expected value and confidence intervals for the
    number of players that started cheating only after having observed
    an actively cheating player obtain at least 3 kills.
    
    Takes as argument an integer n, which defines the number of simulations
    to perform.
    
    Returns 1 string and 1 integer value, which correspond to the confidence
    interval and expected value of the number of these 'observer cheaters'.
    ''' 
    
    # Firstly, so that the simulations work on their own, I obtain
    # the data directly from the text files.
    cheaters = get_cheaters()
    teams = get_teams()
    kills = get_kills()

    # Then, I create a list which will hold the estimates of each simulation.
    obs_cheaters_ev_list = []

    # Then, I go through with the simulation.
    for i in range(n):
        
        # I start by updating the kills list with the new randomized data.
        kills = get_shuffled_kills(kills)

        # Then, I obtain the estimated number of 'observer cheaters'.
        obs_cheaters_ev = get_observer_cheaters(cheaters, kills)
        
        # Finally, I store the relevant information in the previously created list.
        obs_cheaters_ev_list.append(obs_cheaters_ev)

    # Now, I can compute the confidence intervals and mean from the estimates.
    ci_observer_cheaters = confidence_interval(obs_cheaters_ev_list)
    mean_observer_cheaters = mean(obs_cheaters_ev_list)
    
    return ci_observer_cheaters, mean_observer_cheaters

