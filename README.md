# MCUltimate
MCUltimate is a python libary for creating minecraft datapacks.

Type this to make a scoreboard:
```python
from mcultimate import *

jump = Scoreboard('jump_scoreboard', 'minecraft.custom:minecraft.jump') # create a scoreboard with the name jump_scoreboard and the criteria jump
Scoreboard.matches({ # if the jump score matches 1 do the following command on the next line
  'jump': 1'
})
tick.say('hi') # the tick.mcfunction file 'say hi'
Scoreobard.set_score(Player.EVERYONE, 0)
```
