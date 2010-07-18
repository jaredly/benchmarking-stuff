#!/usr/bin/env python

from lepl import *
from lepl.support.lib import str


def Simple():
    '''
    A simple JSON parser.
    '''
    
    escapes = {'\\b': '\b', '\\f': '\f', '\\n': '\n', '\\t': '\t', '\\r': '\r'}
    
    def unescape_string(text):
        return escapes[text]
    
    def unescape_unicode(text):
        return bytes(str(text), 'utf8').decode('unicode_escape')
    
    value          = Delayed()

    unicode_escape = ("\\u" + Digit()[4, ...])   >> unescape_unicode
    regular_escape = ("\\" + Any("bfntr"))       >> unescape_string
    escape         = (unicode_escape | regular_escape)
    string         = (Drop('"') & (AnyBut('"\\') | escape)[...] & Drop('"'))
    
    number         = Float() >> float
    
    comma          = Drop(',')
    
    with DroppedSpace():
        array          = Drop("[") & value[:, comma] & Drop("]")  > list
    
        pair           = string & Drop(":") & value               > tuple
        object_        = Drop("{") & pair[:, comma] & Drop("}")   > dict
    
    
    value += ((Literal('true')  >= (lambda x: True)) |
              (Literal('false') >= (lambda x: False)) |
              (Literal('null')  >= (lambda x: None)) |
              array | object_ | number | string)

    return value


# vim: et sw=4 sts=4
