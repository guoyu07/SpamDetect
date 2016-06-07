# coding=utf-8


STOPWORDS = []
f = open('resource/stopwords.txt', 'r')
lines = f.readlines()
for line in lines:
    line = line.strip()
    line = line.replace(' ', '')
    if line == '' or line.isalpha():
        continue
    words = line.split(',')
    STOPWORDS += words

print '[',
for word in STOPWORDS:
    print "u'" + word + "',",

print ']'
