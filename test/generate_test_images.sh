#!/usr/bin/env bash
# fontlist: fc-list
# convert -list fonts

TRUETYPE_FONT='CourierNew'
TRUETYPE_FONT='Z003-MediumItalic'

# https://legacy.imagemagick.org/Usage/text/
function render () {
  FONT_USED="$2" # abs path of ttf file
  echo $FONT_USED
  # WORK
  # gm convert -font 'Helvetica'   -fill green -draw 'text 50,300 Magick' -pointsize 100  ~/flora-hearts.jpg annotated.gif
  gm convert -font 'l-regular-i-normal--0-0-0-0-p-0-iso8859-2'   -fill green -draw 'text 50,300 Magicktext' -pointsize 100  ~/flora-hearts.jpg annotated.gif

  # list all possible argument
  # convert -list font
  convert -font "$2"   -pointsize 36 label:"$1" -gravity center test.png 
  display test.png

}
render "Árvíztűrő tükörfúrógép 0123456789+-_?.!=" $TRUETYPE_FONT
