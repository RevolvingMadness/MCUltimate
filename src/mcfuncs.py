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

def insert_to_file(file, index, text):
    try:
        content = open(file, 'r').read()
    except:
        open(file, 'w').write('')
        content = ''
    open(file, 'w').write(content[:index] + text + content[index:])

def get_json_item_name(json):
    return json.get('text').lower().replace(' ', '_')