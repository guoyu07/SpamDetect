# coding=utf-8
from math import log
from features import DefaultFeature


class MultiNomialNB():
    WordCnt = [{}, {}, {}]
    NumCnt = [0, 0, 0]
    Features = set([])

    def __int__(self):
        self.WordCnt = [{}, {}, {}]
        self.NumCnt = [0, 0, 0]

    def train(self, trainset, featureExtractor=DefaultFeature()):
        for sample in trainset:
            positive = sample[0]
            vector = sample[1]
            for word in vector:
                self.WordCnt[positive][word] = \
                    self.WordCnt[positive][word] + vector[word] \
                    if word in self.WordCnt[positive] else vector[word]
                self.WordCnt[2][word] = self.WordCnt[2][word] + vector[word] \
                    if word in self.WordCnt[2] else vector[word]
                self.NumCnt[positive] += vector[word]
                self.NumCnt[2] += vector[word]
        self.Features = set(self.WordCnt[2].keys())
        self.Features = featureExtractor.extract_features(self)

    def PofC(self, positive):
        return 1.0 * self.NumCnt[positive] / self.NumCnt[2]

    def PofTermC(self, word, positive):
        if word in self.WordCnt[positive]:
            return 1.0 * (self.WordCnt[positive][word] + 1) / \
                (self.NumCnt[positive] + len(self.WordCnt[2]))
        elif word in self.WordCnt[2]:
            return 1.0 / (self.NumCnt[positive] + len(self.WordCnt[2]))
        return -1

    def PofTerm(self, word):
        if word in self.WordCnt[2]:
            return 1.0 * (self.WordCnt[2][word] + 1) / \
                (self.NumCnt[2] + len(self.WordCnt[2]))
        return -1

    def PofCTerm(self, word, positive):
        return self.PofC(positive) * self.PofTermC(word, positive) \
            / self.PofTerm(word)

    def _predict(self, vector):
        positive = log(self.PofC(1))
        # positive = self.PofC(1)
        negative = log(self.PofC(0))
        # negative = self.PofC(0)
        for word in self.Features:
            if word not in vector:
                continue
            tmp = self.PofTermC(word, 1)
            if tmp > 0:
                positive += log(tmp) * vector[word]
                # positive += log(tmp)
                # positive *= tmp

            tmp = self.PofTermC(word, 0)
            if tmp > 0:
                negative += log(tmp) * vector[word]
                # negative += log(tmp)
                # negative *= tmp

        # print 'positive:%f negative:%f' % (positive, negative)
        return 1 if positive > negative else 0

    def predict(self, X):
        ans = []
        for vector in X:
            ans.append(self._predict(vector))
        return ans


class BernoulliNB():
    WordCnt = {}
    DocCnt = [0, 0, 0]
    Features = set([])

    def __int__(self):
        self.WordCnt = {}
        self.DocCnt = [0, 0, 0]

    def train(self, trainset, featureExtractor=DefaultFeature()):
        for sample in trainset:
            positive = sample[0]
            vector = sample[1]
            for word in vector:
                if word not in self.WordCnt:
                    self.WordCnt[word] = [[], [], []]
                self.WordCnt[word][positive].append(vector[word])
                self.WordCnt[word][2].append(vector[word])
                self.DocCnt[positive] += 1
                self.DocCnt[2] += 1
        self.Features = set(self.WordCnt.keys())
        self.Features = featureExtractor.extract_features(self)

    def PofC(self, positive):
        return 1.0 * self.DocCnt[positive] / self.DocCnt[2]

    def PofTermC(self, word, positive):
        if word in self.WordCnt:
            return 1.0 * (len(self.WordCnt[word][positive]) + 1) / (self.DocCnt[positive] + 2)
        return -1

    def PofTerm(self, word):
        if word in self.WordCnt:
            return 1.0 * (len(self.WordCnt[word][2]) + 1) / (self.DocCnt[2] + 2)
        return -1

    def PofCTerm(self, word, positive):
        return self.PofC(positive) * self.PofTermC(word, positive) \
            / self.PofTerm(word)

    def _predict(self, vector):
        positive = log(self.PofC(1))
        # positive = self.PofC(1)
        negative = log(self.PofC(0))
        # negative = self.PofC(0)
        for word in self.Features:
            if word not in vector:
                tmp = self.PofTermC(word, 1)
                if tmp > 0:
                    positive += log(1 - tmp)
                    # positive *= tmp

                tmp = self.PofTermC(word, 0)
                if tmp > 0:
                    negative += log(1 - tmp)
                    # negative *= tmp
            else:
                tmp = self.PofTermC(word, 1)
                if tmp > 0:
                    positive += log(tmp)
                    # positive *= tmp

                tmp = self.PofTermC(word, 0)
                if tmp > 0:
                    negative += log(tmp)
                    # negative *= tmp

        # print 'positive:%f negative:%f' % (positive, negative)
        return 1 if positive > negative else 0

    def predict(self, X):
        ans = []
        for vector in X:
            ans.append(self._predict(vector))
        return ans


# trainset = [
#     [0, {'a': 1}],
#     [1, {'b': 1}]
# ]
# classifier = MultiNomialNB()
# classifier = BernoulliNB()
# classifier.train(trainset)
# print classifier.DocCnt
# print classifier.WordCnt
# print classifier.predict([{'a', 1}])
