from mcultimate import *
from datetime import datetime
start = datetime.now()






main = Datapack('custom', './custom_datapack')
load = Function(main, 'load')
tick = Function(main, 'tick')
load.tellraw([
    {"text": "Reloaded!"}
], '@a')


sneak_and_right_click = Function(main, 'func')
sneak_and_right_click.say('You sneaked and right clicked')



click = main.add_scoreboard(Scoreboard(main, 'click', 'minecraft.used:minecraft.carrot_on_a_stick'))
sneak = main.add_scoreboard(Scoreboard(main, 'sneak', 'minecraft.custom:minecraft.sneak_time'))
jump = main.add_scoreboard(Scoreboard(main, 'jump', 'minecraft.custom:minecraft.jump'))
main.execute_as('@a', tick)
Scoreboard.matches({
    'click': 1,
    'sneak': 3,
    'jump': 5
}, sneak_and_right_click)
# execute as @a at @s run execute if score @s click matches 1 run execute if score @s sneak matches 1 run function...
click.set_score(Player.EVERYONE, 0)
sneak.set_score(Player.EVERYONE, 0)
jump.set_score(Player.EVERYONE, 0)





end = datetime.now()
td = (end - start).total_seconds() * 10**3
print(f"Conversion Time: {td:.03f}ms")