#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''
This module provides functions for randomizing the roles
performed by players (killing or being killed by someone)
in a match.
'''

from collections import defaultdict
import random


def players_per_match(kills):
    ''' Creates a dictionary with a set of participating players for
    each match.
    
    Takes as argument a list, where elements are match id, account id
    of killing player, account id of killed player, and time of death.
    
    Returns a dictionary in which keys are match ids, and values are
    sets of the different players participating in the match.
    '''

    match_players = defaultdict(set)

    for [match_id, killer_id, killed_id, death_time] in kills:
    
        match_players[match_id].add(killer_id)
        match_players[match_id].add(killed_id)

    return match_players


def players_shuffle(match_players):
    ''' Randomly shuffles an ordered list of players in each match,
    associating the newly shuffled list of players with the original
    list of players.
    
    Takes as argument a dictionary in which keys are match ids, and
    values are sets of player ids.
    
    Returns a dictionary in which keys are match ids, and values are
    dictionaries (for which the keys are player ids, and values are
    the associated player ids after shuffling).
    '''

    for key, value in match_players.items():
        
        # Firstly, I create the lists of original and shuffled ids.
        original_ids = list(value)
        shuffled_ids = original_ids[:]
        random.shuffle(shuffled_ids)
        
        # I set the value (for each key/match) to an empty dictionary, of type string.
        match_players[key] = defaultdict()
    
        # Finally, I fill each new dictionary with a pair of original list player id and shuffled list id. 
        for index in range(len(original_ids)):
            match_players[key].update({original_ids[index]:shuffled_ids[index]})

    return match_players


def kills_updating(match_players, kills):
    ''' Updates list of kills, replacing original acocunt ids by the
    associated account ids post-shuffle.
    
    Takes as argument a dictionary (match_players), in which keys are
    match ids and values are dictionaries associating player ids before
    and after shuffling, and a list an original list of kills.
    
    Returns a new list of kills, where each element is a list with a match id,
    account id of killing player, account id of killed player, and time of death.
    '''
            
     # Now, for each match there are two lists of players with equivalent
    # elements but different orders. The 'substitutes' for each original
    # player id will be the associated player id for each original player id.
    
    for value in kills:

        match_id = value[0]
        killer_id = value[1]
        killed_id = value[2]

        # I update each player id (both for killer and killed) by their associated
        # post-shuffle account id.
        value[1] = match_players[match_id][killer_id]
        value[2] = match_players[match_id][killed_id]

    return kills


def get_shuffled_kills(kills):
    ''' Executes the defined functions necessary to obtain a list of kills
    after randomization of player roles within matches.
    
    Takes as argument an original list of kills, where elements are lists
    with match id, killing player account id, killed player account id,
    and time of death.
    
    Returns a new list of kills, with randomized player role allocations.
    '''
    
    match_players = players_per_match(kills)
    match_players = players_shuffle(match_players)
    kills = kills_updating(match_players, kills)
    
    return kills

