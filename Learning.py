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
w_t_occ=Counter(w_t)
t_occ=Counter([i[1] for i in w_t])

p_emission = []
p_transition = []

#compute emission probability
def EmissionProb(p_emission,w_t_occ ):
for key, value in w_t_occ.items():
    wt_c =t_occ.get(key[1])
    p_emission.append((key[0], key[1], math.log(value/wt_c)))
    
    p_emission=dict()
    EmissionProb(w_t_occ=w_t_occc, p_emission=p_emission)


#compute transition probability
def TransitionProb(p_transition,t_occ)
for t in t_occ.keys():
    if t != '---':
        for t1 in t_occ.keys():
            if t1 != t and t1 != '---':
                count = 0
                for i in range(1, len(w_t)):
                    if w_t[i][1] == t:
                        if w_t[i-1][1] == t1:
                            count += 1
                p_transition.append((t, t1, count/t_occ.get(t1)))
                
                p_transition=dict()
                TransitionProb(p_transition=p_transition, t_occ=t_occ)
                
                
def main():
    
    allTag=[]
    tagID=1
    tagDict=dict()
    
with open("./Bank/Latin/la_llct-ud-test.conllu") as fd:
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    
    for row in rd:
         if ((len(row))> 3):
            w_t.append((row[1], row[3]))
        if (len(row) == 0):
            w_t.append(('---', '---'))
            
       split = row.strip("\n").split(" ")
            
      for w_t in split:
        
         currentTag = w_t[]
         currentWord =  w_t[]
        
        if(w_t not in w_t_occ):
            w_t_occ[w_t]=1
            
          else:
            w_t_occ[w_t]++
            
             if(currentTag not in tagDict):
                    tagDict[currentTag] = tagID
                    tagID++
                    allTag.append(currentTag)
                    
            if (currentTag not in t_occ):
                
                    t_occ[currentTag]=1
            else:
                    t_occ[currentTag]++

            if(currentWord not in w_t):
                    w_t[currentWord] = [currentTag]
            
            else:
                    currentTagset = w_t[currentWord]
              if (currentTag not in currenTagset):
                        currentTagset.append(currentTag)

                            
                            
                    
                
