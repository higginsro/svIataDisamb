# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 15:09:03 2018

@author: rhiggins
"""
import pandas as pd
from Data import preProcessDfData


# from os import path
# import json
# import io
# targetP = path.join("C:\\","users","rhiggins","projects","DF-git","swedish_dev")
# with io.open(path.join(targetP,"intents.json"), mode="r", encoding='utf-8') as f:
#     intents = json.load(f)

# sentences in 'userSays'
# for each usersays, want each token and 'alias' if any.
# utterances = [utt for intent in intents.values() for utt in intent['userSays']]

# def token_and_entity(utterance_list):
#    # expects a list of dictionaries
#    for item in utterance_list:
#        try:
#            print(item['text'],item['meta'])
#        except KeyError as e:
#            print(item['text'],"___")


def pte(utterance_list):
    ss = ''.join([item['text'] for item in utterance_list])
    return ss


# with open('DF_training_utt_raw_sentences.txt','w',encoding='utf-8')as g:
#     for uttl in utterances:
#         g.write(pte(uttl['data'])+'.\n')


# utterances[412]
# # creates tags for each token. UNK for not airport, and @airport for airport.
# raw_sentences = []
# for utt in utterances:
#     sentence = [('<start>','B')]
#     for chunk in utt['data']:
#         if 'alias' in chunk:
#             token, tag = chunk['text'],chunk['meta']
#             sentence.append((token,tag))
#         else:
#             sentence.extend([(item,"UNK")for item in (chunk['text'].split())])
#     sentence.append(('<end>','B'))
#     raw_sentences.append(sentence)
raw_sentences = preProcessDfData.load_DF_data()


def data_augmentation(raw_sentences):
    ''' augment data with previous Token and next token for each token
    '''
    token_unigram_contexts = []
    for rs in raw_sentences:
        for n, pair in enumerate(rs):
            prevTok = ' '
            prevLen = 0
            nextTok = ' '
            nextLen = 0
            tokenLen = 0
            if n != 0:
                prevTok = rs[n - 1][0]
                prevLen = len(rs[n - 1][0])
                tokenLen = len(pair[0])
            elif n < len(rs) - 1:
                nextTok = rs[n + 1][0]
                nextLen = len(rs[n - 1][0])
                tokenLen = len(pair[0])
            #        token_unigram_contexts.append([*pair, prevTok, nextTok])
            token_unigram_contexts.append([*pair, prevTok, nextTok, prevLen, tokenLen, nextLen])
    return token_unigram_contexts


token_unigram_contexts = data_augmentation(raw_sentences=raw_sentences)
totData = pd.DataFrame(token_unigram_contexts)
# totData.columns = ["token","tag", "prevToken","nextToken"]
totData.columns = ["token", "tag", "prevToken", "nextToken", "prevLen", "tokenLen", "nextLen"]

# totData[totData.tag=="@airport"]
# numberOfLocations = totData[totData.tag=="@airport"].shape[0]
# locationtokens = totData[totData.tag=="@airport"]
# till_loc_collocations = locationtokens.prevToken.value_counts()['till']
# loc_till_collocations = locationtokens.nextToken.value_counts()['till']
# fran_loc_collocations = locationtokens.prevToken.value_counts()['från']
# loc_fran_collocations = locationtokens.nextToken.value_counts()['från']
#
# till_total_freq = totData.token.value_counts()['till']
# fran_total_frq = totData.token.value_counts()['från']
import numpy as np


# how important is till?
# normalised pointwise mutual information
def pmi(fx, fy, fxy, nx):
    py_bar_x = fxy / fx
    py = fy / nx
    return np.log2(py_bar_x / py)


def hx(px):
    return -np.log2(px)


def g(x):
    # g:[-1,1]->[0,1]
    return (x + 1) / 2


sum(totData.tag == "@airport") / totData.shape[0]
# prev_token_dist = totData.prevToken.value_counts()
# next_token_dist = totData.nextToken.value_counts()

XX = pd.DataFrame([totData.prevToken == "till",
                   totData.prevToken == "från",
                   totData.nextToken == "till",
                   totData.nextToken == "från",
                   totData.prevLen == 3,
                   totData.tokenLen == 3,
                   totData.nextToken == 3
                   ])
XX = XX.T
yy = totData.tag == "@airport"

# --------------------------------------------
from sklearn import naive_bayes, linear_model
from sklearn.metrics import classification_report, confusion_matrix

clf = naive_bayes.BernoulliNB()
clf2 = linear_model.LogisticRegression()
clf.fit(XX, yy)
clf2.fit(XX, yy)
print(classification_report(yy, clf.predict(XX)))
print(classification_report(yy, clf2.predict(XX)))

XX.shape[0]

# -----------------------------------
# swedish NER data
swtrain = []
with io.open('train_corpus.txt', mode='r', encoding='utf-8') as f:
    sents = f.read()
sents = sents.split('\n\n')
swtr_token_tag_pairs = [[tuple(pair.split('\t')) for pair in sent.split('\n')] for sent in sents]
swtr_token_tag_pairs = [[('<start>', 'B')] + s + [('<end>', 'B')] for s in swtr_token_tag_pairs]
# for s in swtr_token_tag_pairs:
#     r = [('<start>','B')]+s
#     s = s+[('<end>','B')]

swtr_token_tag_pairs[:30]

sw_aug_data = data_augmentation(swtr_token_tag_pairs)
SwedData = pd.DataFrame(sw_aug_data)
SwedData.columns = ["token", "tag", "prevToken", "nextToken", "prevLen", "tokenLen", "nextLen"]


def make_binary_features(tokenDF):
    binDF = pd.DataFrame([tokenDF.prevToken == "till",
                          tokenDF.prevToken == "från",
                          tokenDF.nextToken == "till",
                          tokenDF.nextToken == "från",
                          tokenDF.prevLen == 3,
                          tokenDF.tokenLen == 3,
                          tokenDF.nextToken == 3
                          ])
    return binDF


SwXX = make_binary_features(SwedData)
SwXX = SwXX.T
Swyy = SwedData.tag == "LOC"
sum(Swyy) / len(Swyy)
print(classification_report(Swyy, clf.predict(SwXX)))

print(confusion_matrix(Swyy, clf.predict(SwXX)))

tvals = pd.DataFrame([list(Swyy), list(clf.predict(SwXX))], dtype=bool)
tvals = tvals.T
fps = (tvals.Truth == False) & (tvals.Prediction == True)
fns = (tvals.Truth == True) & (tvals.Prediction == False)
tvals.columns = ['Truth', 'Prediction']
dd = clf.predict(SwXX)
dd[:10]
Swyy[:10]

# --------------------------------------------
clf = naive_bayes.BernoulliNB()
clf2 = linear_model.LogisticRegression()
clf.fit(SwXX, Swyy)
clf2.fit(SwXX, Swyy)
print(classification_report(Swyy, clf.predict(SwXX)))
print(classification_report(yy, clf.predict(XX)))
