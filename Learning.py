#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 15:00:17 2021

@author: Francesco Sannicola
"""

import csv
from collections import Counter
import math

#  import pandas as pd
#data = pd.read_csv("./Bank/Latino/la_llct-ud-test.conllu", nrows=1)

w_t = []

with open("./Bank/Latino/la_llct-ud-test.conllu") as fd:
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    for row in rd:
        if ((len(row))> 3):
            w_t.append((row[1], row[3]))
        if (len(row) == 0):
            w_t.append(('---', '---'))
            
            
w_t_occ=Counter(w_t)
t_occ=Counter([i[1] for i in w_t])

p_emission = []
p_transition = []

#compute emission probability
for key, value in w_t_occ.items():
    wt_c =t_occ.get(key[1])
    p_emission.append((key[0], key[1], math.log(value/wt_c)))
    

    