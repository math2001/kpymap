# -*- encoding: utf-8 -*-

"""
Runs every test file.

Imports every file in the current directory, finds the functions, runs them, and compare their
return value to the expected result.
"""

import importlib
import sys
import glob
import os.path as path
from types import FunctionType
import unittest

class Testr(unittest.TestCase):

    def run_tests(self, module):
        functions = [getattr(module, function) for function in dir(module) if function.startswith('test_')]
        functions = [fn for fn in functions if isinstance(fn, FunctionType)]
        for function in functions:
            test_name = function.__name__[5:]
            try:
                expetected_result = getattr(module, 'result_' + test_name)
            except AttributeError:
                self.fail("Couldn't run test {!r} since there is no excepted result (should be "
                          "saved in the variable {!r})".format(test_name, 'result_' + test_name))
            else: 
                self.assertEqual(function(), expetected_result)

    def test_everything(self):
        self.maxDiff = None
        for file in glob.glob('*.py'):
            if file == path.basename(__file__):
                continue
            self.run_tests(importlib.import_module(path.splitext(file)[0]))

sys.path.insert(0, path.dirname(path.dirname(path.dirname(__file__))))

if __name__ == '__main__':
    unittest.main()