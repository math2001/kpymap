# -*- encoding: utf-8 -*-
from kpymap import *

def test_contexts():
    reset()
    class contexts:
        word_before = get_context('preceding_text', 'regex_contains', "[\\w']$")
        textplain = get_context('selector', 'text.plain')

    with context('dictionnary', 'Packages/Language - French - Français/fr_FR.dic'),\
         context(contexts.textplain):

        add(['2'], 'insert', {'characters': 'é'}, [contexts.word_before, contexts.textplain])
        add(['2'], 'insert', {'characters': 'é'}, contexts.textplain)
        add(['2'], 'insert', contexts.textplain)


    return generate(return_json=True)

result_contexts = """[
    {
        "keys": ["2"],
        "command": "insert",
        "args": {
            "characters": "é"
        },
        "context": [
            {"key": "dictionnary", "operand": "Packages/Language - French - Français/fr_FR.dic"},
            {"key": "selector", "operand": "text.plain"},
            {"key": "preceding_text", "operator": "regex_contains", "operand": "[\\\\w']$"}
        ]
    },
    {
        "keys": ["2"],
        "command": "insert",
        "args": {
            "characters": "é"
        },
        "context": [
            {"key": "dictionnary", "operand": "Packages/Language - French - Français/fr_FR.dic"},
            {"key": "selector", "operand": "text.plain"}
        ]
    },
    {
        "keys": ["2"],
        "command": "insert",
        "context": [
            {"key": "dictionnary", "operand": "Packages/Language - French - Français/fr_FR.dic"},
            {"key": "selector", "operand": "text.plain"}
        ]
    }
]"""
