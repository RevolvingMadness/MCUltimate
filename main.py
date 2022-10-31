from mcultimate import *
from datetime import datetime
start = datetime.now()






main = Datapack('custom', 'C:/Users/andya/AppData/Roaming/.minecraft/saves/The Testolator/datapacks/custom_datapack')
load = Function(main, 'load')
tick = Function(main, 'tick')
load.tellraw([
    {"text": "Reloaded!"}
], '@a')


sneak_and_right_click = Function(main, 'func')
sneak_and_right_click.say('You sneaked and right clicked')



click = main.add_scoreboard(Scoreboard(main, 'click', 'minecraft.used:minecraft.carrot_on_a_stick'))
sneak = main.add_scoreboard(Scoreboard(main, 'sneak', 'minecraft.custom:minecraft.sneak_time'))
main.execute_as('@a', tick)
click.matches(1, sneak.matches(1, sneak_and_right_click))
# execute as @a at @s run execute if score @s click matches 1 run execute if score @s sneak matches 1 run function...
main.execute_as('@a', tick)
click.set_score(Player.EVERYONE, 0)
main.execute_as('@a', tick)
sneak.set_score(Player.EVERYONE, 0)





end = datetime.now()
td = (end - start).total_seconds() * 10**3
print(f"Conversion Time: {td:.03f}ms")