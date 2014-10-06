#!/usr/bin/python

from __future__ import print_function
import sys
import re

def tokenize(line):
    return(line.split())
    
def bigrams(tokens):
    b = [x + ":" + y for x, y in zip(tokens[:-1], tokens[1:])]
    b.append("**START**:" + tokens[0])
    b.append(tokens[-1] + ":**END**")
    return(b)

def trigrams(tokens):
    t = [x + ":" + y + ":" + z for x, y, z in zip(tokens[:-2], tokens[1:-1], tokens[2:])]
    t.append("**START**:**START**:" + tokens[0])
    t.append(tokens[-1] + ":**END**:**END**")
    if len(tokens) > 1:
        t.append("**START**:" + tokens[0] + ":" + tokens[1])
        t.append(tokens[-2] + ":" + tokens[-1] + ":**END**")
    return(t)



def features(text):
    includeUnigrams = True
    includeBigrams = True
    includeTrigrams = True
    text = re.sub("[\n\r]*", "", line)
    text = re.sub(" +", " ", line)
    f = []
    tokens = tokenize(text)
    if includeUnigrams:
        f.extend(tokens)
    if includeBigrams:
        f.extend(bigrams(tokens))
    if includeTrigrams:
        f.extend(trigrams(tokens))
    return f

if __name__ == "__main__":
    while 1:
        line = sys.stdin.readline()
        if not line:
            break

        print(" ".join(features(line))) #space-delimited list
        sys.stdout.flush()
