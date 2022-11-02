import os, shutil
from mcultimate_vars import *

class Trigger:
    def __init__(self, datapack, name, on_trigger):
        self.datapack = datapack
        self.name = name
        self.on_trigger = on_trigger

class Pos:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return (self.x + ' ' + self.y + ' ' + self.z)

    def to_str(self):
        return (self.x + ' ' + self.y + ' ' + self.z)

class Scoreboard:
    datapack = 'd'
    def matches(values, result):
        global datapack
        for item in values:
            open(datapack.tickfunc, 'a').write(f'execute if score @s {item} matches {str(values.get(item))} run ')
        if type(result) == str:
            open(datapack.tickfunc, 'a').write(result + '\n')
        elif type(result) == Function:
            open(datapack.tickfunc, 'a').write(f'function {datapack.namespace}:{result.filename}\n')

    def __init__(self, datapack_arg, name, criteria):
        global datapack
        self.name = name
        self.criteria = criteria
        self.datapack = datapack_arg
        datapack = datapack_arg
        self.value = {}

    def set_score(self, who, value):
        open(self.datapack.tickfunc, 'a').write(f'scoreboard players set {who} {self.name} {str(value)}\n')

class Entity:
    ALLAY = 'allay'
    AREA_EFFECT_CLOUD = 'area_effect_cloud'
    ARMOR_STAND = 'armor_stand'
    ARROW = 'arrow'
    AXOLOTL = 'axolotl'
    BAT = 'bat'
    BEE = 'bee'
    BLAZE = 'blaze'
    BOAT = 'boat'
    CAT = 'cat'
    CAVE_SPIDER = 'cave_spider'
    CHEST_BOAT = 'chest_boat'
    CHEST_MINECART = 'chest_minecart'
    CHICKEN = 'chicken'
    COD = 'cod'
    COMMAND_BLOCK_MINECART = 'command_block_minecart'
    COW = 'cow'
    CREEPER = 'creeper'
    DOLPHIN = 'dolphin'
    DONKEY = 'donkey'
    DRAGON_FIREBALL = 'dragon_fireball'
    DROWNED = 'drowned'
    EGG = 'egg'
    ELDER_GUARDIAN = 'elder_guardian'
    END_CRYSTAL = 'end_crystal'
    ENDER_DRAGON = 'ender_dragon'
    ENDER_PEARL = 'ender_pearl'
    ENDERMAN = 'enderman'
    ENDERMITE = 'endermite'
    EVOKER = 'evoker'
    EVOKER_FANGS = 'evoker_fangs'
    EXPERIENCE_BOTTLE = 'experience_bottle'
    EXPERIENCE_ORB = 'experience_orb'
    EYE_OF_ENDER = 'eye_of_ender'
    FALLING_BLOCK = 'falling_block'
    FIREBALL = 'fireball'
    FIREWORK_ROCKET = 'firework_rocket'
    FOX = 'fox'
    FROG = 'frog'
    FURNACE_MINECART = 'furnace_minecart'
    GHAST = 'ghast'
    GIANT = 'giant'
    GLOW_ITEM_FRAME = 'glow_item_frame'
    GLOW_SQUID = 'glow_squid'
    GOAT = 'goat'
    GUARDIAN = 'guardian'
    HOGLIN = 'hoglin'
    HOPPER_MINECART = 'hopper_minecart'
    HORSE = 'horse'
    HUSK = 'husk'
    ILLUSIONER = 'illusioner'
    IRON_GOLEM = 'iron_golem'
    ITEM = 'item'
    ITEM_FRAME = 'item_frame'
    LEASH_KNOT = 'leash_knot'
    LIGHTNING_BOLT = 'lightning_bolt'
    LLAMA = 'llama'
    LLAMA_SPIT = 'llama_spit'
    MAGMA_CUBE = 'magma_cube'
    MARKER = 'marker'
    MINECART = 'minecart'
    MOOSHROOM = 'mooshroom'
    MULE = 'mule'
    OCELOT = 'ocelot'
    PAINTING = 'painting'
    PANDA = 'panda'
    PARROT = 'parrot'
    PHANTOM = 'phantom'
    PIG = 'pig'
    PIGLIN = 'piglin'
    PIGLIN_BRUTE = 'piglin_brute'
    PILLAGER = 'pillager'
    POLAR_BEAR = 'polar_bear'
    POTION = 'potion'
    PUFFERFISH = 'pufferfish'
    RABBIT = 'rabbit'
    RAVAGER = 'ravager'
    SALMON = 'salmon'
    SHEEP = 'sheep'
    SHULKER = 'shulker'
    SHULKER_BULLET = 'shulker_bullet'
    SILVERFISH = 'silverfish'
    SKELETON = 'skeleton'
    SKELETON_HORSE = 'skeleton_horse'
    SLIME = 'slime'
    SMALL_FIREBALL = 'small_fireball'
    SNOW_GOLEM = 'snow_golem'
    SNOWBALL = 'snowball'
    SPAWNER_MINECART = 'spawner_minecart'
    SPECTRAL_ARROW = 'spectral_arrow'
    SPIDER = 'spider'
    SQUID = 'squid'
    STRAY = 'stray'
    STRIDER = 'strider'
    TADPOLE = 'tadpole'
    TNT = 'tnt'
    TNT_MINECART = 'tnt_minecart'
    TRADER_LLAMA = 'trader_llama'
    TRIDENT = 'trident'
    TROPICAL_FISH = 'tropical_fish'
    TURTLE = 'turtle'
    VEX = 'vex'
    VILLAGER = 'villager'
    VINDICATOR = 'vindicator'
    WANDERING_TRADER = 'wandering_trader'
    WARDEN = 'warden'
    WITCH = 'witch'
    WITHER = 'wither'
    WITHER_SKELETON = 'wither_skeleton'
    WITHER_SKULL = 'wither_skull'
    WOLF = 'wolf'
    ZOGLIN = 'zoglin'
    ZOMBIE = 'zombie'
    ZOMBIE_HORSE = 'zombie_horse'
    ZOMBIE_VILLAGER = 'zombie_villager'
    ZOMBIFIED_PIGLIN = 'zombified_piglin'

class Player:
    EVERYONE      = '@a'
    EVERYBODY     = '@a'
    MYSELF        = '@s'
    SELF          = '@s'
    RANDOM        = '@r'
    ENTITIES      = '@e'
    ALL_ENTITIES  = '@e'
    NEAREST       = '@p'
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags

class ArmorItems:
    def __init__(self, head='air', chestplate='air', leggings='air', boots='air'):
        self.head = head
        self.chestplate = chestplate
        self.leggings = leggings
        self.boots = boots

    def to_nbt(self):
        return '[{id:"' + self.boots + '",Count:1b}, ' + '{id:"' + self.leggings + '",Count:1b}, '+ '{id:"' + self.chestplate + '",Count:1b}, '+ '{id:"' + self.head + '",Count:1b}]'

    def __repr__(self):
        return self.to_nbt()

class Datapack:
    def __init__(self, namespace, location_arg, desc=''):
        self.location = location_arg
        self.namespace = namespace
        self.desc = desc
        self.tickfunc = self.location + f'/data/{self.namespace}/functions/tick.mcfunction'
        self.loadfunc = self.location + f'/data/{self.namespace}/functions/load.mcfunction'
        try:
            os.mkdir(self.location)
        except FileExistsError:
            shutil.rmtree(self.location)
            os.mkdir(self.location)
        open(    self.location + '/pack.mcmeta', 'w').writelines('''{
    "pack": {
        "pack_format": 8,
        "description": ""
    }
}''')
        os.mkdir(self.location + '/data')
        os.mkdir(self.location + '/data/minecraft')
        os.mkdir(self.location + '/data/minecraft/tags')
        os.mkdir(self.location + '/data/minecraft/tags/functions')
        open(    self.location + '/data/minecraft/tags/functions/load.json', 'w').writelines((
            '{\n'
            '    "values": [\n'
            f'      "{self.namespace}:load"\n'
            '    ]\n'
            '}'
        ))
        open(    self.location + '/data/minecraft/tags/functions/tick.json', 'w').writelines((
            '{\n'
            '    "values": [\n'
            f'      "{self.namespace}:tick"\n'
            '    ]\n'
            '}'
        ))
        os.mkdir(self.location + f'/data/{self.namespace}')
        os.mkdir(self.location + f'/data/{self.namespace}/functions')
        self.function_num = 1

    def execute_as(self, who, func):
        open(self.location + f'/data/{self.namespace}/functions/{func.filename}.mcfunction', 'a').write(f'execute as {who} at @s run ')

    def add_scoreboard(self, object):
        object.datapack = self
        open(self.loadfunc, 'a').write(f'scoreboard objectives remove {object.name}\n')
        open(self.loadfunc, 'a').write(f'scoreboard objectives add {object.name} {object.criteria}\n')
        return object

    def add_trigger(self, name, on_trigger):
        open(self.location + f'/data/{self.namespace}/functions/load.mcfunction', 'a').write('scoreboard objectives add givedia trigger\n')
        open(self.location + f'/data/{self.namespace}/functions/tick.mcfunction', 'a').write(f'execute as @a at @s run execute if score @s {name} matches 1.. run function {self.namespace}:{on_trigger.filename}\n')
        open(self.location + f'/data/{self.namespace}/functions/tick.mcfunction', 'a').write(f'scoreboard players set @a {name} 0\n')
        return Trigger(self, name, on_trigger)

    def gamerule(self, rule, val):
        open(self.loadfunc, 'a').write(f'gamerule {rule} {str(val).lower()}\n')
        
class Function:
    def __init__(self, datapack, type='func'):
        self.location = ''
        self.filename = ''
        self.datapack = datapack
        if type in ['main', 'tick']:
            open(datapack.location + f'/data/{datapack.namespace}/functions/tick.mcfunction', 'w').write('')
            self.location = datapack.location + f'/data/{datapack.namespace}/functions/tick.mcfunction'
            self.filename = 'tick'

        if type == 'load':
            open(datapack.location + f'/data/{datapack.namespace}/functions/load.mcfunction', 'w').write('')
            self.location = datapack.location + f'/data/{datapack.namespace}/functions/load.mcfunction'
            self.filename = 'load'

        if type == 'func':
            open(datapack.location + f'/data/{datapack.namespace}/functions/function{str(datapack.function_num)}.mcfunction', 'w').write('')
            self.location = datapack.location + f'/data/{datapack.namespace}/functions/function{str(datapack.function_num)}.mcfunction'
            self.filename = f'function{str(datapack.function_num)}'
            datapack.function_num += 1

    def say(self, text): # /say <text>
        open(self.location, 'a').write(f'say {text}\n')
        return f'say {text}'

    def run(self, function): # /function <function>
        open(self.location, 'a').write(f'function {self.datapack.namespace}:{function.filename}\n')
        return f'function {self.datapack.namespace}:{function.filename}\n'

    def give(self, item, who='@s', count=1): # /give <who> <item> <count>
        open(self.location, 'a').write(f'give {who} {item} {str(count)}\n')
        return f'give {who} {item} {str(count)}\n'

    def enable(self, trigger, who): # /scoreboard players enable <who> <trigger>
        open(self.location, 'a').write(f'scoreboard players enable {who} {trigger.name}\n')
        return f'scoreboard players enable {who} {trigger.name}\n'

    def tellraw(self, text, who): # /tellraw <who> <text>
        text = str(text).replace('\'', '"').replace('\n', '')
        open(self.location, 'a').write(f'tellraw {who} {text}\n')
        return f'tellraw {who} {text}\n'

    def kill(self, who): # /kill <who>
        open(self.location, 'a').write(f'kill {who}\n')
        return f'kill {who}\n'

    def summon(self, entity, pos, nbt={}): # /summon <entity> <pos> <nbt>
        nbtdata = '{'
        for i, key in enumerate(nbt):
            nbtdata += key + ':' + str(nbt.get(key))
            if type(nbt.get(key)) == int:
                nbtdata += 'b'
            if i != len(nbt)-1:
                nbtdata += ', '
        nbtdata += '}'
        open(self.location, 'a').write('summon ' + entity + ' ' + pos.to_str() + ' ' + nbtdata)
        return 'summon ' + entity + ' ' + pos.to_str() + ' ' + nbtdata
    
    def if_score(score, value):
        open(self.location, 'a').write(f'execute if score @s {score} matches {value} run ')

class Command:
    def say(text): # /say <text>
        return f'say {text}'

    def give(item, who='@s', count=1): # /give <who> <item> <count>
        return f'give {who} {item} {str(count)}\n'

    def enable(trigger, who): # /scoreboard players enable <who> <trigger>
        return f'scoreboard players enable {who} {trigger.name}\n'

    def tellraw(text, who): # /tellraw <who> <text>
        text = str(text).replace('\'', '"').replace('\n', '')
        return f'tellraw {who} {text}\n'

    def kill(who): # /kill <who>
        return f'kill {who}\n'

    def summon(entity, pos, nbt={}): # /summon <entity> <pos> <nbt>
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
