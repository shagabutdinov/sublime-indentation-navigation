import sublime
import re

try:
  from Statement import statement
  from Expression import expression
except ImportError as error:
  sublime.error_message("Dependency import failed; please read readme for " +
    "IndentationNavigation plugin for installation instructions; to disable " +
    "this message remove this plugin; message: " + str(error))
  raise error

def get_point(view, position, type = 'change', backward = None,
  before = 0, alignment = 'left', change = False,
  append = None, use_empty_line = False, before_if_lesser = True):

  text = view.substr(sublime.Region(0, view.size())).split("\n")
  text.append('I') # last indented string

  next = _get_next_point(view, text, position, type, backward, before,
    alignment, change, append, use_empty_line, before_if_lesser)

  while next == position and before != None and before > 0:
    before -= 1
    next = _get_next_point(view, text, position, type, backward, before,
      alignment, change, append, use_empty_line, before_if_lesser)

  return next

def _get_next_point(view, text, point, type, backward, before, alignment,
  change, append, use_empty_line, before_if_lesser):

  line, _ = view.rowcol(point)
  new_line = _calculate_next_position(view, text, line, type, backward, before,
    change, use_empty_line, before_if_lesser)

  if append != None and new_line != None:
    next_line_region = view.line(view.text_point(new_line + 1, 0))
    next_line = view.substr(next_line_region)
    if next_line.strip() in append:
      new_line += 1

  new_point = point
  if new_line != None:
    new_point = _convert_to_point(view, text, new_line, alignment)

  return new_point

def _convert_to_point(view, text, line, alignment):
  shift = len(text[line])
  if alignment == 'left':
    shift = len(re.search('^(\s*)', text[line]).group(1))
  elif alignment != 'right':
    raise Exception('Uknown alignment "' + alignment + '"')

  return view.text_point(line, shift)

def _calculate_next_position(view, text, line, type, backward, before,
  change, use_empty_line, before_if_lesser):

  search = range(line, len(text))
  if backward:
    search = range(line, -1, -1)

  current_indentation = None
  current_indentation_search = search
  for current_line in current_indentation_search:
    current_indentation = _get_indentation(text[current_line])
    if current_indentation != None:
      break

  initial_indentation = current_indentation
  previous_lines, target_line, changed = [line], None, False
  indentation = None
  for index, current_line in enumerate(search):
    # first line should be ignored
    if index == 0:
      continue

    use_current_empty_line = (
      use_empty_line and
      indentation != None and
      _check_indentation(
        'equal',
        current_indentation,
        indentation
      )
    )

    indentation = _get_indentation(text[current_line], use_current_empty_line)
    if indentation == None:
      continue

    if indentation != current_indentation and not changed:
      if is_unidented_arguments(view, text, current_line):
        continue
      changed = True

    target_line_found = (
      _check_indentation(type, indentation, current_indentation) and
      (not change or changed)
    )

    if target_line_found:
      target_line = current_line
      break

    previous_lines.append(current_line)

  if target_line == None:
    return None

  is_before_valid = (
    before != None and
    before > 0 and (
      not before_if_lesser or
      _check_indentation(
        'lesser',
        _get_indentation(text[target_line], use_empty_line),
        current_indentation
      )
    )
  )

  if is_before_valid:
    while before > len(previous_lines):
      before -= 1
    return target_line and previous_lines[-before]

  return target_line

def is_unidented_arguments(view, text, line):
  point = view.text_point(line, 0)
  nesting = expression.get_nesting(view, point, 512)
  if nesting == None:
    return False

  start = view.substr(view.line(nesting[0]))
  start_spaces = re.search(r'^(\s*)', start).group(1)

  end = view.substr(view.line(nesting[1]))
  end_spaces = re.search(r'^(\s*)', end).group(1)

  if start_spaces == end_spaces:
    return False

  return statement.is_arguments(view, point)

def _get_indentation(line, use_empty_line = False):
  match = re.search(r'^(\s*)\S', line)
  if match == None and use_empty_line:
    return ''

  return match and match.group(1)

def _check_indentation(type, indentation1, indentation2):
  if type == 'equal':
    return indentation1 == indentation2

  if type == 'change':
    return indentation1 != indentation2

  if type == 'lesser':
    return (
      len(indentation1) < len(indentation2) or (
        indentation1 == '' and len(indentation1) == len(indentation2)
      )
    )

  if type == 'lesser_or_equal':
    return len(indentation1) <= len(indentation2)

  if type == 'greater':
    return len(indentation1) > len(indentation2)

  raise Exception('Unknown type "' + type + '"')