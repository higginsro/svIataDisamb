from os import path
import json
import io
dir_path = path.dirname(path.realpath(__file__))
targetP = path.join(dir_path)
def load_raw_utts():
    with io.open(path.join(targetP,"intents.json"), mode="r", encoding='utf-8') as f:
        intents = json.load(f)
        utterances = [utt for intent in intents.values() for utt in intent['userSays']]
    return utterances
# sentences in 'userSays'
# for each usersays, want each token and 'alias' if any.

def pte(utterance_list):
    ss = ''.join([item['text'] for item in utterance_list])
    return ss


# with io.open('DF_training_utt_raw_sentences.txt', mode='w', encoding='utf-8')as g:
#     for uttl in utterances:
#         g.write(pte(uttl['data']) + '.\n')

def add_tags(utterances):
    '''creates tags for each token. UNK for not airport,
    B for stand/end of sentence, and LOC for airport.'''
    raw_sentences = []
    for utt in utterances:
        sentence = [('<start>', 'B')]
        for chunk in utt['data']:
            if 'alias' in chunk and chunk['meta']=='@airport':
                token, tag = chunk['text'], 'LOC'
                sentence.append((token, tag))
            else:
                sentence.extend([(item, "UNK") for item in (chunk['text'].split())])
        sentence.append(('<end>', 'B'))
        raw_sentences.append(sentence)
    return raw_sentences

def load_DF_data():
    return add_tags(load_raw_utts())