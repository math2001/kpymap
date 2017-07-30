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

class contexts:
    word_before = get_context('preceding_text', 'regex_contains', '[\\w\']$')
    iswidget = get_context('setting.is_widget')
    javascript = get_context('selector', 'source.js', match_all=True)
    python = get_context('selector', 'source.python', match_all=True)

add('ctrl+k', 'ctrl+c', 'show_panel', {'panel': 'console', 'toggle': True})
add('ctrl+k', 'ctrl+d', 'console_cleanr')
add('ctrl+k', 'ctrl+m', 'toggle_minimap')
add('ctrl+k', 'ctrl+s', 'toggle_side_bar')
add('ctrl+k', 'ctrl+o', 'toggle_show_open_files')

with context(contexts.python):
    add('alt+f', 'fold_python_functions')
    add('alt+e', 'insert', {'characters': 'enumerate($1)'})

with context('selector', 'text.html.markdown'):
    add('ctrl+o', 'markdown_preview', {'parser': 'github', 'target': 'browser'})

add('.', '.', 'insert', {'characters': 'self.'}, get_context('selector', 'source.python - comment - string'))

add('f8', 'chain', {'commands': [["save"], ["close_window"]]},
    get_context('selector', 'text.git-commit-message'))

add('<', '-', 'insert', {'characters': '← '})
add('-', '>', 'insert', {'characters': '→ '})

add('alt+f', 'fold_javascript_functions', contexts.javascript)
add('alt+q', 'change_quotes')

add('alt+j', 'swap_line_down')
add('alt+k', 'swap_line_up')
add('alt+l', 'indent')
add('alt+h', 'unindent')

add('ctrl+r', 'permute_selection', get_context('num_selections', 2))
add('ctrl+alt+p', 'project_manager', {'action': 'switch'})
add('alt+p', 'project_manager', {'action': 'new'})

add('ctrl+t', 'title_case')
add('ctrl+u', 'upper_case')
add('ctrl+l', 'lower_case')

with context('dictionary', 'equal', 'Packages/Language - French - Français/fr_FR.dic'), \
     context('selector', 'equal', 'text.plain'):

    add('2', 'insert', {'characters': 'é'}, contexts.word_before)
    add('7', 'insert', {'characters': 'è'})
    add('e', 'e', 'insert', {'characters': 'ée'})
    add('ctrl+0', 'insert', {'characters': 'à'})
    add('ctrl+7', 'insert', {'characters': 'è'})

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