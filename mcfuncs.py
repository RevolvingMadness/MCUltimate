from mcvars import *
def until_char(text, char):
    res = ''
    for i in range(len(text)):
        if text[i] != char:
            res += text[i]
        else:
            break
    return res

def to_nbt_item(item):
    item = str(item)[1:-1]
    text = ''
    text += 'id:"' + until_char(item, '{') + '",Count:1b,tag:{'
    item = item[len(until_char(item, '{')):]
    item = item[1:-1]
    text += item + '}}'
    return text