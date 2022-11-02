# MCUltimate
MCUltimate is a python libary for creating minecraft datapacks.

Type this to make a scoreboard:
```python
from mcultimate import *

# create a scoreboard with the name jump_scoreboard and the criteria jump
jump = Scoreboard('jump_scoreboard', 'minecraft.custom:minecraft.jump')
Scoreboard.matches({ # if the jump score matches 1 do the following command on the next line
  'jump': 1'
})
tick.say('hi') # the tick.mcfunction file 'say hi'
# set everyones jump score to 0
jump.set_score(Player.EVERYONE, 0)
```

To check if multiple scores match you can type this:
```python
from mcultimate import *

# create a scoreboard with the name jump_scoreboard and the criteria jump
jump = Scoreboard('jump_scoreboard', 'minecraft.custom:minecraft.jump')
# create a scoreboard with the name sneak_scoreboard and the criteria sneak_time
sneak = Scoreboard('sneak_scoreboard', 'minecraft.custom:minecraft.sneak_time')

Scoreboard.matches({
  'jump': 1,
  'sneak': 1
})

tick.say('You just right clicked while sneaking!')
# set everyones jump and sneak score to 0
jump.set_score(Player.EVERYONE, 0)
sneak.set_score(Player.EVERYONE, 0)
```
