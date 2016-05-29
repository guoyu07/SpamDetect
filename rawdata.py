# coding=utf-8

import jieba
import os

jieba.enable_parallel()


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


def email2dict(filename):
    info = readEmail(filename)
    words = jieba.cut(''.join(info[1])
                      .replace('。', '。' + os.linesep)
                      .replace('，', '，' + os.linesep)
                      .replace('；', '；' + os.linesep)
                      .replace('、', '、' + os.linesep)
                      .replace('！', '！' + os.linesep)
                      .replace('？', '？' + os.linesep))
    wordcnt = {}
    for word in words:
        word = word.encode('utf-8')
        if word in wordcnt:
            wordcnt[word] = wordcnt[word] + 1
        else:
            wordcnt[word] = 1
    return wordcnt


def data2vec(indexfile, max=-1):
    f = file(indexfile, 'r')
    lines = f.readlines()
    lines = [line.strip().split(' ') for line in lines]
    if max == -1:
        max = len(lines)

    vectors = [[], []]
    cnt = 0
    for line in lines:
        emailvec = []
        positive = 1 if line[0].lower() == 'spam' else 0
        emailvec.append(positive)

        path = os.path.join('trec06c/utf8/', '/'.join(line[1].split('/')[-2:]))
        worddict = email2dict(path)

        emailvec.append(worddict)
        vectors[positive].append(emailvec)
        cnt += 1
        if cnt >= max:
            break
    return vectors



vecs = data2vec('trec06c/full/index', 1000)
print len(vecs[0]), len(vecs[1])
