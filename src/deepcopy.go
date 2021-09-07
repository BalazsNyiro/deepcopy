package main

import (
	_ "image/jpeg"
	_ "image/png"
)

func main() {
	Img := img_read_from_file("./test/test_mark_finding_word_the__font_ubuntu_24pt.png")
	Histogram := histogram_create(Img)
	histogram_result_print(Histogram)
}
