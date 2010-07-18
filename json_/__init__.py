#!/usr/bin/env python

import os
import ppjson
from codetalker.contrib import json
# import jsonply
import lepl_json


local = lambda *parts: os.path.join(os.path.dirname(__file__), *parts)

text = open(local('large_doc.json')).read()
text = '{"man":3}'

functions = {
    'pyparsing': (ppjson.loads, 57),
    'codetalker': (json.loads, 66),
    # 'ply': (jsonply.loads, 465),
    'lepl': (lepl_json.Simple().get_parse_string(), 45),
}

# vim: et sw=4 sts=4
