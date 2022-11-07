from mcvars import *
def to_nbt_item(item, count, nbts=[]):
    text = ''
    text = 'Item:{id:"minecraft:' + item + '",Count:' + str(count)+ 'b'
    if nbts != []:
        text += ',tag:{'
        for nbt in nbts:
            text += str(nbt)
        text += '}'
    text += '}}'