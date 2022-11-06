# MCUltimate
MCUltimate is a python libary for creating minecraft datapacks.

## Tips
When you are coding, the names of the variables **DO NOT MATTER!!!**
<details>
  <summary><strong>Getting started</strong></summary>
 
  This is the basic code you need to make a template datapack:
  ```python
  from mcultimate import *
  pack = Datapack('custom', './datapack') # create a datapack with the namespace custom and in the current directory with the folder name being 'datapack'
  ```
  
  To access your tick and load functions just type this:
  ```python
  from mcultimate import *
  datapack = Datapack('custom', './datapack')
  # you need to pass in the datapack variable, and the type of function it is (tick, load, func. See more in the documentation.)
  tick_func = Function(pack, 'tick') # creates the tick.mcfunction file
  load_func = Function(pack, 'load') # creates the load.mcfunction file
  ```
  If you want to say 'Reloaded!' in the color green when the datapack is done realoading it is as simple as typing this:
  ```python
  from mcultimate import *
  datapack = Datapack('custom', './datapack')
  load_func = Function(pack, 'load')
  load_func.tellraw(Player.EVERYONE, [{ # this code converts into tellraw @a [{"text":"Reloaded!", "color":"green"}]
	'text': 'Reloaded!',
	'color': Color.GREEN
  }])
  ```
  
</details>

<details><summary><strong>Cool Programs</strong></summary>
	
</details>

<details>

  <summary><strong>Scoreboards</strong></summary>
  
  Type this to make a scoreboard:
  ```python
  from mcultimate import *
  
  pack = Datapack('custom', './datapack')
  load = Function(pack, 'load')
  tick = Function(pack, 'tick')
  # create a scoreboard with the name jump_scoreboard and the criteria jump
  jump = Scoreboard('jump_scoreboard', 'minecraft.custom:minecraft.jump')
  Scoreboard.matches({ # if the jump score matches 1 do the following command on the next line
    'jump': 1'
  })
  tick.say('you just jumped!') # the tick.mcfunction file 'say hi'
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

  Scoreboard.matches({ # if the jump and sneak scores match 1 do the following command on the next line
    'jump': 1,
    'sneak': 1
  })

  tick.say('You just right clicked while sneaking!')
  # set everyones jump and sneak score to 0
  jump.set_score(Player.EVERYONE, 0)
  sneak.set_score(Player.EVERYONE, 0)
  ```
</details>

## Documentation
Classes
<details><summary><strong>Color</strong></summary>

#### Usage
```python
...

tick.tellraw(Player.EVERYONE, [{
	'text': 'This is the color yellow',
	'color': Color.YELLOW
}]
```
</details>
