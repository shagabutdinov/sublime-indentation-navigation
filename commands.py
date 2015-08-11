import sublime
import sublime_plugin

from . import indentation_navigation

class GotoIndentation(sublime_plugin.TextCommand):
  def run(self, edit, type = 'change', backward = None, before = 0,
    alignment = 'left', expand = False, change = False, append = None,
    use_empty_line = False, before_if_lesser = True):

    regions = []
    for sel in self.view.sel():
      position = sel.a
      if expand:
        position = sel.b

      next = indentation_navigation.get_point(self.view, position, type,
        backward, before, alignment, change, append, use_empty_line,
        before_if_lesser)

      if expand:
        regions.append(sublime.Region(sel.a, next))
      else:
        regions.append(sublime.Region(next, next))

    self.view.sel().clear()
    self.view.sel().add_all(regions)

    if len(regions) > 0:
      self.view.show(regions[0].b)