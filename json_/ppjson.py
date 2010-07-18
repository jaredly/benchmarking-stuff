#!/usr/bin/env python

# http://www.ptmcg.com/geo/python/confs/TxUnconf2008Pyparsing.html

import json
from pyparsing import *

TRUE = Keyword("true")
FALSE = Keyword("false")
NULL = Keyword("null")

jsonString = dblQuotedString.setParseAction( removeQuotes )
jsonNumber = Combine( Optional('-') + ( '0' | Word('123456789',nums) ) +
                    Optional( '.' + Word(nums) ) +
                    Optional( Word('eE',exact=1) + Word(nums+'+-',nums) ) )


jsonObject = Forward()
jsonValue = Forward()
jsonElements = delimitedList( jsonValue )
jsonArray = Group( Suppress('[') + jsonElements + Suppress(']') )
jsonValue << ( jsonString | jsonNumber | jsonObject  |
               jsonArray | TRUE | FALSE | NULL )
memberDef = Group( jsonString + Suppress(':') + jsonValue )
jsonMembers = delimitedList( memberDef )
jsonObject << Dict( Suppress('{') + jsonMembers + Suppress('}') )
def _dict(s,l,toks):
    res = {}
    for k,v in toks:
        if type(v)==tuple:v = list(v)
        res[k] = v
    return res
jsonObject.setParseAction( _dict )
def _list(s,l,toks):
    return tuple(toks[0])
jsonArray.setParseAction( _list )

jsonComment = cppStyleComment
jsonObject.ignore( jsonComment )

TRUE.setParseAction( replaceWith(True) )
FALSE.setParseAction( replaceWith(False) )
NULL.setParseAction( replaceWith(None) )

jsonString.setParseAction( removeQuotes )

def convertNumbers(s,l,toks):
    n = toks[0]
    try:
        return int(n)
    except ValueError, ve:
        return float(n)

jsonNumber.setParseAction( convertNumbers )

def loads(text):
    return jsonObject.parseString(text)[0]

# loads = jsonObject.parseString


# vim: et sw=4 sts=4
