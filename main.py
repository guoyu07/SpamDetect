# coding=utf-8
from rawdata import data2vec
from bayesian import MultiNomialNB, BernoulliNB
from randomdata import *
from report import accuracyMetric, showMetric

vecs = data2vec('trec06c/full/index', 1000)
groups = randomSplit2(vecs[0]+vecs[1], 0.5)

# classifier = MultiNomialNB()
classifier = BernoulliNB()

trainset = groups[0]
testset = groups[1]

classifier.train(trainset)
predicted = classifier.predict([sample[1] for sample in testset])
expected = [sample[0] for sample in testset]

showMetric(accuracyMetric(expected, predicted))


