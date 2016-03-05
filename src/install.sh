#!/bin/sh
sh build.sh
rm -rf ~/.config/sublime-text-3/Packages/properties-editor/
unzip ../dist/properties-editor.zip -d ~/.config/sublime-text-3/Packages/