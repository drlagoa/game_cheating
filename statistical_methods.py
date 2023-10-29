#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
This module provides functions for the calculation of statistical
concepts necessary for our analysis, namely means and confidence
intervals.
'''

from numpy import std


def mean(lst):
    ''' Calculates the mean of a list of values.
    
    Takes as argument a list of integers. Returns the mean
    as a float value.
    '''
    
    mean = sum(lst) / len(lst)
    return mean


def confidence_interval(lst):
    ''' Calculates the approximation of the confidence interval of a
    value.
    
    Takes as argument a list composed of integers, which are estimations
    of a specific value. Returns a string value which indicates the lower
    and upper bounds of the confidence interval.
    ''' 
    
    avg = mean(lst)
    std_dev = std(lst)
    n = len(lst)
    
    lower_bound = avg - 1.96 * (std_dev / n ** 0.5)
    upper_bound = avg + 1.96 * (std_dev / n ** 0.5)
    
    return '[' + "{:.1f}".format(lower_bound) + ' : ' + "{:.1f}".format(upper_bound) + ']'

