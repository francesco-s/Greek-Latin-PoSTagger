#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 15:00:17 2021

@author: Francesco Sannicola
"""

import csv
from collections import Counter
import numpy as np
import math
import nltk
import cltk


from nltk import word_tokenize
from nltk.tokenize import MWETokenizer

#w_t tutte le parole con proprio tag (+1 per INIT)
w_t = []
# w_s tutte le parole iniziali
w_s= []
w_t.append(('INIT', 'INIT'))


greek_train_tree_bank = "./Bank/Greek/grc_perseus-ud-train.conllu"
latin_train_tree_bank = "./Bank/Latin/la_llct-ud-train.conllu"

with open(latin_train_tree_bank) as fd:
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    i = -1
    for row in rd:
        if len(row) > 3:
            if i == 0:
                w_s.append((row[1].lower(), 'INIT'))
                i = 1
            w_t.append((row[1].lower(), row[3].lower()))
        if len(row) == 0:
            w_t.append(('INIT', 'INIT'))
            i = 0
    w_t.pop()

w_t_occ = Counter(w_t)
w_s_occ = Counter(w_s)

t_occ = Counter([i[1] for i in w_t])

p_emission = dict()
p_emission_init = dict()

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
    if t1 != 'INIT':
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
                p_transition[t] = [[t1, prob]]
            if t in p_transition:
                p_transition[t].append(prob)
            else:
                p_transition[t] = [prob]    
            '''
            if t in p_transition_dict:
                p_transition_dict[t].update({t1: prob})
            else:
                p_transition_dict[t] = {t1: prob}
            

i = 0
states = np.empty(len(p_transition_dict), dtype=object)
for key in p_transition_dict.keys():
    states[i] = str(key)
    i += 1

# VITERBI

query_list = []
first_char_init = 9

w_t_test = []

greek_test_tree_bank = "./Bank/Greek/grc_perseus-ud-test.conllu"
latin_test_tree_bank = "./Bank/Latin/la_llct-ud-test.conllu"

with open(latin_test_tree_bank) as fd:
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    i = -1
    for row in rd:
        if len(row) == 1:
            if row[0].startswith('# text'):
               #if (row[0][len(row[0])-1] == '·'):
                #    query_list.append(row[0][first_char_init:(len(row[0])-1)].lower() + ' ·')
                    #print(len(query_list))
                #else:
                if '...' not in row[0]:
                    query_list.append(row[0][first_char_init:(len(row[0]))].lower().replace('.', ' .').replace('·', ' ·'))
                else:
                    query_list.append(row[0][first_char_init:(len(row[0]))].lower().replace('·', ' ·'))

        elif len(row) > 3:
            w_t_test.append((row[1].lower(), row[3].lower()))
        


        
def dptable(V):
    yield " ".join(("%10d" % i) for i in range(len(V)))
    for y in V[0]:
        yield "%.7s: " % y+" ".join("%.7s" % ("%f" % v[y]) for v in V)

#query = '+ In Dei omnipotentis nomine, regnante domno nostro Karolus divina faventem clementia imperatore augusto, anno imperii eius septimo, pridie idus augusti indictione quinta.'

all_pos = [[]]
all_pos.pop()

token_exclude = [
                 ('[', 'adj', ']'),
                 ('[', 'adv', ']'),
                 ('[', 'aux', ']'),
                 ('[', 'cconj', ']'),
                 ('[', 'det', ']'),
                 ('[', 'init', ']'),
                 ('[', 'noun', ']'),
                 ('[', 'num', ']'),
                 ('[', 'part', ']'),
                 ('[', 'pron', ']'),
                 ('[', 'propn', ']'),
                 ('[', 'punct', ']'),
                 ('[', 'sconj', ']'),
                 ('[', 'verb', ']'),
                 ('[', 'x', ']'),
                 ('[', 'Adj', ']'),
                 ('[', 'Adv', ']'),
                 ('[', 'Aux', ']'),
                 ('[', 'Cconj', ']'),
                 ('[', 'Det', ']'),
                 ('[', 'Init', ']'),
                 ('[', 'Noun', ']'),
                 ('[', 'Num', ']'),
                 ('[', 'Part', ']'),
                 ('[', 'Pron', ']'),
                 ('[', 'Propn', ']'),
                 ('[', 'Punct', ']'),
                 ('[', 'Sconj', ']'),
                 ('[', 'Verb', ']'),
                 ('[', 'X', ']'),
                 ('[', '--', ']'),
                 ('[', 'participle', ']')
                 ]

states = np.delete(states, 0)

tokenizer = MWETokenizer(token_exclude)

all_words = []

for value in p_emission.values():
    all_words.extend(list(value.keys()))

'''for query in query_list:
    input_splitted = tokenizer.tokenize(word_tokenize(query))
    T = len(input_splitted)
    tag_target = 'noun'
    for t in range(0, T):
        max = 0
        for key, value in w_t_occ.items():
            if key[0]==input_splitted[t]:
                if max < value:
                    max = value
                    tag_target = key[1]
        all_pos.append([input_splitted[t], tag_target])'''

for query in query_list:
        
    input_splitted = tokenizer.tokenize(word_tokenize(query))
    T = len(input_splitted)
    
    # Tracking tables from first observation
    backtrace=[{}]
    for i in states:
        try:
            backtrace[0][i]=p_transition_dict['INIT'][i]*p_emission_init['INIT'][input_splitted[0]]
        except KeyError:
            backtrace[0][i]=p_transition_dict['INIT'][i]*0.0000011    
    
    
    for t in range(1, T):
        input_splitted[t] = input_splitted[t].replace('_', '')
        backtrace.append({})
        for y in states:
            try:
                if input_splitted[t] not in all_words:
                     # P(unk|NOUN) =0.5 and P(unk|VERB)
                    '''if y == 'noun':
                         (prob, state) = max((backtrace[t-1][y0] * p_transition_dict[y0][y] * 0.5, y0) for y0 in states)
                    elif y == 'verb':
                         (prob, state) = max((backtrace[t-1][y0] * p_transition_dict[y0][y] * 0.5, y0) for y0 in states)
                    else:
                        (prob, state) = max((backtrace[t-1][y0] * p_transition_dict[y0][y] * 0, y0) for y0 in states)'''
                     #P(unk|ti) = 1/#(PoS_TAGs)
                    (prob, state) = max((backtrace[t-1][y0] * p_transition_dict[y0][y] * (1 / len(states)), y0) for y0 in states)
                else: 
                    (prob, state) = max((backtrace[t-1][y0] * p_transition_dict[y0][y] * p_emission[y][input_splitted[t]], y0) for y0 in states)
                #(prob, state) = max((backtrace[t-1][y0], y0) for y0 in states)
                #prova = prob * p_transition_dict[state][y] * p_emission[y][input_splitted[t]]
            except KeyError:
                # P(unk|NOUN) =1 --> quando non conosco la parola la considero un nome
                '''if y == 'noun' :
                    (prob, state) = max((backtrace[t-1][y0] * p_transition_dict[y0][y] * 1, y0) for y0 in states)
                    #(prob, state) = max((backtrace[t-1][y0], y0) for y0 in states)
                    #prova = prob * p_transition_dict[state][y] * 1
                else:
                    (prob, state) = max((backtrace[t-1][y0] * p_transition_dict[y0][y] * 0.0000001, y0) for y0 in states)
                # P(unk|NOUN) =0.5 and P(unk|VERB) --> quando non conosco la parola la considero o un nome o un verbo
                if y == 'noun' :
                    (prob, state) = max((backtrace[t-1][y0] * p_transition_dict[y0][y] * 0.5, y0) for y0 in states)
                elif y == 'verb':
                    (prob, state) = max((backtrace[t-1][y0] * p_transition_dict[y0][y] * 0.5, y0) for y0 in states)
                else:
                    (prob, state) = max((backtrace[t-1][y0] * p_transition_dict[y0][y] * 0.0000001, y0) for y0 in states)
                #P(unk|ti) = 1/#(PoS_TAGs)
                #(prob, state) = max((backtrace[t-1][y0] * p_transition_dict[y0][y] * (1 / len(states)), y0) for y0 in states)'''
                (prob, state) = max((backtrace[t-1][y0] * p_transition_dict[y0][y] * 0.00000011, y0) for y0 in states)
            backtrace[t][y] = prob
        #for i in dptable(viterbi):
        #   print (i)
        opt=[]
        for j in backtrace:
            for x,y in j.items():
                if j[x]==max(j.values()):
                    opt.append(x)
        
    p=max(backtrace[-1].values())
    # print ('The PoS are\n'+''
    #       .join(map(''.join, zip([x + '/' for x in input_splitted], [x + '\n' for x in opt])))
    #       +'\nWith probability of %s'%p)
    for l in range(0,T):
        all_pos.append([input_splitted[l], opt[l]])

right_pos = 0
wrong_pos = 0
n = 0
k=0

for i in range(0, len(all_pos)):
    if all_pos[i][0] == w_t_test[i][0]:
        k+=1
    else:
        print(i)
    i+=1

for word in all_pos:
    if (word[1] == w_t_test[n][1]):
        right_pos +=1
    else :
        wrong_pos +=1
    n += 1
accuracy = right_pos/(right_pos+wrong_pos)
print(accuracy)

        

