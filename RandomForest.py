"""
File:   RandomForest.py

Brief:  Implements the Random Forest classifier on csv-formatted input data. 
        Part of a homework project for CS170 at UC Berkeley.

Author: John Wilkey
"""
import math;
import sys;
import random;
NUM_TREES = 1;
N = 0;

class BinTree:
    """A simple binary tree implementation"""
    def __init__(self, l=None, r=None, index=None, threshold=None, v=None):
        self.l = l;
        self.r = r;
        self.index = index;
        self.thresh = threshold;
        self.label = v

class Sample:
    """Sample object. Each sample contains a feature vector and a class label"""
    def __init__(self, f,l):
        self.features = f
        self.label = l
        
def getData(path):
    """Read the data files from disk.

    Arguments:
    path    Relative path containing data files
    """

    outL = list();
    with open('hw12data/emailDataset/'+path+'Features.csv') as f,\
        open('hw12data/emailDataset/'+path+'Labels.csv') as l:
            for sample in zip(f,l):
                outL.append(Sample(  [float(x) for x in sample[0].split(',')],\
                                      int(sample[1])))
    return outL

def main():
    """Main algorithm"""

    NUM_TREES = int(sys.argv[1])
    N = int(sys.argv[2])
    print "Using ", NUM_TREES, "trees and N", N
    trainSamples = getData('train')
    valSamples = getData('val')
    sStar = [random.choice(trainSamples) for x in xrange(N)]
    treeList = [buildDecTree(trainSamples) for x in xrange(NUM_TREES)]
    outFile = open('emailOutput'+str(NUM_TREES)+'.csv', 'w')  # '+str(NUM_TREES)+'.csv','w')
    numRight = 0;
    for Si,S in enumerate(valSamples):
        answerList = [classify(S, t) for t in treeList]
        numSpam = [x for x in answerList if x == 1]
        ans = 1 if len(numSpam) > len(answerList)/float(2) else 0
        outFile.write(str(ans)+'\n')
        if S.label == ans: numRight += 1
        else: print "Misclassified ", Si, "as ", ans, "Should have been", S.label, "Accuracy: ", numRight/float(Si+1)
    print "DONE"
    outFile.close();

def classify(S, t):
    """Classify sample S using tree t"""

    if t.index == None:
        return t.label
    nextTree = t.l if S.features[t.index] <= t.thresh else t.r
    return classify(S, nextTree)

def H(s):
    """Compute the entropy value of sample s"""

    numSpam = len([x for x in s if x.label == 1])
    numHam = len(s) - numSpam;
    if numSpam == 0 or numHam == 0: return 0;
    return -1*(float(numSpam)/len(s))*math.log(float(numSpam)/len(s),2)-\
        (float(numHam)/len(s))*math.log(float(numHam)/len(s),2)

def gain(S, SL, SR):
    """Compute information gain from splitting set S into sets SL and SR"""

    result = H(S) - (float(len(SL))/(len(SL)+len(SR))*H(SL)) + (float(len(SR))/(len(SL)+len(SR))*H(SR));
    return result;

def partition(S, (threshold, index)):
    """Partition a set S into two sets determined by threshold and index"""

    l = [x for x in S if x.features[index] <= threshold]
    r = [x for x in S if x.features[index] > threshold]
    return (l,r)

def buildDecTree(S, d=0):
    """Build a single decision tree from training set S starting at depth d.

    Arguments:
    S   Training sample set to build the decision tree from.
    d   Current depth of the decision tree at the point that we're currently
        at while building it. Note that this value is only used in the 
        recursive calls to this function and therefore should be omitted when
        called from outside this function.
    """

    if len(set([s.label for s in S])) == 1:
        return BinTree(v=S[0].label);
    fIndexes = list()
    P = list()
    G = list()
    GG = list()
    while len(set(fIndexes)) < 8:
        candidate = random.randint(0,56)
        if not candidate in fIndexes:
            fIndexes.append(candidate)        
    features = [(sorted(set([s.features[i] for s in S]),reverse=True),i) for i in fIndexes]
    for feature in features:
        n = [((x+y)/2) for x,y in zip(feature[0], feature[0][1:])]
        if not n: n = feature[0]
        G.append((n,feature[1]))
    for g in G:
        p = list()
        for thresh in g[0]:
            p.append((partition(S, (thresh, g[1])),thresh,g[1]))
        P.append(p)
    for p in P:
        for vector in p:
            GG.append((gain(S, vector[0][0], vector[0][1]),vector[1],vector[2]))
    maxGain = max(GG, key=lambda x: x[0])
    (SL,SR) = partition(S, (maxGain[1], maxGain[2]))
    if not SL or not SR:
        ne = SL if SL else SR
        length = len(ne)
        numSpam = len([x.label for x in ne if x.label == 1])
        numHam = len([x.label for x in ne if x.label == 0])
        if numSpam >= len(ne)/float(2):
            label = 1
        else:
            label = 0
        return BinTree(v=label)
    return BinTree(buildDecTree(SL,d+1), buildDecTree(SR,d+1), threshold=maxGain[1], index=maxGain[2])

# Program entry point.
main();
