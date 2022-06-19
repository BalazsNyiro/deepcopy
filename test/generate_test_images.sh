#!/usr/bin/env bash
# fontlist: fc-list
# convert -list fonts
# https://legacy.imagemagick.org/Usage/text/
# https://stackoverflow.com/questions/32108623/image-magick-padding-font

BORDER_THICK="10x10+10+10"
BORDER_NO="no_border"

FONT_LIST="Andale-Mono Arial-Black C059-Bold-Italic C059-Bold C059-Italic C059-Roman Caladea-Bold-Italic Caladea-Bold Caladea-Italic Caladea Cantarell-Extra-Bold Cantarell-Bold Cantarell-Light Cantarell-Regular Cantarell-Thin Century-Schoolbook-L-Roman Courier-New EB-Garamond-12-Regular EB-Garamond-12-Italic GentiumAlt Gentium-Basic"

function render () {
  BORDER=$3
  FONT_USED="$2" # abs path of ttf file
  echo $FONT_USED

  if [ -n "$4" ]; then
    # output file is defined
    PNG_FILE="$4"
  else
    # output file is not defined
    PNG_FILE="test_${2}.png"
  fi
  if [ "$BORDER" = "$BORDER_NO" ];
    then
      BORDER_FLAG="";
      BORDER=""
      # if no border param, don't use border flag
    else BORDER_FLAG="-border";
  fi
  # convert -font "$2" -splice 10x10 -pointsize 36 label:"$1" -gravity center "$PNG_FILE"
  convert -font "$2" $BORDER_FLAG $BORDER -bordercolor white -pointsize 36 label:"$1" -gravity center "$PNG_FILE"
  # display "$PNG_FILE"
}
# list all possible argument
# convert -list font
TXT="Árvíztűrő tükörfúrógép 0123456789+-_?.!=" 
# render "$TXT" "Z003-MediumItalic" $BORDER_THICK
# render "$TXT" "Waree-Bold-Oblique" $BORDER_THICK

#FONT_LIST_ALL=$(convert -list font | grep Font: | awk '{print $2}')
for FONT in $FONT_LIST; do
  echo $FONT; 
  render "$TXT" "$FONT" $BORDER_THICK
done

######### render fix images
render A Andale-Mono $BORDER_THICK general_A.png
render "jim!" Andale-Mono $BORDER_NO general_jim.png
