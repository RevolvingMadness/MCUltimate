import os
import shutil
from mcfuncs import *

######################## DATAPACKS ########################

class Trigger:
    def __init__(self, datapack, name, on_trigger):
        self.datapack = datapack
        self.name = name
        self.on_trigger = on_trigger


class List:
    def __init__(self, *args):
        self.args = args

    def __repr__(self):
        return str(list(self.args))


class Double:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{str(self.value)}d'


class Pos:
    def __init__(self, coord):
        self.c = coord

    def __repr__(self):
        return self.c


class Scoreboard:
    datapack = 'd'

    def matches(values, result):
        global datapack
        for item in values:
            open(datapack.tickfunc, 'a').write(
                f'execute if score @s {item} matches {str(values.get(item))} run ')
        if type(result) == str:
            open(datapack.tickfunc, 'a').write(result + '\n')
        elif type(result) == Function:
            open(datapack.tickfunc, 'a').write(
                f'function {datapack.namespace}:{result.filename}\n')

    def __init__(self, datapack_arg, name, criteria):
        global datapack
        self.name = name
        self.criteria = criteria
        self.datapack = datapack_arg
        datapack = datapack_arg
        self.value = {}

    def set_score(self, who, value):
        open(self.datapack.tickfunc, 'a').write(
            f'scoreboard players set {who} {self.name} {str(value)}\n')


class Enchantment:
    AQUA_AFFINITY = 'aqua_affinity'
    BANE_OF_ARTHROPODS = 'bane_of_arthropods'
    BLAST_PROTECTION = 'blast_protection'
    CHANNELING = 'channeling'
    CURSE_OF_BINDING = 'curse_of_binding'
    CURSE_OF_VANISHING = 'curse_of_vanishing'
    DEPTH_STRIDER = 'depth_strider'
    EFFICIENCY = 'efficiency'
    FEATHER_FALLING = 'feather_falling'
    FIRE_ASPECT = 'fire_aspect'
    FIRE_PROTECTION = 'fire_protection'
    FLAME = 'flame'
    FORTUNE = 'fortune'
    FROST_WALKER = 'frost_walker'
    IMPALING = 'impaling'
    INFINITY = 'infinity'
    KNOCKBACK = 'knockback'
    LOOTING = 'looting'
    LOYALTY = 'loyalty'
    LUCK_OF_THE_SEA = 'luck_of_the_sea'
    LURE = 'lure'
    MENDING = 'mending'
    MULTISHOT = 'multishot'
    PIERCING = 'piercing'
    POWER = 'power'
    PROJECTILE_PROTECTION = 'projectile_protection'
    PROTECTION = 'protection'
    PUNCH = 'punch'
    QUICK_CHARGE = 'quick_charge'
    RESPIRATION = 'respiration'
    RIPTIDE = 'riptide'
    SHARPNESS = 'sharpness'
    SILK_TOUCH = 'silk_touch'
    SMITE = 'smite'
    SOUL_SPEED = 'soul_speed'
    SWEEPING_EDGE = 'sweeping_edge'
    SWIFT_SNEAK = 'swift_sneak'
    THORNS = 'thorns'
    UNBREAKING = 'unbreaking'


class Color:
    BLACK = 'black'
    DARK_BLUE = 'dark_blue'
    DARK_GREEN = 'dark_green'
    DARK_AQUA = 'dark_aqua'
    DARK_RED = 'dark_red'
    DARK_PURPLE = 'dark_purple'
    GOLD = 'gold'
    GRAY = 'gray'
    DARK_GRAY = 'dark_gray'
    BLUE = 'blue'
    GREEN = 'green'
    AQUA = 'aqua'
    RED = 'red'
    LIGHT_PURPLE = 'light_purple'
    PURPLE = 'light_purple'
    YELLOW = 'yellow'
    WHITE = 'white'

    def RGB(red, green, blue):
        return "#{:02x}{:02x}{:02x}".format(red, green, blue)


class Player:
    EVERYONE = '@a'
    MYSELF = '@s'
    SELF = '@s'
    RANDOM = '@r'
    ENTITIES = '@e'
    ALL_ENTITIES = '@e'
    NEAREST = '@p'
    player_types = ['@a', '@s', '@r', '@e', '@p']

    def __init__(self, name, nbt):
        self.name = name
        self.nbt = nbt
        if name in Player.player_types:
            self.text = name + '['
        else:
            if nbt != []:
                self.text = '@a[name=' + name
                self.text += ','
        for i, val in enumerate(self.nbt):
            if type(val) == Tags:
                self.text += val.to_nbt()
            else:
                self.text += str(val)
            if i != len(self.nbt)-1:
                self.text += ','
        self.text += ']'

    def __repr__(self):
        return self.text


class ArmorItems:
    def __init__(self, head='air', chestplate='air', leggings='air', boots='air'):
        self.head = head
        self.chestplate = chestplate
        self.leggings = leggings
        self.boots = boots

    def to_nbt(self):
        return '[{id:"' + self.boots + '",Count:1b}, ' + '{id:"' + self.leggings + '",Count:1b}, ' + '{id:"' + self.chestplate + '",Count:1b}, ' + '{id:"' + self.head + '",Count:1b}]'

    def __repr__(self):
        return self.to_nbt()


class Datapack:
    def __init__(self, namespace, location_arg, desc=''):
        self.location = location_arg
        self.namespace = namespace.lower()
        self.custom_items = []
        self.desc = desc
        self.tickfunc = self.location + \
            f'/data/{self.namespace}/functions/tick.mcfunction'
        self.loadfunc = self.location + \
            f'/data/{self.namespace}/functions/load.mcfunction'
        try:
            os.mkdir(self.location)
        except FileExistsError:
            shutil.rmtree(self.location)
            os.mkdir(self.location)
        open(self.location + '/pack.mcmeta', 'w').writelines('''{
    "pack": {
        "pack_format": 8,
        "description": ""
    }
}''')
        os.mkdir(self.location + '/data')
        os.mkdir(self.location + '/data/minecraft')
        os.mkdir(self.location + '/data/minecraft/tags')
        os.mkdir(self.location + '/data/minecraft/tags/functions')
        open(self.location + '/data/minecraft/tags/functions/load.json', 'w').writelines((
            '{\n'
            '    "values": [\n'
            f'      "{self.namespace}:load"\n'
            '    ]\n'
            '}'
        ))
        open(self.location + '/data/minecraft/tags/functions/tick.json', 'w').writelines((
            '{\n'
            '    "values": [\n'
            f'      "{self.namespace}:tick"\n'
            '    ]\n'
            '}'
        ))
        os.mkdir(self.location + f'/data/{self.namespace}')
        os.mkdir(self.location + f'/data/{self.namespace}/functions')
        self.function_num = 1

    def add_scoreboard(self, object):
        object.datapack = self
        open(self.loadfunc, 'a').write(
            f'scoreboard objectives remove {object.name}\n')
        open(self.loadfunc, 'a').write(
            f'scoreboard objectives add {object.name} {object.criteria}\n')
        return object

    def add_trigger(self, name, on_trigger):
        open(self.loadfunc, 'a').write(f'scoreboard objectives add {name} trigger\n')
        open(self.tickfunc, 'a').write(f'execute as @a at @s run execute if score @s {name} matches 1.. run {on_trigger}\n')
        open(self.tickfunc, 'a').write(f'scoreboard players set @a {name} 0\n')

    def gamerule(self, rule, val):
        open(self.loadfunc, 'a').write(f'gamerule {rule} {str(val).lower()}\n')


class Function:
    def __init__(self, datapack, type='func'):
        self.location = ''
        self.filename = ''
        self.datapack = datapack
        if type in ['main', 'tick']:
            open(datapack.location +
                 f'/data/{datapack.namespace}/functions/tick.mcfunction', 'w').write('')
            self.location = datapack.location + \
                f'/data/{datapack.namespace}/functions/tick.mcfunction'
            self.filename = 'tick'

        if type == 'load':
            open(datapack.location +
                 f'/data/{datapack.namespace}/functions/load.mcfunction', 'w').write('')
            self.location = datapack.location + \
                f'/data/{datapack.namespace}/functions/load.mcfunction'
            self.filename = 'load'

        if type == 'func':
            open(datapack.location +
                 f'/data/{datapack.namespace}/functions/function{str(datapack.function_num)}.mcfunction', 'w').write('')
            self.location = datapack.location + \
                f'/data/{datapack.namespace}/functions/function{str(datapack.function_num)}.mcfunction'
            self.filename = f'function{str(datapack.function_num)}'
            datapack.function_num += 1

    def fill(self, from_, to, block, replace=None):
        self.text = f'fill {from_} {to} {block}'
        if replace != None:
            self.text += ' replace ' + replace
        open(self.location, 'a').write(self.text + '\n')

    def function(self, func):
        open(self.location, 'a').write(
            f'function {self.datapack.namespace}:{func.filename}')

    def execute_as(self, who):
        open(self.location, 'a').write(f'execute as {who} at @s run ')

    def say(self, text):  # /say <text>
        open(self.location, 'a').write(f'say {text}\n')

    def run(self, function):  # /function <function>
        open(self.location, 'a').write(
            f'function {self.datapack.namespace}:{function.filename}\n')

    def give(self, item, who=Player.EVERYONE, count=1):  # /give <who> <item> <count>
        item = item.to_give()
        open(self.location, 'a').write(f'give {who} {item} {str(count)}\n')

    def enable(self, trigger, who):  # /scoreboard players enable <who> <trigger>
        open(self.location, 'a').write(f'scoreboard players enable {who} {trigger}\n')

    def tellraw(self, who, text):  # /tellraw <who> <text>
        text = str(text).replace('\'', '"').replace('\n', '')
        open(self.location, 'a').write(f'tellraw {who} {text}\n')

    def title(self, who, title):  # /title <who> title <title>
        title = str(title).replace('\'', '"').replace('\n', '')
        open(self.location, 'a').write(f'title {who} title {title}\n')

    def subtitle(self, who, subtitle):  # /title <who> subtitle <subtitle>
        subtitle = str(subtitle).replace('\'', '"').replace('\n', '')
        open(self.location, 'a').write(f'title {who} subtitle {subtitle}\n')

    def actionbar(self, who, actionbar):  # /title <who> actionbar <actionbar>
        actionbar = str(actionbar).replace('\'', '"').replace('\n', '')
        open(self.location, 'a').write(f'title {who} actionbar {actionbar}\n')

    def clear(self, who, item=None):  # /clear <who> <?item?>
        open(self.location, 'a').write(f'clear {who}\n')

    # /title <who> times <fade_in> <stay> <fade_out>
    def times(self, who, fade_in, stay, fade_out):
        open(self.location, 'a').write(
            f'title {who} times {fade_in} {stay} {fade_out}\n')

    def reset(self, who):
        open(self.location, 'a').write(f'title {who} reset\n')

    def kill(self, who):  # /kill <who>
        open(self.location, 'a').write(f'kill {who}\n')

    def summon(self, entity, pos, nbt={}):  # /summon <entity> <pos> <nbt>
        nbtdata = '{'
        for i, key in enumerate(nbt):
            nbtdata += key + ':' + str(nbt.get(key))
            if type(nbt.get(key)) == int:
                nbtdata += 'b'
            if i != len(nbt)-1:
                nbtdata += ', '
        nbtdata += '}'
        open(self.location, 'a').write('summon ' +
                                       entity + ' ' + pos.to_str() + ' ' + nbtdata)

    def if_score(self, score, value):
        open(self.location, 'a').write(
            f'execute if score @s {score} matches {value} run ')


class Command:
    def say(text):  # /say <text>
        return f'say {text}'

    def give(item, who='@s', count=1):  # /give <who> <item> <count>
        return f'give {who} {item.to_give()} {str(count)}\n'

    def enable(trigger, who):  # /scoreboard players enable <who> <trigger>
        return f'scoreboard players enable {who} {trigger.name}\n'

    def tellraw(text, who):  # /tellraw <who> <text>
        text = str(text).replace('\'', '"').replace('\n', '')
        return f'tellraw {who} {text}\n'

    def kill(who):  # /kill <who>
        return f'kill {who}\n'

    def summon(entity, pos, nbt={}):  # /summon <entity> <pos> <nbt>
        nbtdata = '{'
        for i, key in enumerate(nbt):
            nbtdata += key + ':' + str(nbt.get(key))
            if type(nbt.get(key)) == int:
                nbtdata += 'b'
            if i != len(nbt)-1:
                nbtdata += ', '
        nbtdata += '}'
        return 'summon ' + entity + ' ' + pos.to_str() + ' ' + nbtdata

    def if_score(score, value):
        return f'execute if score @s {score} matches {value} run '


class Enchantments:
    def __init__(self, enchs_list):
        self.text = 'Enchantments:['
        for i, enchs in enumerate(enchs_list):
            for key in enchs:
                self.text += '{id:"' + key + \
                    '",lvl:' + str(enchs.get(key)) + "}"
            if i != len(enchs_list)-1:
                self.text += ','
        self.text += ']'

    def __repr__(self):
        return self.text


class Name:
    def __init__(self, style):
        self.text = "display:{Name:'"
        self.text += str(style).replace("'", '"')
        self.text += "'}"

    def __repr__(self):
        return self.text


class EntityTag:
    def __init__(self, entity):
        self.text = 'EntityTag:'
        self.text += str(entity)

    def __repr__(self):
        return self.text


class NoGravity:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'NoGravity:' + str(self.value) + 'b'


class Invisible:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'Invisible:' + str(self.value) + 'b'


class Marker:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'Marker:' + str(self.value) + 'b'


class Small:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'Small:' + str(self.value) + 'b'


class NoAI:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'NoAI:' + str(self.value) + 'b'


class RepairCost:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'RepairCost:' + str(self.value)


class Silent:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'Silent:' + str(self.value) + 'b'


class CustomNameVisible:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'CustomNameVisible:' + str(self.value) + 'b'


class EntityId:
    def __init__(self, entity):
        self.value = 'id:"' + entity + '"'

    def __repr__(self):
        return self.value


class HandItems:
    def __init__(self, items):
        self.text = 'HandItems:[{'
        for i, item in enumerate(items):
            if item != {}:
                self.text += to_nbt_item(item) + ''
            else:
                self.text += '{}'
            if i != len(items)-1:
                self.text += ',{'
        self.text += ']'

    def __repr__(self):
        return self.text


class HandDropChances:
    def __init__(self, left, right):
        self.text = 'HandDropChances:[' + \
            str(left) + 'f,' + str(right) + 'f' + ']'

    def __repr__(self):
        return self.text


class ArmorItems:
    def __init__(self, armor):
        self.text = 'ArmorItems:['
        for i, item in enumerate(armor):
            if item == {}:
                self.text += '{}'
            else:
                self.text += '{' + to_nbt_item(str(item))[:-1] + '}'
            if i != len(armor)-1:
                self.text += ','
        self.text += ']'

    def __repr__(self):
        return self.text


class CustomName:
    def __init__(self, style):
        self.text = "CustomName:'"
        self.text += str(style).replace("'", '"')
        self.text += "'"

    def __repr__(self):
        return self.text


class InGround:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'inGround:' + str(self.value) + 'b'


class Tags:
    def __init__(self, tags):
        self.text = 'Tags:['
        for i, tag in enumerate(tags):
            self.text += '"' + str(tag) + '"'
            if i != len(tags)-1:
                self.text += ','
        self.text += ']'
        self.tags = tags

    def normal(self):
        return self.text
    
    def to_nbt(self):
        self.result = ''
        for i, tag in enumerate(self.tags):
            self.result += 'tag=' + tag
            if i != len(self.tags)-1:
                self.result += ','
        return self.result


class Rotation:
    def __init__(self, x, z):
        self.text = 'Rotation:[' + str(x) + 'f,' + str(z) + 'f]'

    def __repr__(self):
        return self.text


class Unbreakable:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'Unbreakable:' + str(self.value) + 'b'


class CustomNBT:
    def __init__(self, nbt):
        self.text = ''
        self.nbt = nbt
        for i, key in enumerate(self.nbt):
            self.text += key + ':' + self.nbt.get(key)
            if i != len(self.nbt)-1:
                self.text += ','

    def __repr__(self):
        return self.text


class Item:
    def __init__(self, item, nbt=[], count=1):
        self.item = item
        self.text = ''
        self.nbt = nbt
        self.count = count

    def to_give(self):
        self.text = self.item + '{'
        for i, tag in enumerate(self.nbt):
            self.text += str(tag)
            if i != len(self.nbt)-1:
                self.text += ','
        self.text += '}'
        return self.text

    def to_entity(self):
        result = 'Item:{id:"minecraft:' + self.item + \
            '",Count:' + str(self.count) + "b"
        if self.nbt != []:
            result += ',tag:{'
            for i, nbt in enumerate(self.nbt):
                result += str(nbt)
                if i != len(self.nbt)-1:
                    result += ','
            result += '}'

        result += '}'
        print(result)
        return result

class BlockState:
    def __init__(self, blockstate):
        self.text = 'BlockState:{Name:"minecraft:'
        hascustomproperties = 0
        for i, nbt in enumerate(blockstate):
            if nbt == "Name":
                self.text += blockstate.get(nbt) + '"'
            else:
                if hascustomproperties == 0:
                    self.text += 'Properties:{'
                hascustomproperties = 1
                self.text += nbt + ':"' + blockstate.get(nbt) + '"'
            if i != len(blockstate)-1:
                self.text += ','
        
        if hascustomproperties:
            self.text += '}'
        self.text += '}'
    
    def __repr__(self):
        return self.text

class Entity:
    def __init__(self, entity, nbt=[]):
        self.entity = entity
        self.text = '@e[type=' + self.entity
        if nbt != []:
            self.text += ',nbt={'
        self.nbt = nbt
        for i, tag in enumerate(self.nbt):
            if type(tag) == Item:
                self.text += tag.to_entity()
            else:
                self.text += str(tag)

            if i != len(self.nbt)-1:
                self.text += ','

        if nbt != []:
            self.text += '}'
        self.text += ']'

    def __repr__(self):
        return self.text

class Scores:
    def __init__(self, scores):
        self.scores = scores
        self.text = 'scores={'
        for i, score in enumerate(self.scores):
            self.text += score + '=' + self.scores.get(score)
            if i != len(self.scores)-1:
                self.text += ','
        self.text += '}'

    def __repr__(self):
        return self.text

class CustomModelData:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'CustomModelData:' + str(self.value)

######################## RESOURCE PACKS ########################

class Resourcepack:
    def __init__(self, datapack, path, textures_location):
        self.datapack = datapack
        self.name = path.split('/')[-1]
        self.tloc = textures_location
        self.path = path
        self.windex = 101
        self.done_creating = 0
        self.writes = [

        ]
        try:
            os.mkdir(path)
        except:
            shutil.rmtree(path)
            os.mkdir(path)
        open(path + '/pack.mcmeta', 'w').writelines('''{
    "pack": {
        "pack_format": 9,
        "description": "Minecraft's Default Textures Packed for Texture Makers!"
    }
}''')
        os.mkdir(path + '/assets/')
        os.mkdir(path + '/assets/minecraft')
        os.mkdir(path + '/assets/minecraft/textures')
        os.mkdir(path + '/assets/minecraft/textures/block')
        os.mkdir(path + '/assets/minecraft/textures/item')
        os.mkdir(path + '/assets/minecraft/models')
        os.mkdir(path + '/assets/minecraft/models/item')
        os.mkdir(path + '/assets/minecraft/models/block')
    
    def replace_block_texture(self, block, texture):
        shutil.copyfile(self.tloc + "/" + texture, self.path + "/assets/minecraft/textures/block/" + block + ".png")
    
    def replace_item_texture(self, item, texture):
        shutil.copyfile(self.tloc + "/" + texture, self.path + "/assets/minecraft/textures/item/" + item + ".png")
    
    def add_custom_item(self, item_display_name, texture, replace_item, custom_model_data, create_trigger_for_item):
        self.item_display_name = item_display_name
        self.texture = texture
        self.replace_item = replace_item
        self.cmdata = custom_model_data
        self.hastrigger = create_trigger_for_item
        texture_json = self.path + "/assets/minecraft/models/item/" + texture.replace('.png', '.json')
        tickfunc = Function(self.datapack, 'tick')
        if self.hastrigger:
            self.datapack.add_trigger('give_' + self.texture.replace('.png', ''), Command.give(Item(replace_item, [
                'display:{Name:\'' + str(self.item_display_name).replace("'", '"') + '\'}',
                CustomModelData(self.cmdata)
            ]), MYSELF))
            tickfunc.enable("give_" + self.texture.replace('.png', ''), Player.EVERYONE)
        self.mjson = self.path + "/assets/minecraft/models/item/" + self.replace_item + ".json"

        shutil.copyfile(self.tloc + "/" + texture, self.path + "/assets/minecraft/textures/item/" + texture)
        open(texture_json, 'w').write(('{\n'
    '    "parent": "item/handheld",\n'
    '    "textures": {\n'
f'        "layer0": "item/' + texture.replace('.png', '') + '"\n'
    '    }\n'
    '}\n'))
        if self.replace_item not in self.writes:
            open(self.mjson, 'w').write(('{\n'
            '	"parent": "item/generated",\n'
            '	"textures": {\n'
            f'		"layer0": "item/{self.replace_item}"\n'
            '	},\n'
            '	\n'
            '	"overrides": [\n'
            '\t\t\n'
            '	]\n'
            '}\n'))

        content = open(self.mjson, 'r').read()
        open(self.mjson, 'w').write(content[:-6])

        no_png_texture = texture.replace('.png', '')
        text = '{"predicate": {"custom_model_data":' + str(self.cmdata) + '}, "model": "item/' + no_png_texture + '"}'

        already_been_in_file = 0
        if self.replace_item in self.writes:
            already_been_in_file = 1
        
        if already_been_in_file:
            text = ',\n\t\t' + text
        else:
            self.writes.append(self.replace_item)

        open(self.mjson, 'a').write(text + '\n\t]\n}\n')