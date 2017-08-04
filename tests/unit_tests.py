# -*- encoding: utf-8 -*-

import unittest
import sys
sys.path.insert(0, __file__ + '../../..')
from kpymap import to_context, to_keybinding, Keybinding, Context, get_option, set_option
from contextlib import contextmanager

@contextmanager
def option(option_name, option_value):
    """Set option and then restore it automatically"""
    default_value = get_option(option_name)
    set_option(option_name, option_value)
    yield
    set_option(option_name, default_value)


class Testr(unittest.TestCase):

    def test_to_keybinding(self):
        args_and_result_args = (
            (('ctrl+a', 'a'), {},
             (['ctrl+a'], 'a', {}, [])),

            (('ctrl+b', 'ctrl+c', 'command'), {},
             (['ctrl+b', 'ctrl+c'], 'command', {}, [])),

            (('ctrl+b', 'ctrl+c', 'command', {'a': 'b'}), {},
             (['ctrl+b', 'ctrl+c'], 'command', {'a': 'b'}, [])),

            (('ctrl+b', 'ctrl+c', 'command'), {'a': 'b'},
             (['ctrl+b', 'ctrl+c'], 'command', {'a': 'b'}, [])),

            (('ctrl+b', 'ctrl+c', 'command', {'a': 'c'}), {'a': 'b'},
             (['ctrl+b', 'ctrl+c'], 'command', {'a': 'b'}, [])),

            (('ctrl+b', 'ctrl+c', 'command', {'a': 'b'}, {'c': 'd'}), {},
             (['ctrl+b', 'ctrl+c'], 'command', {'a': 'b', 'c': 'd'}, [])),

            (('ctrl+b', 'ctrl+c', 'command'), {'a': 'b', 'c': 'd'},
             (['ctrl+b', 'ctrl+c'], 'command', {'a': 'b', 'c': 'd'}, [])),

            (('ctrl+b', 'ctrl+c', 'command', {'a': 'b'}, Context('a', 'equal', 'c', True)), {},
             (['ctrl+b', 'ctrl+c'], 'command', {'a': 'b'}, [Context('a', 'equal', 'c', True)])),

            (('ctrl+b', 'ctrl+c', 'command', Context('a', 'equal', 'c', True)), {'a': 'b'},
             (['ctrl+b', 'ctrl+c'], 'command', {'a': 'b'}, [Context('a', 'equal', 'c', True)])),

            (('ctrl+b', 'ctrl+c', 'command', {'a': 'b'}, Context('a', 'equal', 'c', True), Context('d', 'not_equal', 'e', False)), {},
             (['ctrl+b', 'ctrl+c'], 'command', {'a': 'b'}, [Context('a', 'equal', 'c', True), Context('d', 'not_equal', 'e', False)])),

            (('ctrl+b', 'ctrl+c', 'command', Context('a', 'equal', 'c', True), Context('d', 'not_equal', 'e', False)), {'a': 'b'},
             (['ctrl+b', 'ctrl+c'], 'command', {'a': 'b'}, [Context('a', 'equal', 'c', True), Context('d', 'not_equal', 'e', False)])),

            (('ctrl+b', 'ctrl+c', 'command', Context('a', 'equal', 'c', True), Context('d', 'not_equal', 'e', False)), {},
             (['ctrl+b', 'ctrl+c'], 'command', {}, [Context('a', 'equal', 'c', True), Context('d', 'not_equal', 'e', False)])),

            (('ctrl+b', 'ctrl+c', 'command', Context('a', 'equal', 'c', True), Context('d', 'not_equal', 'e', False)), {},
             (['ctrl+b', 'ctrl+c'], 'command', {}, [Context('a', 'equal', 'c', True), Context('d', 'not_equal', 'e', False)])),

        )

        for args, kwargs, result_args in args_and_result_args:
            self.assertEqual(to_keybinding(*args, **kwargs), Keybinding(*result_args))

    def test_to_context(self):
        args_and_result_args = (
            (('key', 'operator', 'operand', False), {}, ('key', 'operator', 'operand', False)),
            (('key', 'operand'), {}, ('key', 'equal', 'operand', False)),
            (('key', 'operand'), {'match_all': True}, ('key', 'equal', 'operand', True)),
            (('key', 'operand'), {'match_all': True}, ('key', 'equal', 'operand', True)),
            (('key', ), {}, ('key', 'equal', True, False)),
            (('key', ), {'match_all': True}, ('key', 'equal', True, True)),
        )
        for args, kwargs, result_args in args_and_result_args:
            self.assertEqual(to_context(*args, **kwargs), Context(*result_args))

    def test_to_context_with_option(self):
        args_and_result_args = (
            (('key', 'operator', 'operand', False), {}, ('key', 'operator', 'operand', False)),
            (('key', 'operand'), {}, ('key', 'equal', 'operand', True)),
            (('key', 'operand'), {'match_all': False}, ('key', 'equal', 'operand', False)),
            (('key', 'operand'), {'match_all': True}, ('key', 'equal', 'operand', True)),
            (('key', ), {}, ('key', 'equal', True, True)),
            (('key', ), {'match_all': True}, ('key', 'equal', True, True)),
        )
        with option('match_all_default_value', True):
            for args, kwargs, result_args in args_and_result_args:
                self.assertEqual(to_context(*args, **kwargs), Context(*result_args))

if __name__ == '__main__':
    unittest.main()
