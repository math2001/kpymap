# Kpymap

<!-- MarkdownTOC -->

- [API](#api)
    - [`add\(keys, command\[, args\]\[, context\]\)`](#addkeys-command-args-context)
    - [`get_context\(key\[, operator\]\[, operand\]\[, match_all\]\)`](#get_contextkey-operator-operand-match_all)
    - [`context\(...\)`](#context)
    - [`get_option\(option_name\)`](#get_optionoption_name)
    - [`set_option\(option_name, option_value\)`](#set_optionoption_name-option_value)
- [Options](#options)
- [Tip](#tip)
    - [Encoding](#encoding)
    - [No updates](#no-updates)
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

### `get_option(option_name)`

Gets the value of the [option](#options) `option_name`. It has to be a string.

### `set_option(option_name, option_value)`

Set the [option](#options) `option_name` to `option_value`. `option_name` has to be a string.

## Options

Here are the available options:

|        Option Name        | Type | Default |                    Description                     |
|---------------------------|------|---------|----------------------------------------------------|
| `match_all_default_value` | bool | `False` | the `match_all` `Context`'s argument default value |

## Tip

### Encoding

In order to make python work with unicodes and non-ascii characters, you can add this at the top of the `kpymaper.py`:

```python
# -*- encoding: utf-8 -*-
```

It just tell python to use the `utf-8` encoding

### No updates

If the changes you make don't seem to be applied, you might want to check in the console (`View → Show Console`).

When a warning is printed into the console, a message will be printed in the status bar. Since a warning isn't notified in any other way for now, you should often check the status bar after saving your `kpymaper.py`, it might explain to you an unexpected behaviour.

If you think anything that seems like a bug to you, please [raise an issue](https://github.com/math2001/kpymaper/issues/new).

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

Gives:

```json
[
    {
        "keys": [".", "."],
        "command": "insert",
        "args": {
            "characters": "self."
        },
        "context": [
            {"key": "selector", "operand": "source.python", "match_all": true}
        ]
    },
    {
        "keys": ["alt+f"],
        "command": "fold_python_function",
        "context": [
            {"key": "selector", "operand": "source.python", "match_all": true}
        ]
    },
    {
        "keys": ["ctrl+u"],
        "command": "upper_case"
    },
    {
        "keys": ["`"],
        "command": "insert_snippet",
        "args": {
            "contents": "`$SELECTION`"
        },
        "context": [
            {"key": "selector", "operand": "text.markdown.html", "match_all": true},
            {"key": "selection_empty"}
        ]
    },
    {
        "keys": ["*"],
        "command": "insert_snippet",
        "args": {
            "contents": "*$SELECTION*"
        },
        "context": [
            {"key": "selector", "operand": "text.markdown.html", "match_all": true},
            {"key": "selection_empty"}
        ]
    },
    {
        "keys": ["*"],
        "command": "move",
        "args": {
            "by": "characters", 
            "forward": true
        },
        "context": [
            {"key": "selector", "operand": "text.markdown.html", "match_all": true},
            {"key": "regex_contains", "operand": "^*", "match_all": true}
        ]
    },
    {
        "keys": ["`"],
        "command": "move",
        "args": {
            "by": "characters", 
            "forward": true
        },
        "context": [
            {"key": "selector", "operand": "text.markdown.html", "match_all": true},
            {"key": "regex_contains", "operand": "^`", "match_all": true}
        ]
    },
    {
        "keys": ["ctrl+s"],
        "command": "message_dialog",
        "args": {
            "message": "Stop using ctrl+s, Sublime Text saves automatically for you"
        },
        "context": [
            {"key": "setting.save_on_focus_lost"},
            {"key": "setting.learning_mode"}
        ]
    }
]
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
