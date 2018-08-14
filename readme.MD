## Intro
this is a rule-based 'classifier' built from observations about
the context in which airport IATA codes occur in our data.
A basic Bernoulli Naive Bayes was initally built, but made obvious errors which
a hand-built system wouldn't. Time permitting a more sophisticated model would have been built.
NOTE:
At present there is some issue with unicode string comarison

## DATA
Data from which the rules were learnt is form the Swedish dev agent's training phrases for its intents

## Logic
the findCandidates.py file and run() function contain the logic.
which is as follows:
1. query is tokenised. All three letter words are checked for membership in the
intersection of a Swedish dictionary and the IATA codes taken from that appear in the airport entity of Swedish_dev bot.
2. If a 3-letter token is in the intersection, checks are performed for the words in its immediate context
such as if len==3, or 'till' or 'från' are adjacent.
3. If these checks are not conclusive, the utterance is tagged with Parts-of-Speech
and further checks about the types of tags are performed.

## TODO
Deployment remains to be done.
A flask template is in SvIataDisambiguation