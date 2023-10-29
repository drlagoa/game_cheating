#!/usr/bin/env python
# coding: utf-8

# In[2]:


'''
This module provides functions for analysing how cheaters interact
with one another, namely in terms of whether they kill each other
or they observe one another killing other players.

This allows us to compute how many players started cheating only
after having been killed by a cheater or having observed a cheater
kill 3 players.
'''

from datetime import datetime
from collections import defaultdict


def match_starting_time(kills):
    '''Stores the starting time of a given match in a dictionary.
    
    Takes as argument a list of kills, with details on match id,
    account id of killing player, account id of killed player, and
    time of  death.
    
    Returns a dictionary pairing match ids and the time of the
    earliest kill in that match (a proxy for its start).
    '''
    
    current_time = datetime.now()

    # I create a dictionary for match id's (keys) and their respective starting dates (values).
    # I will compare each kill, and see if they are the earliest ocurring in that match.
    matches_start = defaultdict(lambda: current_time)

    for [match_id, killer_id, killed_id, death_time] in kills:

        if matches_start[match_id] > death_time:
            matches_start[match_id] = death_time    
    
    return matches_start


def counter_victim_cheaters(kills, matches_start, cheaters):
    '''Computes the number of players which started cheating after being
    killed by an actively cheating player.
    
    Takes as argument a list (kills) with details on recorded kills, a
    dictionary (matches_start) with the starting time for each match id,
    and a dictionary with the starting date of cheating for each player id.
    
    Returns an integer, the number of players which started cheating
    after being killed by an actively cheating player.
    '''

    victim_cheaters = set()

    # I go through each kill, and check whether it happened at a time
    # when the killed player was not yet cheating, and when the killer
    # player was already cheating.
    
    # I use a try-except specification particularly for Key Errors
    # because many players are not cheaters and therefore are not
    # in the dictionary 'cheaters'. This is more efficient than
    # checking if the player is in the dictionary each time.
    
    for [match_id, killer_id, killed_id, death_time] in kills:    

        try:
            if matches_start[match_id] < cheaters[killed_id][0] and matches_start[match_id] > cheaters[killer_id][0]:
                victim_cheaters.add(killed_id)
        except KeyError:
            pass
        
    return len(victim_cheaters)


def pre_cheating_matches(kills, cheaters, matches_start):
    '''Stores the matches played by cheating players before they started
    cheating, and their time of death in each of these matches.
    
    Takes as argument a list of kills (with details on match id, account
    id of killing player, account id of killed player, and time of death)
    and two dictionaries, one (cheaters) pairing account ids with a list
    (of the date when the player started cheating, and the date when he
    was banned), and another (matches_start) pairing match ids and the
    time of the earliest kill in that match, a proxy for its start.
    
    Returns a dictionary pairing each player account id with a
    dictionary, where keys are match ids and values are the
    player's time of death in that match.
    '''
    
    pre_cheating_matches = defaultdict(dict)

    for [match_id, killer_id, killed_id, death_time] in kills:
        
        # For efficiency, I use the try-except specification instead of
        # checking in the killed_id is included in the cheaters dictionary.
        
        try:
            # Checking if the match started before the killed player started
            # cheating.
            if matches_start[match_id] < cheaters[killed_id][0]:
            # Append entry, registering the match and death_time in the
            # dictionary corresponding to the killed player.
                pre_cheating_matches[killed_id][match_id] = death_time
        
        # When killed_id is not a cheater, and therefore a KeyError appears.
        except KeyError:
            pass

    return pre_cheating_matches


# Technically, the processes performed by pre_cheating_matches (above)
# and kills_per_cheater (below) could be brought under one common function
# iterating only once through 'kills' but I decided to separate them
# for modularity.

def match_kills_per_cheater(kills, cheaters, matches_start):
    '''Stores the matches played by cheating players after they started
    cheating, and the timestamps of all the kills they got in each match.
    
    Takes as argument a list of kills (with details on match id, account
    id of killing player, account id of killed player, and time of death),
    and two dictionaries, one (cheaters) pairing account ids with a list
    (of the date when the player started cheating, and the date when he
    was banned), and another (matches_start) pairing match ids with the
    time of the earliest kill in that match (a proxy for its start).
    
    Returns a dictionary pairing each match id with a dictionary, where
    keys are cheating player account ids and values are lists of all
    the timestamps of that player's kills (in that match).
    '''
    
    match_kills_per_cheater = defaultdict(lambda: defaultdict(list))

    for [match_id, killer_id, killed_id, death_time] in kills:
        
        try:
            if cheaters[killer_id][0] > matches_start[match_id]:
                match_kills_per_cheater[match_id][killer_id].append(death_time)
            
        except KeyError:
            pass

    return match_kills_per_cheater


def match_earliest_3rd_kill(match_kills_per_cheater):
    '''Stores the time at which an actively cheating player first got
    3 kills for each match.
    
    Takes a dictionary where keys are match ids, and values are themselves
    dictionaries (for which keys are cheating player account ids, and
    values are a list of timestamps of their kills).
    
    Returns a dictionary where keys are match ids, and values are the
    time of the first third kill by a single cheating player.
    '''

    match_earliest_3rd_kill = {}
    
    # For each match, I check for each cheating player if they had
    # three kills, and if their third kill occurred earlier than
    # the third kill obtained by other cheating players in that game.

    for match_id, match_details in match_kills_per_cheater.items():
        
        early_3rd_kill = ""
        
        for account_id, kills in match_details.items():
            
            if len(kills) > 2:
                if early_3rd_kill == "" or kills[2] < early_3rd_kill:
                    early_3rd_kill = kills[2]
        
        # After going through each player, I register the earliest
        # third kill from any cheating player in that match, if
        # there was a third kill.
        if not early_3rd_kill == "":
            match_earliest_3rd_kill[match_id] = early_3rd_kill

    return match_earliest_3rd_kill


def counter_observer_cheaters(pre_cheating_matches, match_earliest_3rd_kill):
    '''Computes the number of players which started cheating after playing a
    match in which an actively cheating player had at least 3 kills.
    
    Takes as argument two dictionaries. First dictionary pairs each player
    account id with a dictionary, where keys are match ids and values the
    player's time of death in that match. The second dictionary pairs match
    ids with timestamps for the earliest third kill by a cheating player
    in that match. Returns an integer, the number of players which started
    cheating after observing a cheating player obtain at least 3 kills.
    '''

    observer_cheaters = set()

    # I go through each match played by each cheating players before they
    # started cheating, and check whether they included a cheating player
    # killing 3 players before the time of death of the not yet actively
    # cheating player.
    for player, match_history in pre_cheating_matches.items():
        for match, death_time in match_history.items():
            
            try:
                if death_time > match_earliest_3rd_kill[match]:
                    observer_cheaters.add(player)
            
            except KeyError:
                pass
        
    return len(observer_cheaters)


def get_observer_cheaters(cheaters, kills):
    ''' Executes the defined functions necessary to obtain the number of cheaters
    which started cheating after playing a match where an actively cheating player
    obtained 3 kills before the death of the not yet cheating player.
    
    Takes as arguments a dictionary (cheaters) pairing cheating player ids with a
    list (with the date they started cheating and the date when they were banned),
    and a list with details on match id, killing player id, killed player id,
    and time of death for each kill.
    
    Returns an integer, the number of players which started cheating after
    observing a cheating player get at least 3 kills in a match.
    '''
    
    # Here, I simply call the necessary functions in the appropriate order.

    # Firstly, I store the starting time of each match.
    matches_start_dict = match_starting_time(kills)
    
    # Secondly, I store the matches played by not yet cheating players and their death time.     
    pre_cheating_matches_dict = pre_cheating_matches(kills, cheaters, matches_start_dict)
    
    # Then, I store the kills obtained by each cheating player in each match.
    match_kills_per_cheater_dict = match_kills_per_cheater(kills, cheaters, matches_start_dict)
    
    # Then, I register the time at which the earliest third kill by a cheating player ocurred
    # in each game.
    match_earliest_3rd_kill_dict = match_earliest_3rd_kill(match_kills_per_cheater_dict)
    
    # Finally, I count how many players actually started cheating after playing a match
    # in which they died after a cheating player obtained at least 3 kills.
    nr_observer_cheaters =     counter_observer_cheaters(pre_cheating_matches_dict, match_earliest_3rd_kill_dict)
    
    return nr_observer_cheaters

