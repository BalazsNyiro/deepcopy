package main

import (
	"fmt"
	_ "image/jpeg"
	_ "image/png"
)

func main() {
	fmt.Print("deepcopy")
	Img := Img_read_from_file("test/test_mark_finding_word_the__font_ubuntu_24pt.png")
	Histogram := Histogram_create(Img)
	Histogram_result_print(Histogram)

	fmt.Print("\ndir exists:", Dir_exists("/tmp"))
	fmt.Print("\ndir not exists:", Dir_exists("/tmp_unknown"))
	fmt.Print("\nfile exists:", Dir_exists("/tmp/test/test.txt"))
}
