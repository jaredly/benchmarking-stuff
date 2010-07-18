#!/usr/bin/env python

import os
import css
import cssutils
import css_py.parse

local = lambda *parts: os.path.join(os.path.dirname(__file__), *parts)

text = open(local('data.css')).read()
# text = 'body{color:green;}'

import logging
log = logging.getLogger('silent')
log.setLevel(logging.CRITICAL)

functions = {
    'codetalker':(css.parseString, 88+20),
    'css_py':(css_py.parse.parse, 222+411),
    'cssutils':(cssutils.CSSParser(log=log).parseString, 185+204),
}

# vim: et sw=4 sts=4
