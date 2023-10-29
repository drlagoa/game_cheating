#!/usr/bin/env python
# coding: utf-8

# In[2]:


'''
This module provides functions for randomizing the team
allocation among players in a match.
'''

from collections import defaultdict
import random


def matches_composition(teams):
    ''' Creates a dictionary with the composition of matches in terms
    of players and respective team number.
    
    Takes as argument a list, where elements are themselves a list
    with a match id, a player id, and a team number.
    
    Returns a dictionary in which keys are match ids, and each value
    is  composed of two lists, of player ids and of team numbers.
    '''

    match_team_composition = defaultdict(lambda: [[], []])

    for [match_id, player_id, team_id] in teams:
        
        match_team_composition[match_id][0].append(player_id)
        match_team_composition[match_id][1].append(team_id)

    return match_team_composition


def team_shuffle(match_team_composition):
    ''' Randomly shuffles the team allocation among player account ids
    for every match.
    
    Takes as argument a dictionary, where keys are match ids, and where
    the values are lists of the same lenght, one for player ids, and
    the other for corresponding team numbers.
    
    Returns an equivalent dictionary, for which the list of team numbers
    for each match has been shuffled. 
    '''
    
    for key, value in match_team_composition.items():
        temp_list = value[1][:]
        random.shuffle(temp_list)
        match_team_composition[key] = [value[0], temp_list]

    return match_team_composition


def teams_updating(match_team_composition):
    ''' Creates a new list with details of team numbers for each player
    in each match.
    
    Takes as argument a dictionary pairing match ids with two lists as
    values: player ids and team numbers.
    
    Returns a new list of teams, where each element is a list with a
    match id, a player account id, a team number.
    '''
    
    teams = []
    for key, value in match_team_composition.items():
        for index in range(len(value[0])):
            teams.append([key, value[0][index], value[1][index]])
            
    return teams

def get_shuffled_teams(teams):
    ''' Executes the defined functions necessary to obtain a list of teams
    after randomization.
    
    Takes as argument an original list of teams, where elements are lists
    with match id, player account id, and team number.
    
    Returns an equivalent list of teams, with randomized team allocations.
    '''
    
    match_team_composition = matches_composition(teams)
    match_team_composition = team_shuffle(match_team_composition)
    teams = teams_updating(match_team_composition)
    
    return teams

