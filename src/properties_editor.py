import sublime
import sublime_plugin
from .lib.pyjavaproperties import Properties

class AddEditPropertyCommand(sublime_plugin.WindowCommand):
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
    confirmation_message += "\nAdded in files:\n" + "\n".join(files_without_key)
    confirmation_message += "\n\nEdited in files:\n" + "\n".join(files_with_key)
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
    confirmation_message += "\nRemoved in files:\n" + "\n".join(files_with_key)
    confirmation_message += "\n\nNot found in files:\n" + "\n".join(files_without_key)
    sublime.message_dialog(confirmation_message)


class RenameKeyCommand(sublime_plugin.WindowCommand):
  def run(self, paths = []):
    # TODO: validate if *.properties file
    self.paths = paths
    self.window.show_input_panel("Key to rename:", '', self.on_old_key_put, None, None)

  def on_old_key_put(self, old_key):
    if old_key and old_key.strip():
      self.old_key = old_key
      self.window.show_input_panel("New key:", '', self.on_new_key_put, None, None)

  def on_new_key_put(self, new_key):
    if new_key and new_key.strip():
      self.new_key = new_key
      self.rename_key(self.old_key, self.new_key)

  def rename_key(self, old_key, new_key):
    files_without_old_key = []
    files_with_new_key = []
    files_with_renamed_key = []
    for file in self.paths:
      p = Properties()
      p.load(open(file))
      if p.getProperty(old_key):
        if not p.getProperty(new_key):
          p[new_key] = p[old_key]
          p.removeProperty(old_key)
          files_with_renamed_key.append(file)
        else:
          files_with_new_key.append(file)
      else:
        files_without_old_key.append(file)
      p.store(open(file, 'w'))
    self.display_confirmation_message(files_without_old_key, files_with_new_key, files_with_renamed_key)

  def display_confirmation_message(self, files_without_old_key, files_with_new_key, files_with_renamed_key):
    confirmation_message = "Key " + self.old_key + " was: " 
    if files_with_renamed_key:
      confirmation_message += "\nRenamed in files:\n" + "\n".join(files_with_renamed_key)
    if files_without_old_key:
      confirmation_message += "\n\nNot found in files:\n" + "\n".join(files_without_old_key)
    if files_with_new_key:
      confirmation_message += "\n\nKey " + self.new_key + " already exists in files:\n" + "\n".join(files_with_new_key)
    if files_without_old_key or files_with_new_key:
      sublime.error_message(confirmation_message)
    else:
      sublime.message_dialog(confirmation_message)