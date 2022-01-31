package main

import (
	"deepcopy/util"
	"fmt"
	_ "image/jpeg"
	_ "image/png"
)

func main() {
	Img := util.Img_read_from_file("../test/test_mark_finding_word_the__font_ubuntu_24pt.png")
	Histogram := util.Histogram_create(Img)
	util.Histogram_result_print(Histogram)

	fmt.Print("\ndir exists:", util.Dir_exists("/tmp"))
	fmt.Print("\ndir not exists:", util.Dir_exists("/tmp_unknown"))
}
