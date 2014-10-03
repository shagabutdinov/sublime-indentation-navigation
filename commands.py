import sublime
import sublime_plugin
import re

from Statement import statement
from Expression import expression

class GotoIndentation(sublime_plugin.TextCommand):
  def run(self, edit, type = 'change', backward = None, before = 0,
    alignment = 'left', expand = False, change = False, append = None):

    text = self.view.substr(sublime.Region(0, self.view.size())).split("\n")
    text.append('I') # last indented string

    regions = []
    for sel in self.view.sel():
      position = sel.a
      if expand:
        position = sel.b

      next = self._get_next_point(text, position, type, backward, before,
        alignment, change, append)

      while next == position and before != None and before > 0:
        before -= 1
        next = self._get_next_point(text, position, type, backward, before,
          alignment, change, append)

      if expand:
        regions.append(sublime.Region(sel.a, next))
      else:
        regions.append(sublime.Region(next, next))

    self.view.sel().clear()
    self.view.sel().add_all(regions)

    if len(regions) > 0:
      self.view.show(regions[0].a)

  def _get_next_point(self, text, point, type, backward, before, alignment,
    change, append):

    line, _ = self.view.rowcol(point)
    new_line = self._calculate_next_position(text, line, type, backward, before,
      change)

    if append != None and new_line != None:
      next_line_region = self.view.line(self.view.text_point(new_line + 1, 0))
      next_line = self.view.substr(next_line_region)
      if next_line.strip() in append:
        new_line += 1

    new_point = point
    if new_line != None:
      new_point = self._convert_to_point(text, new_line, alignment)

    return new_point

  def _convert_to_point(self, text, line, alignment):
    shift = len(text[line])
    if alignment == 'left':
      shift = len(re.search('^(\s*)', text[line]).group(1))
    elif alignment != 'right':
      raise Exception('Uknown alignment "' + alignment + '"')

    return self.view.text_point(line, shift)

  def _calculate_next_position(self, text, line, type, backward, before,
    change):
    search = range(line, len(text))
    if backward:
      search = range(line, -1, -1)

    current_indentation = None
    current_indentation_search = search
    for current_line in current_indentation_search:
      current_indentation = self._get_indentation(text[current_line])
      if current_indentation != None:
        break

    previous_lines, target_line, changed = [line], None, False
    for index, current_line in enumerate(search):
      # first line should be ignored
      if index == 0:
        continue

      indentation = self._get_indentation(text[current_line])
      if indentation == None:
        continue

      if indentation != current_indentation and not changed:
        if self.is_unidented_arguments(text, current_line):
          continue
        changed = True

      target_line_found = (self._check_indentation(type, indentation,
        current_indentation) and (not change or changed))

      if target_line_found:
        target_line = current_line
        break

      previous_lines.append(current_line)

    if before != None and before > 0:
      while before > len(previous_lines):
        before -= 1
      return target_line and previous_lines[-before]

    return target_line

  def is_unidented_arguments(self, text, line):
    point = self.view.text_point(line, 0)
    nesting = expression.get_nesting(self.view, point, 512)
    if nesting == None:
      return False

    start = self.view.substr(self.view.line(nesting[0]))
    start_spaces = re.search(r'^(\s*)', start).group(1)

    end = self.view.substr(self.view.line(nesting[1]))
    end_spaces = re.search(r'^(\s*)', end).group(1)

    if start_spaces == end_spaces:
      return False

    return statement.is_arguments(self.view, point)

  def _get_indentation(self, line):
    match = re.search(r'^(\s*)\S', line)
    return match and match.group(1)

  def _check_indentation(self, type, indentation1, indentation2):
    if type == 'equal':
      return indentation1 == indentation2

    if type == 'change':
      return indentation1 != indentation2

    if type == 'lesser':
      return len(indentation1) < len(indentation2)

    if type == 'lesser_or_equal':
      return indentation1 <= indentation2

    if type == 'greater':
      return len(indentation1) > len(indentation2)

    raise Exception('Unknown type "' + type + '"')