#!/usr/bin/env bash
# fontlist: fc-list
# convert -list fonts
# https://legacy.imagemagick.org/Usage/text/

FONTLIST="Andale-Mono Arial-Black C059-Bold-Italic C059-Bold C059-Italic C059-Roman Caladea-Bold-Italic Caladea-Bold Caladea-Italic Caladea Cantarell-Extra-Bold Cantarell-Bold Cantarell-Light Cantarell-Regular Cantarell-Thin Century-Schoolbook-L-Roman Courier-New EB-Garamond-12-Regular EB-Garamond-12-Italic GentiumAlt Gentium-Basic"

function render () {
  FONT_USED="$2" # abs path of ttf file
  echo $FONT_USED
  PNG_FILE="test_${2}.png"
  convert -font "$2"   -pointsize 36 label:"$1" -gravity center "$PNG_FILE" 
  # display "$PNG_FILE"
}
# list all possible argument
# convert -list font
TXT="Árvíztűrő tükörfúrógép 0123456789+-_?.!=" 
# render "$TXT" "Z003-MediumItalic"
# render "$TXT" "Waree-Bold-Oblique"

for FONT in $(convert -list font | grep Font: | awk '{print $2}'); do 
  echo $FONT; 
  render "$TXT" "$FONT"
done

