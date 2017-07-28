# -*- encoding: utf-8 -*-

import json
from contextlib import contextmanager

__all__ = ['add', 'context', 'generate']

INDENTATION = '  '

class Context:

    def __init__(self, key, operand, operator, match_all):
        self.key = key
        self.operand = operand
        self.operator = 'equal' if operator is None else operator
        self.match_all = False if match_all is None else match_all

    def to_keymap(self):
        """converts to proper JSON for a .sublime-keymap"""
        context = {
            'key': self.key,
        }
        if self.operator != 'equal':
            context['operator'] = self.operator

        if self.operand is not True:
            context['operand'] = self.operand

        if self.match_all is not False:
            context['match_all'] = self.match_all

        return context
        return json.dumps(context, ensure_ascii=False)

class Keybinding:

    def __init__(self, keys, command, args=None, context=None):
        self.keys = keys
        self.command = command
        self.args = args
        self.context = context

    def to_keymap(self):
        """converts to proper JSON for a .sublime-keymap"""
        keybinding = {
            'keys': self.keys,
            'command': self.command
        }
        if self.args is not None:
            keybinding['args'] = self.args

        if self.context != []:
            keybinding['context'] = list(map(lambda k: k.to_keymap(), self.context))
            # keybinding['context'] = self.context

        return json.dumps(keybinding, ensure_ascii=False, indent=INDENTATION)

class Keymap:

    def __init__(self):
        self.keybindings = []
        self.context = []

    def add_context(self, key=None, operand=None, operator=None, match_all=None, context=None):
        if context is None:
            context = Context(key, operand, operator, match_all)
        elif key is not None or operand is not None or operator is not None or match_all is not None:
            raise ValueError('Tried to add context by passing an existing one but specified '
                             'arguments with it')
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
        string += ',\n'.join(map(lambda c: c.to_keymap(), self.keybindings))
        string += '\n]'
        return string

keymap = Keymap()

def add(*args, **kwargs):
    keymap.add_keybinding(*args, **kwargs)

def generate():
    string = keymap.to_keymap()
    # CSW: ignore
    print(string)

@contextmanager
def context(*args, **kwargs):
    actual_context = keymap.add_context(*args, **kwargs)
    yield
    keymap.remove_context(actual_context)

def main():
    add(['ctrl+a'], 'select_all')
    add(keys=['ctrl+,'], command='open_file', args={
        'path': 'whatever'
    })

    with context('selector', 'source.python', match_all=True), context('test', 'hello'):
        add(['ctrl+a'], 'select_all')
        add(['.', '.'], 'insert_snippet', {'content': 'self.'})

    generate()

main()