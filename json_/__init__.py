#!/usr/bin/env python
import fpl_json
fpl_json.loads('{"man": 3}')

import os
import ppjson
from codetalker.contrib import json as ctjson
import json
import jsonply
import demjson
import cjson
from lepl.contrib import json as lepl_json

local = lambda *parts: os.path.join(os.path.dirname(__file__), *parts)


text = open(local('large_doc.json')).read()
# text = '{"man": 3}\n'.decode('utf-8')

functions = {
    'pyparsing': (ppjson.loads, 57),
    'codetalker': (ctjson.loads, 66),
    'stdlib.json': (json.loads, 1147),
    'funcparserlib': (fpl_json.loads, 127),
    'ply': (jsonply.parse, 465),
    'demjson': (demjson.decode, 2138),
    'cjson': (cjson.decode, 123),
    # 'lepl': (lepl_json.Simple().get_parse_string(), 45),
}

# vim: et sw=4 sts=4
