# Kpymap

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

It takes the exact same arguments as [`get_context`](#get_context), but it implements a specific behaviour using `with` blocks. Use it like so:

```python
with context('selector', 'source.python'):
    # every shortcut added in this block will have the context(s)
    # specified above automatically added
    add(['.', '.'], 'insert', {'characters': 'self.'}) # works only in python

add(['ctrl+shift+o'], 'open_dir', {'dir': '$packages'}) # works everywhere
```

And that's it!

### Examples

*Coming soon...*