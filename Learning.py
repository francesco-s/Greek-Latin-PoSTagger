import csv
from collections import Counter, defaultdict
import numpy as np
import nltk.tokenize
import json

import pandas as pd
from nltk import pos_tag, PerceptronTagger, pos_tag_sents
from nltk import word_tokenize

w_t = []
w_s = []
w_t.append(('INIT', 'INIT'))

with open("C:\\Users\\39392\\Desktop\\PycharmProgetti\\PosTagger\\Latin\\la_llct-ud-dev.conllu") as fd:
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

# compute emission probability for initial state
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

with open("EmissionProbability.txt", "w") as outfile:
    json.dump({
        "emission probability": p_emission,

    }, outfile, indent=1, ensure_ascii=False)

with open("Transition.txt", "w") as outfiles:
    json.dump({
        "tag_occurance": t_occ,
        "transition probability": p_transition,
        "word_tag pair": w_t,
    }, outfiles, indent=3, ensure_ascii=False)

# VITERBI

query = '+ In Dei omnipotentis nomine, regnante domno nostro Karolus divina faventem clementia imperatore augusto, ' \
        'anno imperii eius septimo, pridie idus augusti indictione quinta. '

input_splitted = nltk.word_tokenize(query)  # y.split()
T = len(input_splitted)


def dptable(V):
    yield " ".join(("%10d" % i) for i in range(len(V)))
    for y in V[0]:
        yield "%.7s: " % y + " ".join("%.7s" % ("%f" % v[y]) for v in V)


# Tracking tables from first observation
backtrace = [{}]
for i in states:
    try:
        backtrace[0][i] = p_transition_dict['INIT'][i] * p_emission[i][input_splitted[0]]
    except KeyError:
        backtrace[0][i] = p_transition_dict['INIT'][i] * 0.001
        # print ('keyerror')

for t in range(1, T):
    backtrace.append({})
    for y in states:
        try:
            (prob, state) = max(
                (backtrace[t - 1][y0] * p_transition_dict[y0][y] * p_emission[y][input_splitted[t]], y0) for y0 in
                states)
        except KeyError:
            # P(unk|NOUN) =1 --> quando non conosco la parola la considero un nome
            '''if y == 'NOUN' :
                (prob, state) = max((backtrace[t-1][y0] * p_transition_dict[y0][y] * 1, y0) for y0 in states)
            else:
                (prob, state) = max((backtrace[t-1][y0] * p_transition_dict[y0][y] * 0.001, y0) for y0 in states)'''
            # P(unk|NOUN) =0.5 and P(unk|VERB) --> quando non conosco la parola la considero o un nome o un vrerbo
            '''if y == 'NOUN' :
                (prob, state) = max((backtrace[t-1][y0] * p_transition_dict[y0][y] * 0.5, y0) for y0 in states)
            elif y == 'VERB':
                (prob, state) = max((backtrace[t-1][y0] * p_transition_dict[y0][y] * 0.5, y0) for y0 in states)
            else:
                (prob, state) = max((backtrace[t-1][y0] * p_transition_dict[y0][y] * 0.001, y0) for y0 in states)'''
            # P(unk|ti) = 1/#(PoS_TAGs)
            (prob, state) = max(
                (backtrace[t - 1][y0] * p_transition_dict[y0][y] * (1 / len(states)), y0) for y0 in states)

        backtrace[t][y] = prob
    # for i in dptable(viterbi):
    #   print (i)
    opt = []
    for j in backtrace:
        for x, y in j.items():
            if j[x] == max(j.values()):
                opt.append(x)

    p = max(backtrace[-1].values())
print('The PoS are : \n' + ''
      .join(map(''.join, zip([x + '/' for x in input_splitted], [x + '\n' for x in opt])))
      + '\nWith probability of:  %s' % p)


# Baseline evaluation
file = open("C:\\Users\\39392\\Desktop\\PycharmProgetti\\PosTagger\\Latin\\la_llct-ud-test.conllu")
for row in file:
    if len(row) > 3:
        if i == 0:
            w_s.append((row[1], 'INIT'))
            i = 1
            w_t.append((row[1], row[3]))
            if len(row) == 0:
                w_t.append(('INIT', 'INIT'))
                i = 0
w_t.pop()

sentence_tokens = '+ In Dei omnipotentis nomine, regnante domno nostro Karolus divina faventem clementia ' \
                      'imperatore augusto, anno imperii eius septimo, pridie idus augusti indictione quinta '

print("Pos Tag of sentence: ",pos_tag(word_tokenize(sentence_tokens)))

tagger = PerceptronTagger()
for item in sentence_tokens.split():
    for sentence in word_tokenize(item):
            tags = tagger.tag(word_tokenize(sentence))
            tags = tagger.tag(sentence_tokens.split())

print("Most Frequent Tag of sentence is: ",Counter(i[1] for i in tags).most_common(1))







                
