#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 15:00:17 2021

@author: Francesco Sannicola
"""

import csv
from collections import Counter
import math
import numpy as np
from array import array
from collections import defaultdict

#  import pandas as pd
#data = pd.read_csv("./Bank/Latino/la_llct-ud-test.conllu", nrows=1)

w_t = []
w_t.append(('INIT', 'INIT'))

with open("./Bank/Latin/la_llct-ud-dev.conllu") as fd:
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    for row in rd:
        if ((len(row))> 3):
            w_t.append((row[1], row[3]))
        if (len(row) == 0):
            w_t.append(('END', 'END'))
            w_t.append(('INIT', 'INIT'))
    w_t.pop()
            
            
            
w_t_occ=Counter(w_t)
t_occ=Counter([i[1] for i in w_t])

p_emission = dict()
p_transition = dict()


#compute emission probability
#prob w given t
for key, value in w_t_occ.items():
    if key[1] in p_emission:
        p_emission[key[1]].append([key[0], value/t_occ.get(key[1])])
    else:
        p_emission[key[1]] = [[key[0], value/t_occ.get(key[1])]]
    
#compute transition probability
#prob t1 given t
for t1 in t_occ.keys():
    for t in t_occ.keys():
        count = 0
        for i in range(1, len(w_t)):
            if w_t[i][1] == t1:
                if w_t[i-1][1] == t:
                    count += 1
        if t in p_transition:
            p_transition[t].append([t1, count/t_occ.get(t)])
        else:
            p_transition[t] = [[t1, count/t_occ.get(t)]]
            
            
y='quinta'
Pi=None


array_p_transition = np.array(list(p_transition.items()))
array_p_emission = np.array(list(p_emission.items()))



