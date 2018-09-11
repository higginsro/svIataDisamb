# coding: utf-8
import re
import os
import io
from utilities.RDRPOSTagger.pSCRDRtagger.RDRPOSTagger import RDRPOSTagger,readDictionary
# def find_possible_airport_pairs(query):
#     to_from = re.findall(r'(till\s)?(\w{3})\s(från\s)?(\w{3})\s',query)
#     from_to = re.findall(r'(från\s)?(\w{3})\s(till\s)?(\w{3})\s',query)
#     return (to_from,from_to)

ss = 'jag vill flyga till ber från par'
tt = 'ber par imorgon'
qq = 'flyg till ber lhr'
ww = 'vill flyga från ber till min'
zamps = [ss,tt,qq,ww]
dir_path=os.path.dirname(os.path.abspath(__file__))

# Intersection of 3 letter swedish words and Iata codes
with io.open(os.path.join(dir_path, 'Data', 'SwedishIataIntersection.txt'), mode='r') as f:
    intersection = f.read().split()

# Set of 3-letter Swedish words less Iata codes
with io.open(os.path.join(dir_path, 'Data', 'SwedishLessIata.txt'), mode='r') as g:
    svLessIata = g.read().split()

# Set of Iata codes less Swedish words
with io.open(os.path.join(dir_path, 'Data', 'IataLessSwedish.txt'), mode='r') as h:
    iataLessSv = h.read().split()
tillonly = 'till ber par'
tillonlyback = 'ber till par'
franonly = 'från ber par'
franonlyback = 'ber från par'

one_prep_words = [tillonly,tillonlyback, franonly, franonlyback]

tokenise = lambda query: query.strip('.').split()
certains = lambda tokens: [t for t in tokens if t not in intersection and len(t)==3]
def probable_airports(query,inIntersection):
    '''
    returns two lists one of probable airports and their indices,
    the other with possible airports and their indices.
    The definitely not airports dealt with upstream
    :param query:
    :return:
    '''
    tokens = tokenise(query)
    probable_airports = []
    possible_airports = []
    probable_non_airports = []
    for token,n in inIntersection:
        if len(token) == 3:
            scores = [0.0]
            print "tokens length: {}".format(len(tokens))
            if n==0:
                print len(tokens) > 1
                if len(tokens)>1 and (tokens[n+1] == u'till' or tokens[n+1] == u'från'):
                    scores.append(0.9)
            if n<len(tokens)-1 and len(tokens[n+1]) == 3:
                scores.append(0.5)
            if n > 0:
                if tokens[n-1] == u'till' or tokens[n-1] == u'från':
                    scores.append(0.9)
                elif len(tokens[n-1]) == 3:
                    scores.append(0.5)
            maxscore = max(scores)
            if maxscore > 0.8:
                probable_airports.append((token,n))
            elif maxscore > 0.1:
                possible_airports.append((token,n))
            else:
                probable_non_airports.append((token,n))
    return probable_airports,possible_airports,probable_non_airports

cands = ['ber par',
         'till ber par',
         'från ber par',
         'ber par från',
         'ber par till',
         'från ber till par'
         ]

import os
# pa_cands = [probable_airports(q) for q in cands]

# Tag a tokenized/word-segmented sentence

# r.tagRawSentence(DICT, "jag vill flyga till paris")

def disAmbiguation(tagged,possible_airports):

    # Tag a tokenized/word-segmented sentence
    print tagged
    tagged_utt = re.split(r'\s', tagged)
    probable_non_airports = []
    probable_airports = []
    for token,n in possible_airports:
        if 'NOUN' not in tagged_utt[n] and 'PROPN' not in tagged_utt[n]:
            probable_non_airports.append((token,n))
        else:
            probable_airports.append((token,n))
    return probable_airports,probable_non_airports

def intersectionElements(query,intersection):
    tokens = tokenise(query)
    elements = []
    for n,token in enumerate(tokens):
        if token in intersection:
            elements.append((token,n))
    return elements

def run(query):
    global dir_path
    # print(__file__)
    # dir_path = os.path.dirname(os.path.abspath(__file__))
    # print(dir_path)
    with io.open(os.path.join(dir_path,'Data','SwedishIataIntersection.txt'),mode='r') as f:
        intersection = f.read().split()

    swedishIata = intersectionElements(query,intersection)
    # dir_path = os.getcwd()
    os.chdir(os.path.join(dir_path, 'utilities', 'RDRPOSTagger', 'pSCRDRtagger'))

    r = RDRPOSTagger()

    # Load the POS tagging model for swedish

    r.constructSCRDRtreeFromRDRfile("../Models/UniPOS/UD_Swedish/sv-upos.RDR")

    # Load the lexicon for swedish

    DICT = readDictionary("../Models/UniPOS/UD_Swedish/sv-upos.DICT")

    print "intersection {}".format(swedishIata)
    probable,possible,non_airports = probable_airports(query,swedishIata)
    print('probabale,\tpossible,\tnon_airports')
    print(probable,possible,non_airports)
    if possible:
        tagged = r.tagRawSentence(DICT,query)
        print(tagged)
        probs,probs_not = disAmbiguation(tagged,possible)
        probable = probable+probs
        print('probable now')
        print(probable)
        return {'probably_airports':probable,
                'probably_not_airports':probs_not+non_airports}
    else:
        return{'probably_airports':probable,
               'probably_not_airports':non_airports}
