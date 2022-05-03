#!/usr/bin/env bash
# fontlist: fc-list
# convert -list fonts
# https://legacy.imagemagick.org/Usage/text/
function render () {
  FONT_USED="$2" # abs path of ttf file
  echo $FONT_USED
  PNG_FILE="test_${2}.png"
  convert -font "$2"   -pointsize 36 label:"$1" -gravity center "$PNG_FILE" 
  display "$PNG_FILE"
}
# list all possible argument
# convert -list font
TXT="Árvíztűrő tükörfúrógép 0123456789+-_?.!=" 
render "$TXT" "Z003-MediumItalic"
render "$TXT" "Waree-Bold-Oblique"
