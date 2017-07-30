# -*- encoding: utf-8 -*-

from kpymap import *

def test_single():
    reset()
    add(['ctrl+a'], 'select_all')
    return generate(return_json=True)

result_single = """\
[
    {
        "keys": ["ctrl+a"],
        "command": "select_all"
    }
]"""