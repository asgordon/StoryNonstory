#!/usr/bin/python

# ltc.py - a linear text classifier

# Andrew S. Gordon 
# v.1 Sept 9, 2014
# v.2 Sept 29, 2014

from __future__ import print_function
import sys

def loadModel(modname):
    w = dict()
    c = [ ]
    with open(modname, "r") as f:
        c = f.readline().split()[1:]
        for line in f:
            arr = line.split()
            fname = arr[0]
            fws = [float(numeric_string) for numeric_string in arr[1:]]
            w[fname] = fws
    return w, c

def classify(feats, w, c):
    res = [0.0] * len(c)
    feats.append("**BIAS**")
    for f in feats:
        if f in w:
            res = [x + y for x,y in zip(res, w[f])] 
    return(c[res.index(max(res))])

if __name__ == "__main__":
    ltcmodname = sys.argv[1]
    print ("Loading model.", file=sys.stderr)        
    w, c = loadModel(ltcmodname)
    print ("Finished loading model.", file=sys.stderr)
    while 1:
        line = sys.stdin.readline()
        if not line: 
            break

        line = line.strip()
        f = line.split()

        print(classify(f, w, c))
        sys.stdout.flush()




