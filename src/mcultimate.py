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


class ArmorItems:  # type: ignore
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
        self.rtickfunc = Function(self, 'tick')
        self.rloadfunc = Function(self, 'load')
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

    def gamerule(self, rule, val):
        open(self.loadfunc, 'a').write(f'gamerule {rule} {str(val).lower()}\n')
    
    def create_folder(self, name, path):
        os.mkdir(self.location + f'/data/{self.namespace}/functions/' + path + "/" + name)


class Function:
    def __init__(self, datapack, name, path=''):
        self.location = ''
        self.filename = name
        self.datapack = datapack
        self.location = datapack.location + f'/data/{self.datapack.namespace}/functions'
        self.base_location = ''
        if path != '':
            self.location += '/' + path + '/'
            self.base_location += path + '/'
        else:
            self.location += '/'
        self.location += f'{self.filename}.mcfunction'
        self.base_location += f'{self.filename}'
        open(f'{self.location}', 'w').write('')

    def fill(self, from_, to, block, replace=None):
        self.text = f'fill {from_} {to} {block}'
        if replace != None:
            self.text += ' replace ' + replace
        open(self.location, 'a').write(self.text + '\n')

    def function(self, func):
        open(self.location, 'a').write(
            f'function {self.datapack.namespace}:{func.base_location}\n')

    def add_trigger(self, name, on_trigger):
        open(self.datapack.loadfunc, 'a').write(
            f'scoreboard objectives add {name} trigger\n')
        open(self.location, 'a').write(
            f'execute as @a at @s run execute if score @s {name} matches 1.. run {on_trigger}')
        open(self.location, 'a').write(f'scoreboard players set @a {name} 0\n')

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
        open(self.location, 'a').write(
            f'scoreboard players enable {who} {trigger}\n')

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
        return f'give {who} {item.to_give()} {str(count)}\n'  # type: ignore

    def enable(trigger, who):  # /scoreboard players enable <who> <trigger>
        return f'scoreboard players enable {who} {trigger.name}\n'  # type: ignore

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
        return 'summon ' + entity + ' ' + pos.to_str() + ' ' + nbtdata  # type: ignore

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
    def __init__(self, nbts):
        self.text = 'EntityTag:{'
        for i, nbt in enumerate(nbts):
            if type(nbt) == Item:
                nbt = nbt.to_entity()
            if type(nbt) == Tags:
                nbt = nbt.normal()
            self.text += str(nbt)
            if i != len(nbts)-1:
                self.text += ','
        self.text += '}'

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
                self.text += to_nbt_item(item) + ''  # type: ignore
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
                self.text += '{' + to_nbt_item(str(item))[:-1] + '}'  # type: ignore
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
            if type(tag) == Tags:
                tag = tag.normal()
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

class Fixed:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'Fixed:' + str(self.value) + 'b'

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

class Motion:
    def __init__(self, mot):
        self.text = '['
        for i, item in enumerate(mot):
            self.text += str(item) + 'd'
            if i != len(mot)-1:
                self.text += ','
        self.text += ']'
        
    def __repr__(self):
        return 'Motion:' + self.text

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
        self.current_custom_block = 1
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
        shutil.copyfile(self.tloc + "/" + texture, self.path +
                        "/assets/minecraft/textures/block/" + block + ".png")

    def replace_item_texture(self, item, texture):
        shutil.copyfile(self.tloc + "/" + texture, self.path +
                        "/assets/minecraft/textures/item/" + item + ".png")
    
    def append_custom_model(self, filepath, text, in_writes):
        try:
            content = open(filepath, 'r').read()
        except FileNotFoundError:
            open(filepath, 'w').write(('{\n'
                                         '	"parent": "item/generated",\n'
                                         '	"textures": {\n'
                                         f'		"layer0": "item/{in_writes}"\n'
                                         '	},\n'
                                         '	\n'
                                         '	"overrides": [\n'
                                         '\t\t\n'
                                         '	]\n'
                                         '}\n'))
            content = open(filepath, 'r').read()
        open(filepath, 'w').write(content[:-6])

        already_been_in_file = 0
        if in_writes in self.writes:
            already_been_in_file = 1

        if already_been_in_file:
            text = ',\n\t\t' + text
        else:
            self.writes.append(in_writes)

        open(filepath, 'a').write(text + '\n\t]\n}\n')

    def add_custom_item(self, item_display_name, texture, replace_item, custom_model_data, create_trigger_for_item):
        no_png_texture = texture.replace('.png', '')
        texture_json = self.path + "/assets/minecraft/models/item/" + \
            texture.replace('.png', '.json')
        if create_trigger_for_item:
            give_item_trigger = Function(self.datapack, 'give_' + no_png_texture)
            self.datapack.rtickfunc.function(give_item_trigger)
            give_item_trigger.add_trigger('give_' + texture.replace('.png', ''), Command.give(Item(replace_item, [
                'display:{Name:\'' +
                str(item_display_name).replace("'", '"') + '\'}',
                CustomModelData(custom_model_data)
            ]), MYSELF))  # type: ignore
            self.datapack.rtickfunc.enable(
                "give_" + texture.replace('.png', ''), Player.EVERYONE)
        mjson = self.path + "/assets/minecraft/models/item/" + \
            replace_item + ".json"

        shutil.copyfile(self.tloc + "/" + texture, self.path +
                        "/assets/minecraft/textures/item/" + texture)
        open(texture_json, 'w').write(('{\n'
                                       '    "parent": "item/handheld",\n'
                                       '    "textures": {\n'
                                       f'        "layer0": "item/' + texture.replace('.png', '') + '"\n'
                                       '    }\n'
                                       '}\n'))
        text = '{"predicate": {"custom_model_data":' + \
            str(custom_model_data) + '}, "model": "item/' + no_png_texture + '"}'
        self.append_custom_model(mjson, text, replace_item)

    def add(self, what):
        return what

    def add_custom_gui(self, gui_layout):
        open_slots = []
        placeholder_slots = [i for i in range(27)]
        for slot in gui_layout:
            placeholder_slots.remove(slot.slot)
            open_slots.append(slot.slot)
        open(self.tickfunc, 'a').write()  # type: ignore

class InputSlot:
    def __init__(self, slot):
        self.slot = slot

class CustomBlock:
    def __init__(self, block_display_name, texture, base_block, create_trigger_for_block, datapack, resourcepack):
        self.datapack = datapack
        self.resourcepack = resourcepack
        self.no_png_texture = texture.replace('.png', '')
        self.datapack.create_folder(self.no_png_texture, "")
        self.place = Function(self.datapack, self.no_png_texture + '_place', self.no_png_texture)
        open(self.place.location, 'a').write(f'execute as @e[tag=init_custom_{self.no_png_texture}] at @s run setblock ~ ~ ~ {base_block}\n')
        open(self.place.location, 'a').write(f'tag @e[tag=init_custom_{self.no_png_texture}] add custom_{self.no_png_texture}\n')
        open(self.place.location, 'a').write(f'execute as @e[tag=custom_{self.no_png_texture}] at @s run execute unless block ~ ~ ~ air run tag @s remove init_custom_{self.no_png_texture}\n')
        open(self.place.location, 'a').write(f'execute as @e[tag=custom_{self.no_png_texture}] at @s run execute if block ~ ~ ~ air run function {self.datapack.namespace}:{self.no_png_texture}/{self.no_png_texture}_break\n')
        self.destroy = Function(self.datapack, self.no_png_texture + '_break', self.no_png_texture)
        open(self.destroy.location, 'a').write(f'execute as @e[tag=custom_{self.no_png_texture}] at @s run execute if block ~ ~ ~ air run kill @e[type=item,nbt=' + '{Item:{id:"minecraft:' + base_block + '"}},limit=1,distance=0..2,sort=nearest]\n')
        open(self.destroy.location, 'a').write(f'execute as @e[tag=custom_{self.no_png_texture}] at @s run execute if block ~ ~ ~ air run summon item ~ ~ ~ ' + '{' + Item(GLOW_ITEM_FRAME, ['display:{Name:\'' + str(block_display_name).replace("'", '"') + '\'}', CustomModelData(self.resourcepack.current_custom_block), EntityTag([ Item(GLOW_ITEM_FRAME, [ CustomModelData(self.resourcepack.current_custom_block) ]), Tags([ f'init_custom_{self.no_png_texture}' ]), Fixed(1) ]) ]).to_entity() + ',Motion:[0.07d, 0.2d, 0.1d]}\n')
        open(self.destroy.location, 'a').write(f'execute as @e[tag=custom_{self.no_png_texture}] at @s run execute if block ~ ~ ~ air run kill @s\n')
        self.datapack.rtickfunc.function(self.place)
        if create_trigger_for_block:
            self.place.add_trigger('give_' + self.no_png_texture, Command.
            give(Item(GLOW_ITEM_FRAME, [
                'display:{Name:\'' +
                str(block_display_name).replace("'", '"') + '\'}',
                CustomModelData(self.resourcepack.current_custom_block),
                EntityTag([
                    Item(GLOW_ITEM_FRAME, [
                        CustomModelData(self.resourcepack.current_custom_block)
                    ]),
                    Tags([
                        f'init_custom_{self.no_png_texture}'
                    ]),
                    Fixed(1)
                ])
            ]), MYSELF))  # type: ignore
            self.datapack.rtickfunc.enable(
                "give_" + self.no_png_texture, Player.EVERYONE)
        open(self.resourcepack.path + '/assets/minecraft/models/item/' + self.no_png_texture + '.json', 'w').write(('{\n'
'	"credit": "Made with MCUltimate",\n'
'	"textures": {\n'
f'		"0": "block/{self.no_png_texture}",\n'
f'		"particle": "block/{self.no_png_texture}"\n'
'	},\n'
'	"elements": [\n'
'		{\n'
'			"from": [0, 0, 0],\n'
'			"to": [16, 16, 16],\n'
'			"faces": {\n'
'				"north": {"uv": [0, 0, 16, 16], "texture": "#0"},\n'
'				"east": {"uv": [0, 0, 16, 16], "texture": "#0"},\n'
'				"south": {"uv": [0, 0, 16, 16], "texture": "#0"},\n'
'				"west": {"uv": [0, 0, 16, 16], "texture": "#0"},\n'
'				"up": {"uv": [0, 0, 16, 16], "texture": "#0"},\n'
'				"down": {"uv": [0, 0, 16, 16], "texture": "#0"}\n'
'			}\n'
'		}\n'
'	],\n'
'	"display": {\n'
'       "thirdperson_righthand": {\n'
'           "rotation": [-25, 0, -43.51],\n'
'           "translation": [0, 2.75, 0],\n'
'           "scale": [0.38, 0.38, 0.38]\n'
'       },\n'
'       "firstperson_righthand": {\n'
'           "rotation": [-2.9, 50.24, -2.92],\n'
'           "translation": [-0.75, 0.75, 2],\n'
'           "scale": [0.4, 0.4, 0.4]\n'
'       },\n'
'       "firstperson_lefthand": {\n'
'           "rotation": [-2.9, 50.24, -2.92],\n'
'           "translation": [-0.75, 0.75, 2],\n'
'           "scale": [0.4, 0.4, 0.4]\n'
'       },\n'
'       "gui": {\n'
'           "rotation": [24.25, -47, 0],\n'
'           "translation": [0, 0.25, 0],\n'
'           "scale": [0.67, 0.67, 0.67]\n'
'       },\n'
'       "ground": {\n'
'           "scale": [0.25, 0.25, 0.25],\n'
'           "translation": [0, 2.5, 0]\n'
'		},\n'
'       "head": {\n'
'			"scale": [0.801, 0.80295, 0.801]\n'
'		},\n'
'		"fixed": {\n'
'			"translation": [0, 0, -14],\n'
'			"scale": [2.001, 2.001, 2.001]\n'
'		}\n'
'	}\n'
'}'))
        shutil.copyfile(self.resourcepack.tloc + '/' + texture, self.resourcepack.path + '/assets/minecraft/textures/block/' + texture)
        if 'glow_item_frame' not in self.resourcepack.writes:
            open(self.resourcepack.path + '/assets/minecraft/models/item/glow_item_frame.json', 'w').write(('{\n'
                                         '	"parent": "item/generated",\n'
                                         '	"textures": {\n'
                                         f'		"layer0": "item/glow_item_frame"\n'
                                         '	},\n'
                                         '	\n'
                                         '	"overrides": [\n'
                                         '\t\t\n'
                                         '	]\n'
                                         '}\n'))
        self.resourcepack.append_custom_model(self.resourcepack.path + '/assets/minecraft/models/item/glow_item_frame.json', '{"predicate": {"custom_model_data":' + \
            str(self.resourcepack.current_custom_block) + '}, "model": "item/' + self.no_png_texture + '"}', 'glow_item_frame')
        self.resourcepack.writes.append('glow_item_frame')
        self.resourcepack.current_custom_block += 1
    
    def on_destroy(self, on_destroy):
        text = on_destroy + '\n'
        if type(on_destroy) == Function:
            text = f'function {self.datapack.namespace}:{on_destroy.base_location}\n'
        open(self.destroy.location, 'a').write(text)
    
    def on_place(self, on_place):
        text = f'execute as @e[tag=init_custom_{self.no_png_texture}] at @s run ' + on_place + '\n'
        if type(on_place) == Function:
            text += f'function {self.datapack.namespace}:{on_place.base_location}\n'
        content = open(self.place.location, 'r').read()
        open(self.place.location, 'w').write(text + content)