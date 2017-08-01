# Kpymap

<!-- MarkdownTOC -->

- [API](#api)
    - [`add\(keys, command\[, args\]\[, context\]\)`](#addkeys-command-args-context)
    - [`get_context\(key\[, operator\]\[, operand\]\[, match_all\]\)`](#get_contextkey-operator-operand-match_all)
    - [`context\(...\)`](#context)
- [Examples](#examples)
    - [`with` block](#with-block)
- [Installation](#installation)
    - [Using package control](#using-package-control)
    - [Using the command line](#using-the-command-line)

<!-- /MarkdownTOC -->


A simple API that allows you to write your Sublime Text keybindings in python.

All it does is provide you a tiny API to add keybindings and convert them into JSON (properly formated for sublime keybindings).

All you have to do is create python script (for example `kpymaper.py`) in your `User` folder, and add this boilerplate (it won't be written in the further examples):

```python
from kpymap import *
reset()

# code goes here

generate()
```

**Watch out**: If you save this script, it'll overwrite your current keybindings. Make sure you make a copy of **before**.

You have access to the following functions:

## API

### `add(keys, command[, args][, context])`

Adds a keybinding.

- `keys` must be a list of **strings**
- `command` must be a string
- `args` (optional) a dict
- `context` (optional) a context (you can get one using [`get_context`](#get_context)). It might also be a *list* of context

### `get_context(key[, operator][, operand][, match_all])`

This allows you to get a context object, so that you can add it to a keybinding.

- `key` must be a **string** or a **context** object (if it is, every other arguments will be ignored and returns the given context).
- `operator` (optional) must be a **string**. Default: `equal`
- `operand` (optional) any JSON serializable object. Default: `True`
- `match_all` (optional) a boolean. Default: `False`

Note: if only specify 2 arguments (such as `get_context('selector', 'source.python')`), the second argument will be understood as the **operand** and the operator will be set to `equal` (its default value)

### `context(...)`

It takes the exact same arguments as [`get_context`](#get_context), but it implements a specific behaviour using `with` blocks. Every keybinding added (`add`) inside this block will have the the specified context(s). Of course, the others won't.

## Examples

### `with` block

```python

# You can set common contests using `with` block
with context('selector', 'source.python', True):
    add('.', '.', 'insert', {'characters': 'self.'})
    add('alt+f', 'fold_python_function')

# or not

add('ctrl+u', 'upper_case')

# You can nest some!

with context('selector', 'text.markdown.html', True):
    with context('selection_empty', False):
        add('`', 'insert_snippet', '`$SELECTION`')
        add('*', 'insert_snippet', '*$SELECTION*')

    add('*', 'move', {'forward': True, 'by': 'characters'},
        get_context('regex_contains', '^*', True))
    add('`', 'move', {'forward': True, 'by': 'characters'},
        get_context('regex_contains', '^`', True))

# or add more than one context using one `with` statement

with context('setting.save_on_focus_lost'), \
     context('setting.learning_mode'):
     add('ctrl+s', 'message_dialog',
         {'message': 'Stop using ctrl+s, Sublime Text saves automatically for you'})

```

```json

```



## Installation

Because it is not available on package control for now, you have to add this repo "manually" to your list.

### Using package control

1. Open up the command palette (<kbd>ctrl+shift+p</kbd>), and find `Package Control: Add Repository`. Then enter the URL of this repo: `https://github.com/math2001/kpymap` in the input field.
2. Open up the command palette again and find `Package Control: Install Package`, and just search for `kpymap`. (just a normal install)

### Using the command line

```bash
cd "%APPDATA%\Sublime Text 3\Packages"             # on window
cd ~/Library/Application\ Support/Sublime\ Text\ 3 # on mac
cd ~/.config/sublime-text-3                        # on linux

git clone "https://github.com/math2001/kpymap"
```

> Which solution do I choose?

It depends of your needs:

- If you intend to just use kpymap, then pick the first solution (Package Control), **you'll get automatic update**.
- On the opposite side, if you want to tweak it, use the second solution. Note that, to get updates, you'll have to `git pull`
