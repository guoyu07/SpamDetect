# coding=utf-8

import jieba
import os


def convert2utf8(srcf, tarf):
    sf = open(srcf, 'r')
    tf = open(tarf, 'w')
    lines = sf.readlines()
    utf8 = []
    for line in lines:
        try:
            utf8.append(line.decode('gbk').encode('utf-8'))
        except Exception, e:
            print repr(e)
            continue
    tf.writelines(utf8)


def data2utf8(srcdir, tardir):
    paths = os.listdir(srcdir)
    if not os.path.exists(tardir):
        os.mkdir(tardir)
    for path in paths:
        if os.path.isdir(os.path.join(srcdir, path)):
            data2utf8(os.path.join(srcdir, path), os.path.join(tardir, path))
        else:
            convert2utf8(os.path.join(srcdir, path),
                         os.path.join(tardir, path))

# data2utf8('../trec06c/data/', '../trec06c/utf8/')


def readEmail(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    lines = [line.strip().replace(' ', '').replace('\t', '') for line in lines]
    info = [[], []]
    po = 0
    for line in lines:
        if line == '':
            po = 1
            continue
        info[po].append(line)
    return info

# info = readEmail('trec06c/utf8/000/000')

# print ','.join(jieba.cut(''.join(info[1]))).encode('utf-8')
