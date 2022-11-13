import os
import shutil

from mcfuncs import *

######################## DATAPACKS ########################

datapack = None
resourcepack = None

class Scoreboard:
    '''
    Parameters:
        name (str): The name of the scoreboard
        criteria (str): The criteria of the scoreboard.

    Usage:
        right_click = Scoreboard('right_click', 'minecraft.used:minecraft.carrot_on_a_stick')

    Returns:
        None
    '''
    def __init__(self, name, criteria):
        self.json_name = name
        self.criteria = criteria

    def set_score(self, who, value):
        open(datapack.tickfunc, "a").write(
            f"scoreboard players set {who} {self.json_name} {str(value)}\n"
        )



class Color:
    '''
    Parameters:
        None

    Usage:
        load.tellraw(Player.EVERYONE, [{
            "text": "This is the color green or a RGB value",
            "color": Color.GREEN | Color.RGB(50, 100, 150)
        }])

    Returns:
        The RGB value in hex
    '''
    BLACK = "black"
    DARK_BLUE = "dark_blue"
    DARK_GREEN = "dark_green"
    DARK_AQUA = "dark_aqua"
    DARK_RED = "dark_red"
    DARK_PURPLE = "dark_purple"
    GOLD = "gold"
    GRAY = "gray"
    DARK_GRAY = "dark_gray"
    BLUE = "blue"
    GREEN = "green"
    AQUA = "aqua"
    RED = "red"
    LIGHT_PURPLE = "light_purple"
    PURPLE = "light_purple"
    YELLOW = "yellow"
    WHITE = "white"

    def RGB(red, green, blue):
        return "#{:02x}{:02x}{:02x}".format(red, green, blue)


class Player:
    '''
    Parameters:
        name (str): The name of the player.
        nbt (list): The nbt of the player

    Usage:
        load.tellraw(Player('RevolvingMadness', [Tags(["owner"])]), [{
            "text": "You are the owner!",
            "color": Color.DARK_RED
        }])

    Returns:
        None
    '''
    EVERYONE = "@a"
    MYSELF = "@s"
    SELF = "@s"
    RANDOM = "@r"
    ENTITIES = "@e"
    ALL_ENTITIES = "@e"
    NEAREST = "@p"
    player_types = ["@a", "@s", "@r", "@e", "@p"]

    def __init__(self, name, nbt):
        self.json_name = name
        self.nbt = nbt
        if name in Player.player_types:
            self.text = name + "["
        else:
            if nbt != []:
                self.text = "@a[name=" + name
                self.text += ","
        for i, val in enumerate(self.nbt):
            if type(val) == Tags:
                self.text += val.to_nbt()
            else:
                self.text += str(val)
            if i != len(self.nbt) - 1:
                self.text += ","
        self.text += "]"

    def __repr__(self):
        return self.text


class ArmorItems:  # type: ignore
    '''
    Parameters:
        head (str): The head item
        chestplate (str): The chestplate item
        leggings (str): The leggings item
        boots (str): The boots item

    Usage:
        func.summon(ARMOR_STAND, '~ ~ ~', [ArmorItems(
            Item(DIAMOND_HELMET),      heads item
            Item(AIR),                 chestplates item
            Item(CHAINMAIL_LEGGINGS),  leggings item
            Item(LEATHER_BOOTS)       boots item
        )])

    Returns:
        None
    '''
    def __init__(self, head="air", chestplate="air", leggings="air", boots="air"):
        self.head = head
        self.chestplate = chestplate
        self.leggings = leggings
        self.boots = boots

    def to_nbt(self):
        return (
            '[{id:"'
            + self.boots
            + '",Count:1b}, '
            + '{id:"'
            + self.leggings
            + '",Count:1b}, '
            + '{id:"'
            + self.chestplate
            + '",Count:1b}, '
            + '{id:"'
            + self.head
            + '",Count:1b}]'
        )

    def __repr__(self):
        return self.to_nbt()


class Block:
    def __init__(self, block, block_states):
        self.b = block
        self.b_states = block_states
        self.text = self.b + '['
        for i, state in enumerate(self.b_states):
            self.text += state.__repr__()
            if i != len(self.b_states)-1:
                self.text += ','
        self.text += ']'

    def __repr__(self):
        return self.text


class Datapack:
    def __init__(self, namespace, location):
        global datapack
        self.location = location
        datapack = self
        self.json_namespace = namespace.lower()
        self.custom_items = []
        self.namespace = namespace
        self.tickfunc = (
            self.location +
            f"/data/{self.json_namespace}/functions/tick.mcfunction"
        )
        self.loadfunc = (
            self.location +
            f"/data/{self.json_namespace}/functions/load.mcfunction"
        )
        try:
            os.mkdir(self.location)
        except FileExistsError:
            shutil.rmtree(self.location)
            os.mkdir(self.location)
        open(self.location + "/pack.mcmeta", "w").writelines(
            """{
    "pack": {
        "pack_format": 8,
        "description": ""
    }
}"""
        )
        os.mkdir(self.location + "/data")
        os.mkdir(self.location + "/data/minecraft")
        os.mkdir(self.location + "/data/minecraft/tags")
        os.mkdir(self.location + "/data/minecraft/tags/functions")
        open(
            self.location + "/data/minecraft/tags/functions/load.json", "w"
        ).writelines(
            (
                "{\n"
                '    "values": [\n'
                f'      "{self.json_namespace}:load"\n'
                "    ]\n"
                "}"
            )
        )
        open(
            self.location + "/data/minecraft/tags/functions/tick.json", "w"
        ).writelines(
            (
                "{\n"
                '    "values": [\n'
                f'      "{self.json_namespace}:tick"\n'
                "    ]\n"
                "}"
            )
        )
        os.mkdir(self.location + f"/data/{self.json_namespace}")
        os.mkdir(self.location + f"/data/{self.json_namespace}/functions")
        self.function_num = 1
        self.rtickfunc = Function("tick")
        self.rloadfunc = Function("load")

    def add_scoreboard(self, object):
        object.datapack = self
        open(self.loadfunc, "a").write(
            f"scoreboard objectives remove {object.name}\n")
        open(self.loadfunc, "a").write(
            f"scoreboard objectives add {object.name} {object.criteria}\n"
        )
        return object

    def gamerule(self, rule, val):
        open(self.loadfunc, "a").write(f"gamerule {rule} {str(val).lower()}\n")

    def create_folder(self, name, path):
        os.mkdir(
            self.location
            + f"/data/{self.json_namespace}/functions/"
            + path
            + "/"
            + name
        )


class Function:
    def __init__(self, name, path=""):
        self.location = ""
        self.filename = name

        self.location = datapack.location + \
            f"/data/{datapack.namespace}/functions"
        self.base_location = ""
        if path != "":
            self.location += "/" + path + "/"
            self.base_location += path + "/"
        else:
            self.location += "/"
        self.location += f"{self.filename}.mcfunction"
        self.base_location += f"{self.filename}"
        open(self.location, "w").write("")

    def matches(self, values, result):
        for item in values:
            open(self.location, "a").write(
                f"execute if score @s {item} matches {str(values.get(item))} run "
            )
        if type(result) == str:
            open(self.location, "a").write(result + "\n")
        elif type(result) == Function:
            open(self.location, "a").write(
                f"function {datapack.namespace}:{result.filename}\n"
            )


    def fill(self, from_, to, block, replace=None):
        self.text = f"fill {from_} {to} {block}"
        if replace != None:
            self.text += " replace " + replace
        open(self.location, "a").write(self.text + "\n")

    def schedule(self, function, time):
        open(self.location, "a").write(
            f'schedule function {datapack.namespace}:{function.filename} {time}')

    def setblock(self, where, block):
        self.text = f'setblock {where} {block}'
        open(self.location, "a").write(self.text + '\n')

    def if_block(self, where, block):
        open(self.location, "a").write(
            f'execute if block {where} {block} run ')
        return f'execute if block {where} {block} run'

    def function(self, func):
        return f"function {datapack.namespace}:{func.base_location}\n"

    def add_trigger(self, name, on_trigger):
        open(datapack.loadfunc, "a").write(
            f"scoreboard objectives add {name} trigger\n"
        )
        open(self.location, "a").write(
            f"execute as @a at @s run execute if score @s {name} matches 1.. run {on_trigger}"
        )
        open(self.location, "a").write(f"scoreboard players set @a {name} 0\n")

    def execute_as(self, who):
        open(self.location, "a").write(f"execute as {who} at @s run ")

    def say(self, text):  # /say <text>
        open(self.location, "a").write(f"say {text}\n")

    def run(self, function):  # /function <function>
        open(self.location, "a").write(
            f"function {datapack.namespace}:{function.filename}\n"
        )

    def give(self, item, who=Player.EVERYONE, count=1):  # /give <who> <item> <count>
        item = item.to_give()
        open(self.location, "a").write(f"give {who} {item} {str(count)}\n")

    def enable(self, trigger, who):  # /scoreboard players enable <who> <trigger>
        open(self.location, "a").write(
            f"scoreboard players enable {who} {trigger}\n")

    def tellraw(self, who, text):  # /tellraw <who> <text>
        text = str(text).replace("'", '"').replace("\n", "")
        open(self.location, "a").write(f"tellraw {who} {text}\n")

    def title(self, who, title):  # /title <who> title <title>
        title = str(title).replace("'", '"').replace("\n", "")
        open(self.location, "a").write(f"title {who} title {title}\n")

    def subtitle(self, who, subtitle):  # /title <who> subtitle <subtitle>
        subtitle = str(subtitle).replace("'", '"').replace("\n", "")
        open(self.location, "a").write(f"title {who} subtitle {subtitle}\n")

    def actionbar(self, who, actionbar):  # /title <who> actionbar <actionbar>
        actionbar = str(actionbar).replace("'", '"').replace("\n", "")
        open(self.location, "a").write(f"title {who} actionbar {actionbar}\n")

    def clear(self, who, item=None):  # /clear <who> <?item?>
        open(self.location, "a").write(f"clear {who}\n")

    # /title <who> times <fade_in> <stay> <fade_out>
    def times(self, who, fade_in, stay, fade_out):
        open(self.location, "a").write(
            f"title {who} times {fade_in} {stay} {fade_out}\n"
        )

    def reset(self, who):
        open(self.location, "a").write(f"title {who} reset\n")

    def kill(self, who):  # /kill <who>
        open(self.location, "a").write(f"kill {who}\n")

    def summon(self, entity, pos, nbt={}):  # /summon <entity> <pos> <nbt>
        nbtdata = "{"
        for i, key in enumerate(nbt):
            nbtdata += key + ":" + str(nbt.get(key))
            if type(nbt.get(key)) == int:
                nbtdata += "b"
            if i != len(nbt) - 1:
                nbtdata += ", "
        nbtdata += "}"
        open(self.location, "a").write(
            "summon " + entity + " " + pos.to_str() + " " + nbtdata
        )

    def if_score(self, score, value):
        open(self.location, "a").write(
            f"execute if score @s {score} matches {value} run "
        )


class Command:
    def say(text):  # /say <text>
        return f"say {text}"

    def give(item, who="@s", count=1):  # /give <who> <item> <count>
        return f"give {who} {item.to_give()} {str(count)}\n"  # type: ignore

    def enable(trigger, who):  # /scoreboard players enable <who> <trigger>
        # type: ignore
        return f"scoreboard players enable {who} {trigger.name}\n"

    def tellraw(text, who):  # /tellraw <who> <text>
        text = str(text).replace("'", '"').replace("\n", "")
        return f"tellraw {who} {text}\n"

    def kill(who):  # /kill <who>
        return f"kill {who}\n"

    def if_block(where, block):
        return f'execute if block {where} {block} run'

    def summon(entity, pos, nbt=[]):  # /summon <entity> <pos> <nbt>
        nbtdata = "{"
        for i, tag in enumerate(nbt):
            if type(tag) == Tags:
                tag = tag.normal()
            nbtdata += tag
            if i != len(nbt) - 1:
                nbtdata += ", "
        nbtdata += "}"
        return "summon " + entity + " " + pos + " " + nbtdata  # type: ignore

    def if_score(score, value):
        return f"execute if score @s {score} matches {value} run "


class Enchantments:
    def __init__(self, enchs_list):
        self.text = "Enchantments:["
        for i, enchs in enumerate(enchs_list):
            for key in enchs:
                self.text += '{id:"' + key + \
                    '",lvl:' + str(enchs.get(key)) + "}"
            if i != len(enchs_list) - 1:
                self.text += ","
        self.text += "]"

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
        self.text = "EntityTag:{"
        for i, nbt in enumerate(nbts):
            if type(nbt) == Item:
                nbt = nbt.to_entity()
            if type(nbt) == Tags:
                nbt = nbt.normal()
            self.text += str(nbt)
            if i != len(nbts) - 1:
                self.text += ","
        self.text += "}"

    def __repr__(self):
        return self.text


class NoGravity:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "NoGravity:" + str(self.value) + "b"


class Invisible:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Invisible:" + str(self.value) + "b"


class Marker:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Marker:" + str(self.value) + "b"


class Small:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Small:" + str(self.value) + "b"


class NoAI:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "NoAI:" + str(self.value) + "b"


class RepairCost:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "RepairCost:" + str(self.value)


class Silent:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Silent:" + str(self.value) + "b"


class CustomNameVisible:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "CustomNameVisible:" + str(self.value) + "b"


class EntityId:
    def __init__(self, entity):
        self.value = 'id:"' + entity + '"'

    def __repr__(self):
        return self.value


class HandItems:
    def __init__(self, items):
        self.text = "HandItems:[{"
        for i, item in enumerate(items):
            if item != {}:
                self.text += to_nbt_item(item) + ""  # type: ignore
            else:
                self.text += "{}"
            if i != len(items) - 1:
                self.text += ",{"
        self.text += "]"

    def __repr__(self):
        return self.text


class HandDropChances:
    def __init__(self, left, right):
        self.text = "HandDropChances:[" + \
            str(left) + "f," + str(right) + "f" + "]"

    def __repr__(self):
        return self.text


class ArmorItems:
    def __init__(self, armor):
        self.text = "ArmorItems:["
        for i, item in enumerate(armor):
            if item == {}:
                self.text += "{}"
            else:
                # type: ignore
                self.text += "{" + to_nbt_item(str(item))[:-1] + "}"
            if i != len(armor) - 1:
                self.text += ","
        self.text += "]"

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
        return "inGround:" + str(self.value) + "b"


class Tags:
    def __init__(self, tags):
        self.text = "Tags:["
        for i, tag in enumerate(tags):
            self.text += '"' + str(tag) + '"'
            if i != len(tags) - 1:
                self.text += ","
        self.text += "]"
        self.tags = tags

    def normal(self):
        return self.text

    def to_nbt(self):
        self.result = ""
        for i, tag in enumerate(self.tags):
            self.result += "tag=" + tag
            if i != len(self.tags) - 1:
                self.result += ","
        return self.result


class Rotation:
    def __init__(self, x, z):
        self.text = "Rotation:[" + str(x) + "f," + str(z) + "f]"

    def __repr__(self):
        return self.text


class Unbreakable:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Unbreakable:" + str(self.value) + "b"


class CustomNBT:
    def __init__(self, nbt):
        self.text = ""
        self.nbt = nbt
        for i, key in enumerate(self.nbt):
            self.text += key + ":" + self.nbt.get(key)
            if i != len(self.nbt) - 1:
                self.text += ","

    def __repr__(self):
        return self.text


class Item:
    def __init__(self, item, nbt=[], count=1):
        self.item = item
        self.text = ""
        self.nbt = nbt
        self.count = count

    def to_give(self):
        self.text = self.item + "{"
        for i, tag in enumerate(self.nbt):
            if type(tag) == Tags:
                tag = tag.normal()
            self.text += str(tag)
            if i != len(self.nbt) - 1:
                self.text += ","
        self.text += "}"
        return self.text

    def to_entity(self):
        result = 'Item:{id:"minecraft:' + self.item + \
            '",Count:' + str(self.count) + "b"
        if self.nbt != []:
            result += ",tag:{"
            for i, nbt in enumerate(self.nbt):
                result += str(nbt)
                if i != len(self.nbt) - 1:
                    result += ","
            result += "}"

        result += "}"
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
                    self.text += "Properties:{"
                hascustomproperties = 1
                self.text += nbt + ':"' + blockstate.get(nbt) + '"'
            if i != len(blockstate) - 1:
                self.text += ","

        if hascustomproperties:
            self.text += "}"
        self.text += "}"

    def __repr__(self):
        return self.text


class Entity:
    def __init__(self, entity, nbt=[]):
        self.entity = entity
        self.text = "@e[type=" + self.entity
        if nbt != []:
            self.text += ",nbt={"
        self.nbt = nbt
        for i, tag in enumerate(self.nbt):
            if type(tag) == Item:
                self.text += tag.to_entity()
            else:
                self.text += str(tag)

            if i != len(self.nbt) - 1:
                self.text += ","

        if nbt != []:
            self.text += "}"
        self.text += "]"

    def __repr__(self):
        return self.text


class Fixed:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Fixed:" + str(self.value) + "b"


class Scores:
    def __init__(self, scores):
        self.scores = scores
        self.text = "scores={"
        for i, score in enumerate(self.scores):
            self.text += score + "=" + self.scores.get(score)
            if i != len(self.scores) - 1:
                self.text += ","
        self.text += "}"

    def __repr__(self):
        return self.text


class Motion:
    def __init__(self, mot):
        self.text = "["
        for i, item in enumerate(mot):
            self.text += str(item) + "d"
            if i != len(mot) - 1:
                self.text += ","
        self.text += "]"

    def __repr__(self):
        return "Motion:" + self.text


class Age:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'age=' + str(self.value)


class CustomModelData:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "CustomModelData:" + str(self.value)


######################## RESOURCE PACKS ########################


class Resourcepack:
    def __init__(self, path, textures_location):
        global resourcepack

        resourcepack = self
        self.json_name = path.split("/")[-1]
        self.tloc = textures_location
        self.path = path
        self.windex = 101
        self.done_creating = 0
        self.current_custom_block = 1
        self.writes = []
        try:
            os.mkdir(path)
        except:
            shutil.rmtree(path)
            os.mkdir(path)
        open(path + "/pack.mcmeta", "w").writelines(
            """{
    "pack": {
        "pack_format": 9,
        "description": "Minecraft's Default Textures Packed for Texture Makers!"
    }
}"""
        )
        os.mkdir(path + "/assets/")
        os.mkdir(path + "/assets/minecraft")
        os.mkdir(path + "/assets/minecraft/textures")
        os.mkdir(path + "/assets/minecraft/textures/block")
        os.mkdir(path + "/assets/minecraft/textures/item")
        os.mkdir(path + "/assets/minecraft/models")
        os.mkdir(path + "/assets/minecraft/models/item")
        os.mkdir(path + "/assets/minecraft/models/block")

    def replace_block_texture(self, block, texture):
        shutil.copyfile(
            self.tloc + "/" + texture,
            self.path + "/assets/minecraft/textures/block/" + block + ".png",
        )

    def replace_item_texture(self, item, texture):
        shutil.copyfile(
            self.tloc + "/" + texture,
            self.path + "/assets/minecraft/textures/item/" + item + ".png",
        )

    def append_custom_model(self, filepath, text, in_writes):
        try:
            content = open(filepath, "r").read()
        except FileNotFoundError:
            open(filepath, "w").write(
                (
                    "{\n"
                    '	"parent": "item/generated",\n'
                    '	"textures": {\n'
                    f'		"layer0": "item/{in_writes}"\n'
                    "	},\n"
                    "	\n"
                    '	"overrides": [\n'
                    "\t\t\n"
                    "	]\n"
                    "}\n"
                )
            )
            content = open(filepath, "r").read()
        open(filepath, "w").write(content[:-6])

        already_been_in_file = 0
        if in_writes in self.writes:
            already_been_in_file = 1

        if already_been_in_file:
            text = ",\n\t\t" + text
        else:
            self.writes.append(in_writes)

        open(filepath, "a").write(text + "\n\t]\n}\n")

    def add(self, what):
        return what

    def add_custom_gui(self, gui_layout):
        open_slots = []
        placeholder_slots = [i for i in range(27)]
        for slot in gui_layout:
            placeholder_slots.remove(slot.slot)
            open_slots.append(slot.slot)
        open(self.tickfunc, "a").write()  # type: ignore


class CustomItem:
    def __init__(
        self,
        item_display_name,
        texture,
        replace_item,
        custom_model_data,
        create_trigger_for_item,
        datapack,
        resourcepack,
    ):

        no_png_texture = texture.replace(".png", "")
        texture_json = (
            resourcepack.path
            + "/assets/minecraft/models/item/"
            + texture.replace(".png", ".json")
        )
        if create_trigger_for_item:
            give_item_trigger = Function("give_" + no_png_texture)
            datapack.rtickfunc.function(give_item_trigger)
            give_item_trigger.add_trigger(
                "give_" + texture.replace(".png", ""),
                Command.give(
                    Item(
                        replace_item,
                        [
                            "display:{Name:'"
                            + str(item_display_name).replace("'", '"')
                            + "'}",
                            CustomModelData(custom_model_data),
                        ],
                    ),
                    MYSELF,
                ),
            )  # type: ignore
            datapack.rtickfunc.enable(
                "give_" + texture.replace(".png", ""), Player.EVERYONE
            )
        mjson = (
            resourcepack.path
            + "/assets/minecraft/models/item/"
            + replace_item
            + ".json"
        )

        shutil.copyfile(
            resourcepack.tloc + "/" + texture,
            resourcepack.path + "/assets/minecraft/textures/item/" + texture,
        )
        open(texture_json, "w").write(
            (
                "{\n"
                '    "parent": "item/handheld",\n'
                '    "textures": {\n'
                f'        "layer0": "item/' +
                texture.replace(".png", "") + '"\n'
                "    }\n"
                "}\n"
            )
        )
        text = (
            '{"predicate": {"custom_model_data":'
            + str(custom_model_data)
            + '}, "model": "item/'
            + no_png_texture
            + '"}'
        )
        resourcepack.append_custom_model(mjson, text, replace_item)


class CustomBlock:
    def __init__(
        self,
        block_display_name,
        texture,
        base_block,
        create_trigger_for_block
    ):

        self.block_display_name = block_display_name
        self.create_trigger_for_block = create_trigger_for_block
        self.texture = texture
        self.base_block = base_block
        self.json_name = get_json_item_name(block_display_name)
        datapack.create_folder(self.json_name, "")
        self.place = Function(self.json_name + "_place", self.json_name)
        self.destroy = Function(
            self.json_name + "_break", self.json_name
        )
        open(self.destroy.location, "a").write(
            f"execute as @e[tag=custom_{self.json_name}] at @s run execute if block ~ ~ ~ air run summon item ~ ~ ~ "
            + "{"
            + Item(
                GLOW_ITEM_FRAME,
                [
                    "display:{Name:'"
                    + str(self.block_display_name).replace("'", '"')
                    + "'}",
                    CustomModelData(resourcepack.current_custom_block),
                    EntityTag(
                        [
                            Silent(1),
                            Item(
                                GLOW_ITEM_FRAME,
                                [
                                    CustomModelData(
                                        resourcepack.current_custom_block
                                    )
                                ],
                            ),
                            Tags([f"init_custom_{self.json_name}"]),
                            Fixed(1),
                        ]
                    ),
                ],
            ).to_entity()
            + ",Motion:[0.07d, 0.2d, 0.1d]}\n"
        )
        open(self.place.location, "a").write(
            f"execute as @e[tag=init_custom_{self.json_name}] at @s run setblock ~ ~ ~ {self.base_block}\n"
        )
        open(self.place.location, "a").write(
            f"tag @e[tag=init_custom_{self.json_name}] add custom_{self.json_name}\n"
        )
        open(self.place.location, "a").write(
            f"execute as @e[tag=custom_{self.json_name}] at @s run execute unless block ~ ~ ~ air run tag @s remove init_custom_{self.json_name}\n"
        )
        open(self.place.location, "a").write(
            f"execute as @e[tag=custom_{self.json_name}] at @s run execute if block ~ ~ ~ air run function {datapack.namespace}:{self.json_name}/{self.json_name}_break\n"
        )
        open(self.destroy.location, "a").write(
            f"execute as @e[tag=custom_{self.json_name}] at @s run execute if block ~ ~ ~ air run kill @e[type=item,nbt="
            + '{Item:{id:"minecraft:'
            + self.base_block
            + '"}},limit=1,distance=0..2,sort=nearest]\n'
        )
        if type(texture) == SidedTextures:
            texture = texture.to_custom_block()
            open(
                resourcepack.path
                + "/assets/minecraft/models/item/"
                + get_json_item_name(block_display_name)
                + ".json",
                "w",
            ).write(texture)
            resourcepack.append_custom_model(
                resourcepack.path
                + "/assets/minecraft/models/item/glow_item_frame.json",
                '{"predicate": {"custom_model_data":'
                + str(resourcepack.current_custom_block)
                + '}, "model": "item/'
                + get_json_item_name(block_display_name)
                + '"}',
                "glow_item_frame",
            )
        elif type(texture) == CustomBlockModel:
            self.texture = texture.json
            self.no_json_texture = texture.json.replace(".json", "")
            self.json_texture()
        elif ".png" in texture:
            self.no_png_texture = texture.replace(".png", "")
            self.png_texture()

    def png_texture(self):
        open(self.destroy.location, "a").write(
            f"execute as @e[tag=custom_{self.json_name}] at @s run execute if block ~ ~ ~ air run kill @s\n"
        )
        datapack.rtickfunc.function(self.place)
        if self.create_trigger_for_block:
            self.place.add_trigger(
                "give_" + self.json_name,
                Command.give(
                    Item(
                        GLOW_ITEM_FRAME,
                        [
                            "display:{Name:'"
                            + str(self.block_display_name).replace("'", '"')
                            + "'}",
                            CustomModelData(resourcepack.current_custom_block),
                            EntityTag(
                                [
                                    Silent(1),
                                    Item(
                                        GLOW_ITEM_FRAME,
                                        [
                                            CustomModelData(
                                                resourcepack.current_custom_block
                                            )
                                        ],
                                    ),
                                    Tags([f"init_custom_{self.json_name}"]),
                                    Fixed(1),
                                ]
                            ),
                        ],
                    ),
                    MYSELF,
                ),
            )  # type: ignore
            datapack.rtickfunc.enable(
                "give_" + self.json_name, Player.EVERYONE)
        open(
            resourcepack.path
            + "/assets/minecraft/models/item/"
            + self.no_png_texture
            + ".json",
            "w",
        ).write(
            (
                "{\n"
                '	"credit": "Made with MCUltimate",\n'
                '	"textures": {\n'
                f'		"0": "block/{self.no_png_texture}",\n'
                f'		"particle": "block/{self.no_png_texture}"\n'
                "	},\n"
                '	"elements": [\n'
                "		{\n"
                '			"from": [0, 0, 0],\n'
                '			"to": [16, 16, 16],\n'
                '			"faces": {\n'
                '				"north": {"uv": [0, 0, 16, 16], "texture": "#0"},\n'
                '				"east": {"uv": [0, 0, 16, 16], "texture": "#0"},\n'
                '				"south": {"uv": [0, 0, 16, 16], "texture": "#0"},\n'
                '				"west": {"uv": [0, 0, 16, 16], "texture": "#0"},\n'
                '				"up": {"uv": [0, 0, 16, 16], "texture": "#0"},\n'
                '				"down": {"uv": [0, 0, 16, 16], "texture": "#0"}\n'
                "			}\n"
                "		}\n"
                "	],\n"
                '	"display": {\n'
                '       "thirdperson_righthand": {\n'
                '           "rotation": [-25, 0, -43.51],\n'
                '           "translation": [0, 2.75, 0],\n'
                '           "scale": [0.38, 0.38, 0.38]\n'
                "       },\n"
                '       "firstperson_righthand": {\n'
                '           "rotation": [-2.9, 50.24, -2.92],\n'
                '           "translation": [-0.75, 0.75, 2],\n'
                '           "scale": [0.4, 0.4, 0.4]\n'
                "       },\n"
                '       "firstperson_lefthand": {\n'
                '           "rotation": [-2.9, 50.24, -2.92],\n'
                '           "translation": [-0.75, 0.75, 2],\n'
                '           "scale": [0.4, 0.4, 0.4]\n'
                "       },\n"
                '       "gui": {\n'
                '           "rotation": [24.25, -47, 0],\n'
                '           "translation": [0, 0.25, 0],\n'
                '           "scale": [0.67, 0.67, 0.67]\n'
                "       },\n"
                '       "ground": {\n'
                '           "scale": [0.25, 0.25, 0.25],\n'
                '           "translation": [0, 2.5, 0]\n'
                "		},\n"
                '       "head": {\n'
                '			"scale": [0.801, 0.80295, 0.801]\n'
                "		},\n"
                '		"fixed": {\n'
                '			"translation": [0, 0, -14],\n'
                '			"scale": [2.001, 2.001, 2.001]\n'
                "		}\n"
                "	}\n"
                "}"
            )
        )
        shutil.copyfile(
            resourcepack.tloc + "/" + self.texture,
            resourcepack.path + "/assets/minecraft/textures/block/" + self.texture,
        )
        if "glow_item_frame" not in resourcepack.writes:
            open(
                resourcepack.path
                + "/assets/minecraft/models/item/glow_item_frame.json",
                "w",
            ).write(
                (
                    "{\n"
                    '	"parent": "item/generated",\n'
                    '	"textures": {\n'
                    f'		"layer0": "item/glow_item_frame"\n'
                    "	},\n"
                    "	\n"
                    '	"overrides": [\n'
                    "\t\t\n"
                    "	]\n"
                    "}\n"
                )
            )
        resourcepack.append_custom_model(
            resourcepack.path
            + "/assets/minecraft/models/item/glow_item_frame.json",
            '{"predicate": {"custom_model_data":'
            + str(resourcepack.current_custom_block)
            + '}, "model": "item/'
            + self.no_png_texture
            + '"}',
            "glow_item_frame",
        )
        resourcepack.writes.append("glow_item_frame")
        resourcepack.current_custom_block += 1

    def json_texture(self):
        open(self.destroy.location, "a").write(
            f"execute as @e[tag=custom_{self.json_name}] at @s run execute if block ~ ~ ~ air run kill @s\n"
        )
        datapack.rtickfunc.function(self.place)
        if self.create_trigger_for_block:
            self.place.add_trigger(
                "give_" + self.json_name,
                Command.give(
                    Item(
                        GLOW_ITEM_FRAME,
                        [
                            "display:{Name:'"
                            + str(self.block_display_name).replace("'", '"')
                            + "'}",
                            CustomModelData(resourcepack.current_custom_block),
                            EntityTag(
                                [
                                    Silent(1),
                                    Item(
                                        GLOW_ITEM_FRAME,
                                        [
                                            CustomModelData(
                                                resourcepack.current_custom_block
                                            )
                                        ],
                                    ),
                                    Tags(
                                        [f"init_custom_{self.no_json_texture}"]),
                                    Fixed(1),
                                ]
                            ),
                        ],
                    ),
                    MYSELF,
                ),
            )  # type: ignore
            datapack.rtickfunc.enable(
                "give_" + self.json_name, Player.EVERYONE)
        shutil.copyfile(
            resourcepack.tloc + "/" + self.texture,
            resourcepack.path + "/assets/minecraft/models/item/" + self.texture,
        )
        if "glow_item_frame" not in resourcepack.writes:
            open(
                resourcepack.path
                + "/assets/minecraft/models/item/glow_item_frame.json",
                "w",
            ).write(
                (
                    "{\n"
                    '	"parent": "item/generated",\n'
                    '	"textures": {\n'
                    f'		"layer0": "item/glow_item_frame"\n'
                    "	},\n"
                    "	\n"
                    '	"overrides": [\n'
                    "\t\t\n"
                    "	]\n"
                    "}\n"
                )
            )
        resourcepack.append_custom_model(
            resourcepack.path
            + "/assets/minecraft/models/item/glow_item_frame.json",
            '{"predicate": {"custom_model_data":'
            + str(resourcepack.current_custom_block)
            + '}, "model": "item/'
            + self.no_json_texture
            + '"}',
            "glow_item_frame",
        )
        resourcepack.writes.append("glow_item_frame")
        resourcepack.current_custom_block += 1

    def on_destroy(self, on_destroy):
        text = on_destroy + "\n"
        if type(on_destroy) == Function:
            text = f"function {datapack.namespace}:{on_destroy.base_location}\n"
        open(self.destroy.location, "a").write(text)

    def on_place(self, on_place):
        text = f"execute as @e[tag=init_custom_{self.no_json_texture}] at @s run "
        if type(on_place) == Function:
            text += f"function {datapack.namespace}:{on_place.base_location}\n"
        else:
            text += on_place
        text += '\n'
        content = open(self.place.location, "r").read()
        open(self.place.location, "w").write(text + content)


class SidedTextures:
    def __init__(self, top, bottom, left, right, front, back):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.front = front
        self.back = back

    def to_custom_block(self):
        no_png_top = self.top.replace(".png", "")
        no_png_bottom = self.bottom.replace(".png", "")
        no_png_left = self.left.replace(".png", "")
        no_png_right = self.right.replace(".png", "")
        no_png_front = self.front.replace(".png", "")
        no_png_back = self.back.replace(".png", "")
        shutil.copyfile(
            resourcepack.tloc + "/" + self.top,
            resourcepack.path + "/assets/minecraft/textures/block/" + self.top,
        )
        shutil.copyfile(
            resourcepack.tloc + "/" + self.bottom,
            resourcepack.path + "/assets/minecraft/textures/block/" + self.bottom,
        )
        shutil.copyfile(
            resourcepack.tloc + "/" + self.left,
            resourcepack.path + "/assets/minecraft/textures/block/" + self.left,
        )
        shutil.copyfile(
            resourcepack.tloc + "/" + self.right,
            resourcepack.path + "/assets/minecraft/textures/block/" + self.right,
        )
        shutil.copyfile(
            resourcepack.tloc + "/" + self.front,
            resourcepack.path + "/assets/minecraft/textures/block/" + self.front,
        )
        shutil.copyfile(
            resourcepack.tloc + "/" + self.back,
            resourcepack.path + "/assets/minecraft/textures/block/" + self.back,
        )

        text = (
            "{\n"
            '	"credit": "Made with MCUltimate",\n'
            '	"textures": {\n'
            f'		"0": "block/{no_png_bottom}",\n'
            f'		"1": "block/{no_png_front}",\n'
            f'		"2": "block/{no_png_top}",\n'
            f'		"3": "block/{no_png_right}",\n'
            f'       "4": "block/{no_png_left}",\n'
            f'       "5": "block/{no_png_back}",\n'
            f'		"particle": "block/{no_png_bottom}"\n'
            "	},\n"
            '	"elements": [\n'
            "		{\n"
            '			"from": [0, 0, 0],\n'
            '			"to": [16, 16, 16],\n'
            '			"faces": {\n'
            '				"north": {"uv": [0, 0, 16, 16], "texture": "#3"},\n'
            '				"east": {"uv": [0, 0, 16, 16], "texture": "#1"},\n'
            '				"south": {"uv": [0, 0, 16, 16], "texture": "#4"},\n'
            '				"west": {"uv": [0, 0, 16, 16], "texture": "#5"},\n'
            '				"up": {"uv": [0, 0, 16, 16], "texture": "#2"},\n'
            '				"down": {"uv": [0, 0, 16, 16], "texture": "#0"}\n'
            "			}\n"
            "		}\n"
            "	],\n"
            '	"display": {\n'
            '       "thirdperson_righthand": {\n'
            '           "rotation": [-25, 0, -43.51],\n'
            '           "translation": [0, 2.75, 0],\n'
            '           "scale": [0.38, 0.38, 0.38]\n'
            "       },\n"
            '       "firstperson_righthand": {\n'
            '           "rotation": [-2.9, 50.24, -2.92],\n'
            '           "translation": [-0.75, 0.75, 2],\n'
            '           "scale": [0.4, 0.4, 0.4]\n'
            "       },\n"
            '       "firstperson_lefthand": {\n'
            '           "rotation": [-2.9, 50.24, -2.92],\n'
            '           "translation": [-0.75, 0.75, 2],\n'
            '           "scale": [0.4, 0.4, 0.4]\n'
            "       },\n"
            '       "gui": {\n'
            '           "rotation": [24.25, -47, 0],\n'
            '           "translation": [0, 0.25, 0],\n'
            '           "scale": [0.67, 0.67, 0.67]\n'
            "       },\n"
            '       "ground": {\n'
            '           "scale": [0.25, 0.25, 0.25],\n'
            '           "translation": [0, 2.5, 0]\n'
            "		},\n"
            '       "head": {\n'
            '			"scale": [0.801, 0.80295, 0.801]\n'
            "		},\n"
            '		"fixed": {\n'
            '			"translation": [0, 0, -14],\n'
            '			"scale": [2.001, 2.001, 2.001]\n'
            "		}\n"
            "	}\n"
            "}"
        )

        return text


class CustomBlockModel:
    def __init__(self, json, textures):
        self.json = json
        for texture in textures:
            shutil.copy(resourcepack.tloc + '/' + texture, resourcepack.path +
                        '/assets/minecraft/textures/block/' + texture)

    def __repr__(self):
        return self.json
