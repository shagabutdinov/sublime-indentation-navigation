# Sublime IndentationNavigation plugin

This is glorious plugin that allow to navigate through text usign indentation of
lines. It reduce count of typing drastically when managing or navigating through
blocks of code.

### Demo

![Demo](https://raw.github.com/shagabutdinov/sublime-indentation-navigation/master/demo/demo.gif "Demo")


### Installation

This plugin is part of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
plugin set. You can install sublime-enhanced and this plugin will be installed
automatically.

If you would like to install this package separately check "Installing packages
separately" section of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
package.

### Usage

There is several handy usecases (please see keyboard shortcuts in "commands"
section below):

1. Go to out of indentation - when cursor is in "if" or "for" block hit keyboard
shortcut to go to beginning or end of this block.

  ```
  if condition
    statement1 # <- cursor at this line
    statement2
  |end # <- cursor here after executing command
  ```

2. Go to into next indented block

  ```
  statement1 # <- cursor at this line
  statement2

  |if condition # <- cursor here after executing command
    ...
  end
  ```

3. Go to end of next indented block

  ```
  statement1 # <- cursor at this line
  statement2

  if condition
    ...
  |end # <- cursor here after executing command
  ```

4. Select to next indented block

  ```
  | # <- cursor here
  {statement1
  statement2} # <- block will be selected after executing command

  if condition
    ...
  end
  ```

5. Select up to next indented block

  ```
  | # <- cursor here
  {statement1
  statement2

  if condition
    ...
  end} # <- block will be selected after executing command
  ```

6. Select current indented block to the end

  ```
  if condition
    statement1
    | # <- cursor here
    {statement2
    statement3} # <- block will be selected after executing command
  end
  ```

7. Select current indentation - provides ability to select current indentation
that works a bit better that sublime's default "expand_selection" {"to":
"indentation"}

Backward versions of function is useless when working with languages that use
indentation to define code blocks (python, cofee) :(

### Commands

| Description                           | Keyboard shortcut | Command palette                                              |
|---------------------------------------|-------------------|--------------------------------------------------------------|
| Goto out of block forward             | alt+h             | IndentationNavigation: Goto out of block forward             |
| Goto out of block backward            | alt+y             | IndentationNavigation: Goto out of block backward            |
| Select to the end of block forward    | alt+shift+h       | IndentationNavigation: Select to the end of block forward    |
| Select to the end of block backward   | alt+shift+y       | IndentationNavigation: Select to the end of block backward   |
| Goto block forward                    | alt+ctrl+h        | IndentationNavigation: Goto block forward                    |
| Goto block backward                   | alt+ctrl+y        | IndentationNavigation: Goto block backward                   |
| Select to beginning of block forward  | alt+ctrl+shift+h  | IndentationNavigation: Select to beginning of block forward  |
| Select to beginning of block backward | alt+ctrl+shift+y  | IndentationNavigation: Select to beginning of block backward |
| Goto end of block forward             | ctrl+h            | IndentationNavigation: Goto end of block forward             |
| Goto end of block backward            | ctrl+y            | IndentationNavigation: Goto end of block backward            |
| Select to end of block forward        | ctrl+shift+h      | IndentationNavigation: Select to end of block forward        |
| Select to end of block backward       | ctrl+shift+y      | IndentationNavigation: Select to end of block backward       |
| Select current indentation            | alt+u             | IndentationNavigation: Select current indentation            |


### Dependencies

- https://github.com/shagabutdinov/sublime-statement
- https://github.com/shagabutdinov/sublime-expression