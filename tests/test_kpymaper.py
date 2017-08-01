# -*- encoding: utf-8 -*-
import difflib
import sys
import os.path as path

sys.path.insert(0, path.dirname(path.dirname(path.dirname(__file__))))

def output(*args, **kwargs):
    # used to by pass git hook
    # CSW: ignore
    print(*args, **kwargs)

from kpymap import *
reset()


# ----------------------------------------

add('ctrl+a', 'command')

add('ctrl+b', 'command', {'arg': 'value'})
add('ctrl+e', 'command', {'arg1': 'value1', 'arg2': 'value2'})

add('alt+c', 'command', {'arg1': 'value1', 'arg2': 'value2'}, get_context('key', 'operand', match_all=True))
add('ctrl+u', 'command', {'arg1': 'value1', 'arg2': 'value2'}, get_context('key', 'operator', 'operand', False))
add('ctrl+t', 'command', {'arg1': 'value1', 'arg2': 'value2'}, get_context('key', 'operand', match_all=True), get_context('keyalone'))

add('ctrl+alt+b', 'e' 'command', {'arg': 'value'})
add('ctrl+b', 'c', 'command', {'arg1': 'value1', 'arg2': 'value2'})
add('ctrl+c', 'alt+h', 'command', get_context('key', 'operand'))
add('ctrl+b', 'c', 'command', {'arg1': 'value1', 'arg2': 'value2'}, get_context('key', 'operand'))

with context('key', 'operator', 'operand', False):
    add(':', ')', 'command', get_context('key1', 'operand'))
    add('alt+r', 'command', get_context('key2', 'operand'), get_context('key3', 'operand'))

context1 = get_context('python', 'is', 'awesome')

with context(context1):
    add('whatever', 'command', context1)
    add('whatever2', 'command2', get_context('python', 'is', 'awesome'))
    add('hello', 'world', get_context('key2', 'hey!'))

# ----------------------------------------

keymaped_generated = generate(return_json=True)
with open('expected-result.json', encoding='utf-8') as fp:
    expected_result = fp.read()
    if expected_result != keymaped_generated:
        # CSW: ignore
        output("Test failed.")
        output("------------")
        output(''.join(difflib.context_diff(expected_result.splitlines(True),
                                            keymaped_generated.splitlines(True),
                                            fromfile='Python',
                                            tofile='expected-result.json')))
    else:
        output("Yeah!! Everything is still working!")