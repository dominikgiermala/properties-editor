import sublime
import sublime_plugin
import glob
import os
from .lib.pyjavaproperties import Properties

class PropertiesEditorCommand(sublime_plugin.WindowCommand):
  def run(self):
    if self.load_and_validate_settings():
      self.window.show_input_panel("Property key:", '', self.on_key_put, None, None)

  def on_key_put(self, key):
    if key and key.strip():
      self.key = key
      self.window.show_input_panel("Property value:", '', self.on_value_put, None, None)

  def on_value_put(self, value):
    if value and value.strip():
      self.edit_properties(self.key, value)

  def edit_properties(self, key, value):
    os.chdir(self.properties_dir)
    confirmation_message = "Property " + self.key + " set to " + value + " In files:\n"
    for file in glob.glob(self.files_regex):
      p = Properties()
      p.load(open(file))
      p[key] = value
      p.store(open(file, 'w'))
      confirmation_message += file + "\n"
    sublime.message_dialog(confirmation_message)

  def load_and_validate_settings(self):
    config_file_name = "PropertiesEditor.sublime-settings"
    settings = sublime.load_settings(config_file_name)
    self.properties_dir = settings.get('properties_dir')
    self.files_regex = settings.get('files_regex')
    is_valid = self.properties_dir and self.properties_dir.strip() and self.files_regex and self.files_regex.strip()
    if not is_valid:
      sublime.message_dialog("Properties Editor needs congiuration to work correctly.\n" +
        "Please set path to properties files regex in file " + config_file_name)
    return is_valid
    