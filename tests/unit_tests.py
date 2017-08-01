# -*- encoding: utf-8 -*-

import unittest
import sys
sys.path.insert(0, __file__ + '../../..')
from kpymap import to_context, to_keybinding, Keybinding, Context

class Testr(unittest.TestCase):

    def test_to_keybinding(self):
        args_and_result_args = (
            (('ctrl+a', 'a'),
             (['ctrl+a'], 'a', {}, [])),

            (('ctrl+b', 'ctrl+c', 'command'),
             (['ctrl+b', 'ctrl+c'], 'command', {}, [])),

            (('ctrl+b', 'ctrl+c', 'command', {'a': 'b'}),
             (['ctrl+b', 'ctrl+c'], 'command', {'a': 'b'}, [])),

            (('ctrl+b', 'ctrl+c', 'command', {'a': 'b'}, Context('a', 'equal', 'c', True)),
             (['ctrl+b', 'ctrl+c'], 'command', {'a': 'b'}, [Context('a', 'equal', 'c', True)])),

            (('ctrl+b', 'ctrl+c', 'command', {'a': 'b'}, Context('a', 'equal', 'c', True), Context('d', 'not_equal', 'e', False)),
             (['ctrl+b', 'ctrl+c'], 'command', {'a': 'b'}, [Context('a', 'equal', 'c', True), Context('d', 'not_equal', 'e', False)])),

            (('ctrl+b', 'ctrl+c', 'command', Context('a', 'equal', 'c', True), Context('d', 'not_equal', 'e', False)),
             (['ctrl+b', 'ctrl+c'], 'command', {}, [Context('a', 'equal', 'c', True), Context('d', 'not_equal', 'e', False)])),
        )

        for args, result_args in args_and_result_args:
            self.assertEqual(to_keybinding(*args), Keybinding(*result_args))

    def test_to_context(self):
        args_and_result_args = (
            (('key', 'operator', 'operand', False), {}, ('key', 'operator', 'operand', False)),
            (('key', 'operand'), {}, ('key', 'equal', 'operand', False)),
            (('key', 'operand'), {'match_all': True}, ('key', 'equal', 'operand', True)),
            (('key', 'operand'), {'match_all': True}, ('key', 'equal', 'operand', True)),
            (('key', ), {}, ('key', 'equal', True, False)),
            (('key', ), {'match_all': True}, ('key', 'equal', True, False)),
        )
        for args, kwargs, result_args in args_and_result_args:
            self.assertEqual(to_context(*args, **kwargs), Context(*result_args))

if __name__ == '__main__':
    unittest.main()
