package main

import (
	"fmt"
	_ "image/jpeg"
	_ "image/png"
)

func main() {
	fmt.Print("deepcopy")
	Img := Img_read_from_file("test/general_A.png")
	/*
		Histogram := Histogram_create(Img)
		Histogram_result_print(Histogram)
		fmt.Print("\ndir exists:", Dir_exists("/tmp"))
		fmt.Print("\ndir not exists:", Dir_exists("/tmp_unknown"))
		fmt.Print("\nfile exists:", Dir_exists("/tmp/test/test.txt"))
	*/
	bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax := background_detect_rgb_ranges()
	foreground_select_pixels(Img, bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax)
}
