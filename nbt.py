# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = r"""
	['|"](\d{0,}b)['|"]|(False|True)
	"""

test_str = {
    'display': {
        'Name': {
            "text": "Iron Golem Spawn Egg",
            "italic": False
        },
        'EntityTag': {
            'id': "minecraft:iron_golem",
            'Invulnerable': '1b',
            'Glowing': '1b'
        }
}}

# 1.  ['|"](\d{0,}b)['|"]|(False|True)  &&  \L$2$1

# 2.  ["|']([^text|italic|id].*)["|']:(\s[^{])  &&  $1:$2

# 3.  "([display|Name]*)"  &&  $1