#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 15:00:17 2021

@author: Francesco Sannicola
"""

import csv
from collections import Counter
import numpy as np


#  import pandas as pd
# data = pd.read_csv("./Bank/Latino/la_llct-ud-test.conllu", nrows=1)

w_t = []
w_s= []
w_t.append(('INIT', 'INIT'))

with open("./Bank/Latin/la_llct-ud-dev.conllu") as fd:
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    i = -1
    for row in rd:
        if len(row) > 3:
            if i == 0:
                w_s.append((row[1], 'INIT'))
                i = 1
            w_t.append((row[1], row[3]))
        if len(row) == 0:
            w_t.append(('INIT', 'INIT'))
            i = 0
    w_t.pop()

w_t_occ = Counter(w_t)
w_s_occ = Counter(w_s)

t_occ = Counter([i[1] for i in w_t])

p_emission = dict()
p_emission_init = dict()
p_transition = dict()

# compute emission probability
# prob w given t
for key, value in w_t_occ.items():
    prob = value / t_occ.get(key[1])
    '''if key[1] in p_emission:
        p_emission[key[1]].append([key[0], prob])
    else:
        p_emission[key[1]] = [[key[0], prob]]'''
    if key[1] in p_emission:
        p_emission[key[1]].update({key[0]: prob})
    else:
        p_emission[key[1]] = {key[0]: prob}

#compute emission probability for initial state
for key, value in w_s_occ.items():
    prob = value / t_occ.get(key[1])
    if key[1] in p_emission_init:
        p_emission_init[key[1]].update({key[0]: prob})
    else:
        p_emission_init[key[1]] = {key[0]: prob}
    
p_transition_dict = dict()
# compute transition probability
# prob t1 given t
for t1 in t_occ.keys():
    for t in t_occ.keys():
        count = 0
        for i in range(1, len(w_t)):
            if w_t[i][1] == t1:
                if w_t[i - 1][1] == t:
                    count += 1
        prob = count / t_occ.get(t)
        '''if t in p_transition:
            p_transition[t].append([t1, prob])
        else:
            p_transition[t] = [[t1, prob]]'''
        if t in p_transition_dict:
            p_transition_dict[t].update({t1: prob})
        else:
            p_transition_dict[t] = {t1: prob}
        if t in p_transition:
            p_transition[t].append(prob)
        else:
            p_transition[t] = [prob]

i = 0
array_p_transition = np.zeros((len(p_transition), len(p_transition)))
states = np.empty(len(p_transition), dtype=object)
for key, values in p_transition.items():
    states[i] = str(key)
    array_p_transition[i, :] = values
    i += 1

# VITERBI

y = '+ In Dei omnipotentis nomine, regnante domno nostro Karolus divina faventem clementia imperatore augusto, anno imperii eius septimo, pridie idus augusti indictione quinta.'

input_splitted = y.split()
T = len(input_splitted)

# Tracking tables from first observation
viterbi=[{}]
for i in states:
    try:
        viterbi[0][i]=p_transition_dict['INIT'][i]*p_emission[i][input_splitted[0]]
    except KeyError:
        viterbi[0][i]=p_transition_dict['INIT'][i]*0.001
        #print ('keyerror')
    
def dptable(V):
    yield " ".join(("%10d" % i) for i in range(len(V)))
    for y in V[0]:
        yield "%.7s: " % y+" ".join("%.7s" % ("%f" % v[y]) for v in V)

for t in range(1, T):
    viterbi.append({})
    for y in states:
        try:
            (prob, state) = max((viterbi[t-1][y0] * p_transition_dict[y0][y] * p_emission[y][input_splitted[t]], y0) for y0 in states)
        except KeyError:
            (prob, state) = max((viterbi[t-1][y0] * p_transition_dict[y0][y] * 0.001, y0) for y0 in states)
        viterbi[t][y] = prob
    #for i in dptable(viterbi):
        #print (i)
    opt=[]
    for j in viterbi:
        for x,y in j.items():
            if j[x]==max(j.values()):
                opt.append(x)
    
h=max(viterbi[-1].values())
print ('The steps of PoS are '+' '.join(opt)+' with probability of %s'%h)
