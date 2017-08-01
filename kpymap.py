# -*- encoding: utf-8 -*-

import json
import uuid
import textwrap
try:
    import sublime
except ImportError:
    sublime = None
from os.path import join
from contextlib import contextmanager
from collections import OrderedDict

__all__ = ['add', 'context', 'generate', 'reset', 'get_context', 'get_keybinding']

DEFAULT_ARG_VALUE=uuid.uuid4()

INDENTATION = '    '

def dump(string, *args, **kwargs):
    return json.dumps(string, ensure_ascii=False, *args, **kwargs)

def output(*args, **kwargs):
    # used to by pass git hook
    # CSW: ignore
    print(*args, **kwargs)

def every(iterable, func):
    for item in iterable:
        if not func(item):
            return False
    return True

def error_message(message, printout=False):
    message = 'Kpymap (warning) ]> ' + message
    if sublime: sublime.status_message('Kpymap ]> Warning message displayed in the console!')
    if sublime and not printout:
        sublime.error_message(message)
    else:
        output(message)
    return message

def remove_duplicate(seq):
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

class Context:

    def __init__(self, key, operator, operand, match_all):
        self.key = key
        self.operand = operand
        self.operator = operator
        self.match_all = match_all

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

    def __eq__(self, obj):
        if not isinstance(obj, Context):
            return False

        return self.key == obj.key \
           and self.operator == obj.operator \
           and self.operand == obj.operand \
           and self.match_all == obj.match_all

    def __hash__(self):
        return hash((self.key, self.operator, self.operand, self.match_all))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        operator = '' if self.operator == 'equal' else ' operator=' + repr(self.operator)
        match_all = '' if self.match_all == False else ' match_all=' + repr(self.match_all)
        return '<Context key={!r}{} operand={!r}{}>'.format(self.key, operator, self.operand,
                                                            match_all)

class Keybinding:

    def __init__(self, keys, command, args, context):
        self.keys = list(keys)
        self.command = command
        self.args = args
        self.context = context

    def to_keymap(self):
        """converts to proper JSON for a .sublime-keymap"""
        string = '{\n'
        string += INDENTATION + '"keys": ' + dump(self.keys) + ',\n'
        string += INDENTATION + '"command": ' + dump(self.command)

        if self.args != {}:
            self.args = OrderedDict((key, self.args[key]) for key in sorted(self.args.keys()))
            string += ',\n' + INDENTATION + '"args": ' + \
                textwrap.indent(dump(self.args, indent=INDENTATION), INDENTATION)[len(INDENTATION):]

        if self.context != []:
            string += ',\n' + INDENTATION + '"context": [\n'
            string += ',\n'.join([(INDENTATION * 2) + context.to_keymap() for context in
                                 remove_duplicate(self.context)]) + '\n'
            string += INDENTATION + ']'

        return string + '\n}'

    def __eq__(self, obj):
        if not isinstance(obj, Keybinding):
            return False

        return self.keys == obj.keys \
           and self.command == obj.command \
           and self.args == obj.args \
           and self.context == obj.context

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        args = '' if self.args == {} else ' args=' + repr(self.args)
        context = '' if self.context == [] else ' context=' + repr(self.context)
        return '<Keybinding keys={!r} command={!r}{}{}>'.format(self.keys, self.command, args,
                                                                context)

class Keymap:

    def __init__(self):
        self.keybindings = []
        self.context = []
        self.keymap_generated = False
        self.shown_error_already = False

    def error_if_generated(self, message):
        if not self.keymap_generated:
            return

        error_message(message, printout=self.shown_error_already)
        self.shown_error_already = True

    def add_context(self, context):
        self.error_if_generated("You shouldn't add a context after JSON has been generated "
                                "since it is going to be simply ignored.")
        self.context.append(context)
        return context

    def add_keybinding(self, keybinding):
        self.error_if_generated("You shouldn't add a keybinding after JSON has been generated "
                                "since it is going to be simply ignored.")
        keybinding.context = self.context + keybinding.context
        self.keybindings.append(keybinding)
        return keybinding

    def remove_context(self, context):
        self.context.remove(context)

    def to_keymap(self):
        if self.keymap_generated:
            error_message("In order to improve performance, you should call 'generate()' only once")
        self.keymap_generated = True
        string = '[\n'
        string += textwrap.indent(',\n'.join(map(lambda c: c.to_keymap(), self.keybindings)), INDENTATION)
        string += '\n]'
        return string

keymap = Keymap()

def to_keybinding(*args, **kwargs):

    keys = []
    command = None
    arguments = {}
    context = []

    if isinstance(args[-1], str):
        keys = args[:-1]
        command = args[-1]
    else:
        length = len(args)
        just_str = True
        for i, arg in enumerate(args):
            if isinstance(arg, str) and just_str:
                keys.append(arg)
                continue
            just_str = False
            if isinstance(arg, Context):
                context.append(arg)
            else:
                arguments.update(arg)

        command = keys.pop()

    if arguments is None:
        arguments = {}

    arguments.update(kwargs)

    return Keybinding(keys, command, arguments, context)

def to_context(key, operator=DEFAULT_ARG_VALUE, operand=DEFAULT_ARG_VALUE, match_all=False):
    if isinstance(key, Context):
        if operator != DEFAULT_ARG_VALUE or operand != DEFAULT_ARG_VALUE or match_all != False:
            error_message('Passed a context as an argument but gave extra args with it (they are '
                          'simply ignored). Remove them to not get this warning anymore.',
                          printout=True)
        return key

    if operand == DEFAULT_ARG_VALUE:
        operand = operator
        operator = DEFAULT_ARG_VALUE

    if operator == DEFAULT_ARG_VALUE:
        operator = 'equal'

    if operand == DEFAULT_ARG_VALUE:
        operand = True

    return Context(key, operator, operand, match_all)

# APIS functions

@contextmanager
def context(*args, **kwargs):
    actual_context = keymap.add_context(to_context(*args, **kwargs))
    yield
    keymap.remove_context(actual_context)

def reset():
    keymap.__init__()

def add(*args, **kwargs):
    return keymap.add_keybinding(to_keybinding(*args, **kwargs))

def get_keybinding(*args, **kwargs):
    return to_keybinding(*args, **kwargs)

def get_context(*args, **kwargs):
    return to_context(*args, **kwargs)

def generate(return_json=False):
    string = keymap.to_keymap()
    if return_json is True or sublime is None:
        # the file is build, not run by ST, so just output the JSON
        return string

    keymap_file = join(sublime.packages_path(), 'User',
                       'Default ({}).sublime-keymap'.format(sublime.platform().title()))
    with open(keymap_file, 'w', encoding='utf-8') as fp:
        fp.write(string)
    output('Kpymap: wrote', keymap_file)

