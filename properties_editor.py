import sublime
import sublime_plugin
import glob
import os
from .lib.pyjavaproperties import Properties

class PropertiesEditorCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.show_input_panel("Property key:", '', self.on_key_put, None, None)

  def on_key_put(self, key):
    if key and key.strip():
      self.key = key
      self.window.show_input_panel("Property value:", '', self.on_value_put, None, None)

  def on_value_put(self, value):
    if value and value.strip():
      self.edit_properties(self.key, value)

  def edit_properties(self, key, value):
    os.chdir("/home/dominik/git/al/ei-i18n-messages/src/main/resources")
    confirmation_message = "Property " + self.key + " set to " + value + " In files:\n"
    for file in glob.glob("messages-locale_*.properties"):
      p = Properties()
      p.load(open(file))
      p[key] = value
      p.store(open(file, 'w'))
      confirmation_message += file + "\n"
    sublime.message_dialog(confirmation_message)