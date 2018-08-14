# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 15:09:03 2018

@author: rhiggins
"""
import pandas as pd
from Data import preProcessDfData


raw_sentences = preProcessDfData.load_DF_data()
rse_labels = [zip(*rs) for rs in raw_sentences]
def data_augmentation(raw_sentences):
    ''' augment data with previous Token and next token for each token
    TODO turn this into a method that doesn't take a pair, just
    lists of tokens.
    '''
    token_unigram_contexts = []
    for rs in raw_sentences:
        for n,pair in enumerate(rs):

            prevTok = ' '
            prevLen = 0
            nextTok = ' '
            nextLen = 0
            tokenLen = 0
            if n != 0:
                prevTok = rs[n-1][0]
                prevLen = len(rs[n-1][0])
                tokenLen = len(pair[0])
            elif n<len(rs)-1:
                nextTok = rs[n+1][0]
                nextLen = len(rs[n+1][0])
                tokenLen = len(pair[0])
    #        token_unigram_contexts.append([*pair, prevTok, nextTok])
            token_unigram_contexts.append([pair[0], pair[1], prevTok, nextTok, prevLen, tokenLen, nextLen])
    return token_unigram_contexts

def make_binary_features(tokenDF):
    binDF= pd.DataFrame([tokenDF.prevToken==u"till",
                   tokenDF.prevToken==u"från",
                   tokenDF.nextToken==u"till",
                   tokenDF.nextToken==u"från",
                   tokenDF.prevLen==3,
                   tokenDF.tokenLen==3,
                   tokenDF.nextToken==3
                  ])
    return binDF.T

token_unigram_contexts = data_augmentation(raw_sentences=raw_sentences)
totData = pd.DataFrame(token_unigram_contexts)
totData.columns = ["token","tag", "prevToken","nextToken", "prevLen","tokenLen","nextLen"]
# TODO this classifier basically doesn't work.
# needs work
XX = pd.DataFrame([totData.prevToken==u"till",
                   totData.prevToken==u"från",
                   totData.nextToken==u"till",
                   totData.nextToken==u"från",
                   totData.prevLen==3,
                   totData.tokenLen==3,
                   totData.nextToken==3
                  ])
XX = XX.T
# yy = totData.tag=="@airport"
yy = totData.tag==u"LOC"
#--------------------------------------------
from sklearn import naive_bayes, linear_model
from sklearn.metrics import classification_report, confusion_matrix
clf = naive_bayes.BernoulliNB()
clf2 = linear_model.LogisticRegression()
clf.fit(XX,yy)
clf2.fit(XX,yy)
print(classification_report(yy,clf.predict(XX)))
print(classification_report(yy,clf2.predict(XX)))

XX.shape[0]

#-----------------------------------
# swedish NER data
swtrain = []
import io
with io.open('./Data/train_corpus.txt', mode='r', encoding='utf-8') as f:
    sents = f.read()
sents = sents.split('\n\n')
swtr_token_tag_pairs = [[('<start>','B')]+[tuple(pair.split('\t')) for pair in sent.split('\n')]+[('<end>','B')] for sent in sents]
sw_aug_data = data_augmentation(swtr_token_tag_pairs)
SwedData = pd.DataFrame(sw_aug_data)
SwedData.columns = ["token","tag", "prevToken","nextToken", "prevLen","tokenLen","nextLen"]

SwXX = make_binary_features(SwedData)
SwXX = SwXX.T
Swyy = SwedData.tag=="LOC"
sum(Swyy)/len(Swyy)
print(classification_report(Swyy, clf.predict(SwXX)))

print(confusion_matrix(Swyy,clf.predict(SwXX)))

tvals = pd.DataFrame([list(Swyy),list(clf.predict(SwXX))],dtype=bool)
tvals = tvals.T
fps = (tvals.Truth==False) & (tvals.Prediction==True)
fns = (tvals.Truth==True) & (tvals.Prediction==False)
tvals.columns = ['Truth','Prediction']
dd = clf.predict(SwXX)
dd[:10]
Swyy[:10]

#--------------------------------------------
clf = naive_bayes.BernoulliNB()
clf2 = linear_model.LogisticRegression()
clf.fit(SwXX,Swyy)
clf2.fit(SwXX,Swyy)
print(classification_report(Swyy, clf.predict(SwXX)))
print(classification_report(yy,clf.predict(XX)))
