# coding:utf-8
import pandas as pd

def query2features(query):
    return makeBinaryFeatures(makeDataFrame(query))

def q2t(query):
    query.strip('.')
    tokens = ['<start>']+query.split()+['<end>']
    return tokens

def query2augmentedTokens(query):
    query.strip('.')
    tokens = ['<start>']+query.split()+['<end>']
    return token_augmentation(tokens=tokens)

def token_augmentation(tokens):
    '''
    creates contextual features for each token
    :param tokens: a list of tokens from an utterance/sentence
    :return:
    '''
    token_unigram_contexts = []
    for n,token in enumerate(tokens):
        prevTok = ' '
        prevLen = 0
        nextTok = ' '
        nextLen = 0
        tokenLen = 0
        if n != 0:
            prevTok = tokens[n - 1]
            prevLen = len(tokens[n - 1])
            tokenLen = len(token)
        if n < len(tokens) - 1:
            nextTok = tokens[n + 1]
            nextLen = len(tokens[n + 1])
            tokenLen = len(token)
        token_unigram_contexts.append([token, prevTok, nextTok, prevLen, tokenLen, nextLen])
    return token_unigram_contexts


def makeBinaryFeatures(tokenDF):
    binDF= pd.DataFrame([tokenDF.prevToken==u"till",
                   tokenDF.prevToken==u"från",
                   tokenDF.nextToken==u"till",
                   tokenDF.nextToken==u"från",
                   tokenDF.prevLen==3,
                   tokenDF.tokenLen==3,
                   tokenDF.nextToken==3
                  ])
    return binDF.T

def makeDataFrame(query):
    augmented_tokens = query2augmentedTokens(query)
    df = pd.DataFrame(augmented_tokens,columns=['token',
                                                'prevToken',
                                                'nextToken',
                                                'prevLen',
                                                'tokenLen',
                                                'nextLen'])
    return df

