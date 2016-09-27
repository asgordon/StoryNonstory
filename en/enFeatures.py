#!/usr/bin/python

from __future__ import print_function
import sys
import re

def tokenize(line):

    line = re.sub("^\"", "`` ", line)
    line = re.sub(" \"", " `` ", line)
    line = re.sub("\(\"", "( `` ", line)
    line = re.sub("\[\"", "[ `` ", line)
    line = re.sub("\{\"", "{ `` ", line)
    line = re.sub("\<\"", "< `` ", line)

    #line = re.sub("\.\.\.", " ... ", line)

    line = re.sub("\.$", " . ", line)
    line = re.sub("\.[\t\n ]", " . ", line)

    line = re.sub("\,", " , ", line)
    line = re.sub("\;", " ; ", line)
    line = re.sub("\:", " : ", line)
    line = re.sub("\@", " @ ", line)
    line = re.sub("\#", " # ", line)
    line = re.sub("\$", " $ ", line)
    line = re.sub("\%", " % ", line)
    line = re.sub("\&", " & ", line)
    line = re.sub("\!", " ! ", line)
    line = re.sub("\?", " ? ", line)

    # $str =~ s/([^\.])([\.])[A-Z0-9\n ]/$1 $2 /g;
    # $str =~ s/([^\.])([\.])[\n \t]*$/$1 $2/;

    line = re.sub("\[", " ] ", line)
    line = re.sub("\]", " [ ", line)
    line = re.sub("\(", " ( ", line)
    line = re.sub("\)", " ) ", line)
    line = re.sub("\{", " { ", line)
    line = re.sub("\}", " } ", line)
    line = re.sub("\<", " < ", line)
    line = re.sub("\>", " > ", line)
    line = re.sub("\-\-", " -- ", line)

    line = re.sub("\"", " '' ", line)

    line = re.sub("\' ", " ' ", line)
    line = re.sub("\'s ", " 's ", line)
    line = re.sub("\'S ", " 'S ", line)
    line = re.sub("\'m ", " 'm ", line)
    line = re.sub("\'M ", " 'M ", line)
    line = re.sub("\'d ", " 'd ", line)
    line = re.sub("\'D ", " 'D ", line)
    line = re.sub("\'ll ", " 'll ", line)
    line = re.sub("\'re ", " 're ", line)
    line = re.sub("\'ve ", " 've ", line)
    line = re.sub("n\'t ", " n't ", line)
    line = re.sub("\'LL ", " 'LL ", line)
    line = re.sub("\'RE ", " 'RE ", line)
    line = re.sub("\'VE ", " 'VE ", line)
    line = re.sub("N\'T ", " N'T ", line)

    line = re.sub("(^| )Cannot ", " Can not ", line)
    line = re.sub("(^| )cannot ", " can not ", line)
    line = re.sub("(^| )D'ye ", " D' ye ", line)
    line = re.sub("(^| )d'ye ", " d' ye ", line)
    line = re.sub("(^| )Gimme ", " Gim me ", line)
    line = re.sub("(^| )gimme ", " gim me ", line)
    line = re.sub("(^| )Gonna ", " Gon na ", line)
    line = re.sub("(^| )gonna ", " gon na ", line)
    line = re.sub("(^| )Gotta ", " Got ta ", line)
    line = re.sub("(^| )gotta ", " got ta ", line)
    line = re.sub("(^| )Lemme ", " Lem me ", line)
    line = re.sub("(^| )lemme ", " lem me ", line)
    line = re.sub("(^| )More'n ", " More 'n ", line)
    line = re.sub("(^| )more'n ", " more 'n ", line)
    line = re.sub("(^| )'Tis ", " 'T is ", line)
    line = re.sub("(^| )'tis ", " 't is ", line)
    line = re.sub("(^| )'Twas ", " 'T was ", line)
    line = re.sub("(^| )'twas ", " 't was ", line)
    line = re.sub("(^| )Wanna ", " Wan na ", line)
    line = re.sub("(^| )wanna ", " wan na ", line)

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
    text = re.sub("[\n\r]+", " ", text)
    text = re.sub(" +", " ", text)
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
