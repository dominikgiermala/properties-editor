import sublime
import sublime_plugin
from .lib.pyjavaproperties import Properties

class UpdatePropertyCommand(sublime_plugin.WindowCommand):
  def run(self, paths = []):
    # TODO: validate if *.properties file
    self.paths = paths
    self.window.show_input_panel("Property key:", '', self.on_key_put, None, None)

  def on_key_put(self, key):
    if key and key.strip():
      self.key = key
      self.window.show_input_panel("Property value:", '', self.on_value_put, None, None)

  def on_value_put(self, value):
    if value and value.strip():
      self.edit_properties(self.key, value)

  def edit_properties(self, key, value):
    files_without_key = []
    files_with_key = []
    for file in self.paths:
      p = Properties()
      p.load(open(file))
      if p.getProperty(key):
        files_with_key.append(file)
      else:
        files_without_key.append(file)
      p[key] = value
      p.store(open(file, 'w'))
    confirmation_message = "Property " + key + "=" + value + " was: " 
    confirmation_message += "\nAdded in files:\n" + "".join(files_without_key)
    confirmation_message += "\nEdited in files:\n" + "".join(files_with_key)
    sublime.message_dialog(confirmation_message)


class RemovePropertyCommand(sublime_plugin.WindowCommand):
  def run(self, paths = []):
    # TODO: validate if *.properties file
    self.paths = paths
    self.window.show_input_panel("Property key:", '', self.on_key_put, None, None)

  def on_key_put(self, key):
    if key and key.strip():
      self.remove_property(key, self.paths)

  def remove_property(self, key, paths):
    files_without_key = []
    files_with_key = []
    for file in self.paths:
      p = Properties()
      p.load(open(file))
      if p.getProperty(key):
        p.removeProperty(key)
        files_with_key.append(file)
        p.store(open(file, 'w'))
      else:
        files_without_key.append(file)
    confirmation_message = "Property " + key + " was: "
    confirmation_message += "\nRemoved in files:\n" + "".join(files_with_key)
    confirmation_message += "\nNot found in files:\n" + "".join(files_without_key)
    sublime.message_dialog(confirmation_message)
    