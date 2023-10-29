#!/usr/bin/env python
# coding: utf-8

# In[2]:


'''
This module provides functions useful for analysing how cheaters
team up. It allows us to calculate the number of cheaters in each
team, the total amount of teams, and number of teams with 0, 1, 2,
3, or 4 cheaters.
'''

from collections import defaultdict


def set_from_dict(dictionary):
    '''Takes a dictionary as an argument and returns a set, where the
    elements are the keys in the input dictionary.
    '''
    
    final_set = set(dictionary.keys())
    return final_set


def cheaters_per_team(teams, cheaters_set):
    '''Counts the amount of cheaters per team.
    
    Takes as argument a list (teams) and a set (cheaters_set). The elements
    in the list are lists with details of team membership for each player
    (match id, player account id, and team number). The elements of the set
    are account ids of cheating players.
    
    Returns two outputs, a dictionary and an integer. For the dictionary,
    the keys are the unique id's of every team (match - team combination),
    and the values are the number of cheaters in that unique team.
    The integer output is the number of teams with no cheaters at all.
    '''
    
    teams_cheaters_dict = defaultdict(int)
    unique_teams_set = set()
    
    # As I iterate over players, I make sure to add the unique team id
    # to the set, so I have the total number of teams.
    # The dictionary serves as a counter of cheating players per team.
    # I iterate over the details for every player, and if the player is
    # a cheater, I add 1 to the counter of the respective team.
    
    for [match_id, player_id, team_number] in teams:    
        
        unique_team_id = match_id + ' - ' + team_number
        
        unique_teams_set.add(unique_team_id)
        
        if player_id in cheaters_set:
            teams_cheaters_dict[unique_team_id] += 1
    
    # I output total_nr_teams in order to calculate how many teams have no
    # cheaters. The alternative of simply including them in the dictionary
    # would result in an unnecessarily large dictionary, which would include
    # all teams with 0 cheaters.
    total_nr_teams = len(unique_teams_set)
    return teams_cheaters_dict, total_nr_teams


def counters_team_with_cheaters(teams_cheaters_dict, total_nr_teams):
    ''' Computes the amount of teams which have 0, 1, 2, 3, or 4 cheaters.
    
    Takes as argument a dictionary where the keys are unique team ids, and
    where the values are the number of cheaters in that team. Also takes as
    argument an integer, which is the total number of unique team ids.
    
    Returns five integers, which are the number of teams with 0, 1, 2, 3,
    or 4 cheaters, respectively.
    '''

    one_cheater = 0
    two_cheaters = 0
    three_cheaters = 0
    four_cheaters = 0


    for value in teams_cheaters_dict.values():
        if value == 1:
            one_cheater += 1
        elif value == 2:
            two_cheaters += 1
        elif value == 3:
            three_cheaters += 1    
        elif value == 4:
            four_cheaters += 1    
    
    zero_cheaters = total_nr_teams - (one_cheater + two_cheaters + three_cheaters + four_cheaters)
   
    return zero_cheaters, one_cheater, two_cheaters, three_cheaters, four_cheaters


def get_cheater_counters(cheaters, teams):
    ''' Executes the defined functions necessary to obtain the number of teams
    with 0, 1, 2, 3, or 4 cheaters.
    
    Takes as arguments a dictionary with details on cheating player account ids,
    and a list with details on team ids, player ids, and team numbers.
    
    Returns five integers, which are the number of teams with 0, 1, 2, 3,
    or 4 cheaters.
    '''
    
    # Here, I simply call the necessary functions in the appropriate order.
    # Firstly, obtain the set of cheating player ids. Secondly, I count how
    # many cheaters each team has, as well as how many teams exist in total.
    # Finally, I count how many teams have 0, 1, 2, 3, or 4 cheaters.
    
    cheaters_set = set_from_dict(cheaters)
    
    teams_cheaters_dict, total_nr_teams = cheaters_per_team(teams, cheaters_set)
    
    zero_cheaters, one_cheater, two_cheaters, three_cheaters, four_cheaters =     counters_team_with_cheaters(teams_cheaters_dict, total_nr_teams)
    
    return zero_cheaters, one_cheater, two_cheaters, three_cheaters, four_cheaters

