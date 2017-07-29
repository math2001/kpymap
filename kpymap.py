# -*- encoding: utf-8 -*-

import json
import textwrap
try:
    import sublime
except ImportError:
    sublime = None
from os.path import join
from contextlib import contextmanager

__all__ = ['add', 'context', 'generate', 'reset']

INDENTATION = '  '

def dump(string, *args, **kwargs):
    return json.dumps(string, ensure_ascii=False, *args, **kwargs)

def output(*args, **kwargs):
    # used to by pass git hook
    # CSW: ignore
    print(*args, **kwargs)

class Context:

    def __init__(self, key, operator, operand, match_all):
        self.key = key
        self.operand = operand
        self.operator = 'equal' if operator is None else operator
        self.match_all = False if match_all is None else match_all

    def to_keymap(self):
        """converts to proper JSON for a .sublime-keymap"""
        string = '{"key": ' + dump(self.key)

        if self.operator != 'equal':
            string += ', "operator": ' + dump(self.operator)

        if self.operand is not True:
            string += ', "operand": ' + dump(self.operand)

        if self.match_all is not False:
            string += ', "match_all": ' + dump(self.match_all)

        return string + '}'

class Keybinding:

    def __init__(self, keys, command, args=None, context=None):
        self.keys = keys
        self.command = command
        self.args = args
        self.context = context

    def to_keymap(self):
        """converts to proper JSON for a .sublime-keymap"""
        string = '{\n'
        string += INDENTATION + '"keys": ' + dump(self.keys) + ',\n'
        string += INDENTATION + '"command": ' + dump(self.command)
        if self.args is not None:
            string += ',\n' + INDENTATION + '"args": ' + \
                textwrap.indent(dump(self.args, indent=INDENTATION), INDENTATION)[len(INDENTATION):]

        if self.context != []:
            string += ',\n' + INDENTATION + '"context": [\n'
            string += ',\n'.join([(INDENTATION * 2) + context.to_keymap() for context in self.context]) + '\n'
            string += INDENTATION + ']'

        return string + '\n}'

class Keymap:

    def __init__(self):
        self.keybindings = []
        self.context = []

    def add_context(self, key=None, operator=None, operand=None, match_all=None, context=None):
        if context is None:
            context = Context(key, operator, operand, match_all)
        elif key is not None or operand is not None or operator is not None or match_all is not None:
            raise ValueError('Tried to add context by passing an existing one but specified '
                             'arguments with it')
        elif operator is not None and operand is None:
            operator = operand
            operand = None

        self.context.append(context)
        return context

    def add_keybinding(self, keys=None, command=None, args=None, context=None, keybinding=None):
        if context is not None:
            context = self.context + [context]
        else:
            context = self.context + []

        if keybinding is None:
            keybinding = Keybinding(keys, command, args, context)
        elif keys is not None or command is not None or args is not None or context is not None:
            raise ValueError('Tried to add keybinding by passing an existing one but specified '
                             'arguments too')

        self.keybindings.append(keybinding)

    def remove_context(self, context):
        self.context.remove(context)

    def to_keymap(self):
        string = '[\n'
        string += textwrap.indent(',\n'.join(map(lambda c: c.to_keymap(), self.keybindings)), INDENTATION)
        string += '\n]'
        return string

keymap = Keymap()

# APIS functions

def reset():
    keymap.__init__()

def add(*args, **kwargs):
    keymap.add_keybinding(*args, **kwargs)

def generate():
    if sublime is None:
        # the file is build, not run by ST, so just output the JSON
        return output(keymap.to_keymap())

    keymap_file = join(sublime.packages_path(), 'User',
                       'Default ({}).sublime-keymap'.format(sublime.platform().title()))
    with open(keymap_file, 'w', encoding='utf-8') as fp:
        fp.write(keymap.to_keymap())
    output('Kpymap: wrote', keymap_file)

@contextmanager
def context(*args, **kwargs):
    actual_context = keymap.add_context(*args, **kwargs)
    yield
    keymap.remove_context(actual_context)

