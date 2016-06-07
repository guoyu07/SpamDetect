# coding=utf-8
from rawdata import data2vec
from bayesian import MultiNomialNB, BernoulliNB
from randomdata import *
from report import accuracyMetric, showMetric
from features import *
import time


vecs = data2vec('trec06c/full/index', 5000)
groups = randomSplit2(vecs[0]+vecs[1], 0.5)

trainset = groups[0]
testset = groups[1]
FeaturenNum = 50


classifier = BernoulliNB()
classifier.train(trainset, CombineExtractor(FeaturenNum))
