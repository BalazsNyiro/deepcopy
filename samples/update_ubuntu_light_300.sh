
TEXT="$(cat update_text_default_abc_lower.txt)"
echo "sample text: $TEXT"
URL="https://fonts.google.com/specimen/Ubuntu?preview.text=$TEXT"
echo "URL: $URL"
google-chrome --headless --disable-gpu  --screenshot --window-size=2000,2000  --virtual-time-budget=15000  "$URL"

gm convert screenshot.png -crop 1000x90+300+950 sample_ubuntu_light_300.png

rm screenshot.png
