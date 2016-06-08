# coding=utf-8
from rawdata import data2vec
from bayesian import MultiNomialNB, BernoulliNB
from randomdata import *
from report import accuracyMetric, showMetric
from features import *
import time
from numpy import mean
from math import sqrt

vecs = data2vec('trec06c/full/index', 5000)
groups = randomSplit2(vecs[0] + vecs[1], 0.5)
trainset = groups[0]
testset = groups[1]
FeaturenNum = 40

def initFeatures():
    classifier = BernoulliNB()
    classifier.train(trainset, MutualInfo(FeaturenNum))
    return classifier.Features


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


def mean_distance(vecas, vecbs, matrix=None):
    sum = 0.0
    cnt = 0
    for a in vecas:
        for b in vecbs:
            cnt += 1
            if matrix:
                sum += matrix[a[0]][b[0]]
            else:
                sum += distance(a, b)
    return sum / cnt


def cluster(vecs, matrix=None):
    mind = 2.0
    minij = []
    vecs = [[vec] for vec in vecs]
    while mind == 2.0 or mind < 0.3:
        if mind != 2.0:
            vecs[minij[0]] = vecs[minij[0]] + vecs[minij[1]]
            del vecs[minij[1]]
            mind = 2.0
        for i in range(len(vecs)):
            for j in range(max(i+1,5), len(vecs)):
                tmpd = mean_distance(vecs[i], vecs[j], matrix)
                if tmpd < mind:
                    mind = tmpd
                    minij = [i, j]
    return vecs


features = initFeatures()
featurevecs = feature_vecs(features, trainset)
MATRIX = feature_matrix(featurevecs)

# max = -1.0
# min = 1.0
# for i in MATRIX:
#     for j in MATRIX[i]:
#         if MATRIX[i][j] > max:
#             max = MATRIX[i][j]
#         if MATRIX[i][j] < min:
#             min = MATRIX[i][j]

# print max, min


vecs = cluster(featurevecs, MATRIX)

print len(vecs)
for c in vecs:
    print mean_distance(c, c, MATRIX),
    for v in c:
        print v[0],
    print

num = 20
print '[',
cnt = 0
for c in vecs:
    print "u'" + c[0][0] + "', ",
    cnt += 1
    if cnt == num:
        break
print ']'
