# coding=utf-8
import random
from sklearn import preprocessing


def randomSplit(examples, num):
    remain = examples[:]
    groupnum = len(examples) / num
    groups = []
    for i in range(num - 1):
        group = random.sample(remain, groupnum)
        for g in group:
            remain.remove(g)
        groups.append(group)
    groups.append(remain)
    return groups


def randomSplit2(examples, ratio):
    remain = examples[:]
    num = int(len(examples) * ratio)
    trainset = random.sample(remain, num)
    for t in trainset:
        remain.remove(t)
    return [trainset, remain]


# 有放回采样
def randomDraw(examples, num):
    samples = []
    for i in range(num):
        samples.append(examples[random.randint(0, len(examples) - 1)])
    return samples


# 轮盘赌
def roulette(examples, num, P):
    samples = []
    for i in range(num):
        pointer = random.random()
        sum = 0.0
        for j in range(len(P)):
            sum += P[j]
            if sum > pointer:
                samples.append(examples[j])
                break
    return samples


def normalize(trainset):
    X = [e[0] for e in trainset]
    X = preprocessing.scale(X)
    # X = preprocessing.normalize(X, norm='l2')
    return [[X[i], trainset[i][1]] for i in range(len(trainset))]


def balance(examples):
    positive = [e for e in examples if e[1] == 1]
    negative = [e for e in examples if e[1] == 0]
    avelength = (len(positive) + len(negative)) / 2

    if len(positive) < avelength:
        copy = random.sample(positive, avelength - len(positive))
        positive = positive + copy
        negative = random.sample(negative, avelength)
        trainset = positive + negative
    elif len(positive) > avelength:
        copy = random.sample(negative, avelength - len(negative))
        negative = negative + copy
        positive = random.sample(positive, avelength)
        trainset = positive + negative
    return trainset
