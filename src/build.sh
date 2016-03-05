#!/bin/sh
cd ../dist
mkdir properties-editor
mkdir properties-editor/lib
cp "../src/properties_editor.py" properties-editor/
cp "../src/Side Bar.sublime-menu" properties-editor/
cp "../src/lib/pyjavaproperties.py" properties-editor/lib/
rm properties-editor.zip
zip -r properties-editor.zip properties-editor
rm -rf properties-editor