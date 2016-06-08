# coding=utf-8
from rawdata import data2vec
from bayesian import MultiNomialNB, BernoulliNB
from randomdata import *
from report import accuracyMetric, showMetric
from features import *
import time
from numpy import mean
from math import sqrt

vecs = data2vec('trec06c/full/index', 1000)
groups = randomSplit2(vecs[0] + vecs[1], 0.5)
trainset = groups[0]
testset = groups[1]
FeaturenNum = 50

def initFeatures():
    classifier = BernoulliNB()
    classifier.train(trainset, DefaultFeature(FeaturenNum))
    return CombineExtractor(FeaturenNum).extract_features(classifier)


def feature_vecs(Features, trainset):
    vecs = []
    for feature in Features:
        vec = []
        for sample in trainset:
            if feature in sample[1]:
                vec.append(1)
            else:
                vec.append(0)
        vecs.append([feature, vec])
    return vecs


def pearson(veca, vecb):
    a, b = veca[1], vecb[1]
    length = len(a)
    aa = [a[i] * a[i] for i in range(length)]
    ab = [a[i] * b[i] for i in range(length)]
    bb = [b[i] * b[i] for i in range(length)]
    meana, meanb = mean(a), mean(b)
    meanaa, meanbb = mean(aa), mean(bb)
    up = mean(ab) - meana * meanb
    down = sqrt((meanaa - meana * meana) * (meanbb - meanb * meanb))
    return up / down


def distance(veca, vecb):
    return 1.0 - pearson(veca, vecb)



def feature_matrix(vecs):
    matrix = {}
    for veca in vecs:
        matrix[veca[0]] = {}
        for vecb in vecs:
            matrix[veca[0]][vecb[0]] = distance(veca, vecb)
    return matrix


def mean_distance(vecas, vecbs):
    sum = 0.0
    cnt = 0
    for a in vecas:
        for b in vecbs:
            cnt += 1
            sum += distance(a, b)
    return sum / cnt


def cluster():
    pass

features = initFeatures()
featurevecs = feature_vecs(features, trainset)
MATRIX = feature_matrix(featurevecs)

max = -1.0
min = 1.0
for i in MATRIX:
    for j in MATRIX[i]:
        if MATRIX[i][j] > max:
            max = MATRIX[i][j]
        if MATRIX[i][j] < min:
            min = MATRIX[i][j]

print max, min
