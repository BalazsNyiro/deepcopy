#!/usr/bin/env bash
# fontlist: fc-list
# convert -list fonts
# https://legacy.imagemagick.org/Usage/text/
# https://stackoverflow.com/questions/32108623/image-magick-padding-font

FONT_LIST="Andale-Mono Arial-Black C059-Bold-Italic C059-Bold C059-Italic C059-Roman Caladea-Bold-Italic Caladea-Bold Caladea-Italic Caladea Cantarell-Extra-Bold Cantarell-Bold Cantarell-Light Cantarell-Regular Cantarell-Thin Century-Schoolbook-L-Roman Courier-New EB-Garamond-12-Regular EB-Garamond-12-Italic GentiumAlt Gentium-Basic"

function render () {
  FONT_USED="$2" # abs path of ttf file
  echo $FONT_USED
  if [ -n "$1" ]; then
    # output file is defined
    PNG_FILE="$3"
  else
    # output file is not defined
    PNG_FILE="test_${2}.png"
  fi
  # convert -font "$2" -splice 10x10 -pointsize 36 label:"$1" -gravity center "$PNG_FILE"
  convert -font "$2" -border 10x10+10+10 -bordercolor white -pointsize 36 label:"$1" -gravity center "$PNG_FILE"
  # display "$PNG_FILE"
}
# list all possible argument
# convert -list font
TXT="Árvíztűrő tükörfúrógép 0123456789+-_?.!=" 
# render "$TXT" "Z003-MediumItalic"
# render "$TXT" "Waree-Bold-Oblique"

#FONT_LIST_ALL=$(convert -list font | grep Font: | awk '{print $2}')
for FONT in $FONT_LIST; do
  echo $FONT; 
  render "$TXT" "$FONT"
done

######### render fix images
render A Andale-Mono general_A.png
render jinn Andale-Mono general_jinn.png
