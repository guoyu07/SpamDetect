# coding=utf-8
import re


def useless_word(word):
    if check_string(word) == 0:
        return True
    return False

# 0:u'中国★', 1:u'中国', 2:u'！。', 3:u'中国。'
def check_string(string):
    if re.match(u'^[\u4e00-\u9fff]+$', string) != None:
        return 1
    elif re.match(u'^[·！￥……（）——【】、：；‘’“”《》，。？]+$', string) != None:
        return 2
    elif re.match(u'^[\u4e00-\u9fff·！￥……（）——【】、：；‘’“”《》，。？]+$', string) != None:
        return 3
    return 0
