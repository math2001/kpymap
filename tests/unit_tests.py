# -*- encoding: utf-8 -*-

import unittest
import sys
sys.path.insert(0, __file__ + '../../..')
from kpymap import to_keybinding, Keybinding, Context

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

if __name__ == '__main__':
    unittest.main()

def run():
    unittest.main()