#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
This module provides the necessary functions for translating
data from original .txt files into python objects, namely dictionaries
and lists.
'''

from datetime import datetime


def get_cheaters():
    '''Opens file cheaters.txt and returns a dictionary of cheating players.
    Each key is the account id of a cheating player. The value for each key
    is a list with two elements. The two elements are the date when they
    started cheating, and the date when they were banned for cheating.
    
    Takes a text file as argument, and returns a dictionary as the output.
    '''
    
    data = {}
    for line in open('assignment-final-data\cheaters.txt', 'r'):
        entry = line.strip().split('\t')
        data[entry[0]] = [datetime.strptime(entry[1], '%Y-%m-%d'), datetime.strptime(entry[2], '%Y-%m-%d')]
    return data 


def get_teams():
    '''Opens file teams.txt and returns a list of team id's for players
    in different matches. Each entry of the list consists of a list
    with the match id, the player account id, and the team number.
    
    Takes a text file as argument, and returns a list as the output.
    '''
    
    data = []
    for line in open(r'assignment-final-data\team_ids.txt', 'r'):
        data.append(line.strip().split('\t'))
    return data 


def get_kills():
    '''Opens file kills.txt and returns a list of kills, which are identified
    as lists of the match id, the account id of the killer, the account id
    of the killed player, and the time at which the kill took place.
    
    Takes a text file as argument, and returns the list as the output.
    '''
    
    data = []
    for line in open('assignment-final-data\kills.txt', 'r'):
        entry = line.strip().split('\t')
        data.append([entry[0], entry[1], entry[2], datetime.strptime(entry[3], '%Y-%m-%d %H:%M:%S.%f')])
    return data 

