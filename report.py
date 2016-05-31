# coding=utf-8
from math import sqrt

def accuracyMetric(expected, predicted):
    TP, FN, FP, TN = 0, 0, 0, 0
    for i in range(len(expected)):
        if expected[i] == 1 and predicted[i] == 1:
            TP += 1
        elif expected[i] == 1 and predicted[i] == 0:
            FN += 1
        elif expected[i] == 0 and predicted[i] == 1:
            FP += 1
        elif expected[i] == 0 and predicted[i] == 0:
            TN += 1
    return [[TP, FN], [FP, TN]]


def showMetric(metric):
    TP, FN, FP, TN = metric[0][0], metric[0][1], metric[1][0], metric[1][1]
    print '                       | Predicted Positive | Predicted Negative'
    print '    -------------------|--------------------|---------'
    print '    Condition Positive |', TP, '|', FN
    print '    Condition Negative |', FP, '|', TN

    print
    print '    accuracy', 1.0 * (TP + TN) / (TP + FN + FP + TN), '  '
    if TP + FP == 0:
        precision = 0
    else:
        precision = 1.0 * TP / (TP + FP)

    if TP + FN == 0:
        recall = 0
    else:
        recall = 1.0 * TP / (TP + FN)

    print '    precision', precision, '  '
    print '    recall', recall, '  '
    print '    F1-measure', 2.0 * precision * recall / (precision + recall), '  '
    print '    G-mean', sqrt(recall * TN / (TN + FP)), '  '
    print
