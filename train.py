#!/usr/bin/python

# train.py : averaged perceptron training for linear text classifiers
# usage: python train.py features.txt labels.txt > model.txt

# Andrew S. Gordon
# Sept 2014

from __future__ import print_function
import sys
from random import shuffle
from classify import classify

def loadData(featuresname, labelsname):
    with open(labelsname) as ln:
        labels = ln.read().splitlines()
    with open(featuresname) as fn:
        features = [line.strip().split() for line in fn]
    if len(labels) != len(features):
        raise Exception("Feature file and label file are of different lengths.")
    d = zip(labels, features) # list of tuples (labelstr, featurelist)
    c = list(set(labels))
    return d, c

def trainModel(d, c, epochs = 10, rate = 1.0, averaged = True):
    w = dict()
    cw = dict()
    w["**BIAS**"] = [0.0] * len(c)

    for i in xrange(epochs):
        shuffle(d)
        incorrect = 0;
        for item in d:
            predicted = classify(item[1], w, c)
            if (predicted != item[0]):
                incorrect += 1
                u = [0.0] * len(c)
                u[c.index(predicted)] -= rate
                u[c.index(item[0])] += rate
                w["**BIAS**"] = [x + y for x, y in zip(u, w["**BIAS**"])]
                for f in item[1]:
                    if f in w:
                        w[f] = [x + y for x, y in zip(u, w[f])]
                    else:
                        w[f] = u
        for f in w:
            if f in cw:
                cw[f] = [x + y for x, y in zip(w[f], cw[f])]
            else:
                cw[f] = w[f]
        acc = float(len(d) - incorrect) / float(len(d))
        print ("Epoch " + str(i) + ": " + str(acc) + " accuracy", file=sys.stderr)
    if averaged:
        for f in cw:
            w[f] = [x / epochs for x in cw[f]]
    incorrect = 0;
    for item in d:
        predicted = classify(item[1], w, c)
        if predicted != item[0]:
            incorrect += 1
    acc = float(len(d) - incorrect) / float(len(d))
    print ("Final: " + str(acc) + " accuracy on training data", file=sys.stderr)
    return w

def crossValidate(d, c, folds=10):
    shuffle(d)
    cm = [[0 for x in xrange(len(c))] for x in xrange(len(c))]
    for i in xrange(folds):
        t_start = i * (len(d) / folds)
        t_end =  (i + 1) * (len(d) / folds)
        print(" fold " + str(i) + ": testing from item " + str(t_start) + " to " + str(t_end), file=sys.stderr)
        test = d[t_start : t_end]
        train = d[:]
        train[t_start:t_end] = []
        w = trainModel(train, c)
        for item in test:
            predicted = classify(item[1], w, c)
            cm[c.index(item[0])][c.index(predicted)] += 1
    print(c, file=sys.stderr)
    print(cm, file=sys.stderr)
    row_totals = [sum(x) for x in cm]
    col_totals = [sum(x) for x in zip(*cm)]
    correct = 0
    for i in xrange(len(c)):
        truepos = float(cm[i][i])
        correct += truepos
        pre = float(cm[i][i]) / float(col_totals[i])
        rec = float(cm[i][i]) / float(row_totals[i])
        f1 = 2.0 * (pre * rec) / (pre + rec)
        print(c[i] + ": " + str(pre) + " precision, " + str(rec) + " recall, " + str(f1) + " F1-measure", file=sys.stderr)
    acc = float(correct) / float(len(d))
    print (str(folds) + "-fold cross validation accuracy: " + str(acc), file=sys.stderr)


if __name__ == "__main__":
    featuresname = sys.argv[1]
    labelsname = sys.argv[2]

    print ("Loading data.", file=sys.stderr)
    d, c = loadData(featuresname, labelsname)
    print ("Finished loading data.", file=sys.stderr)
    
    print ("Training model.", file=sys.stderr)
    w = trainModel(d, c)
    print ("Finished training model.", file=sys.stderr)
    
    print("classlabels\t" + "\t".join(c))
    for key in w:
        print(key + "\t" + "\t".join(map(str, w[key])))

    print("Cross validating.", file=sys.stderr)
    crossValidate(d, c)
