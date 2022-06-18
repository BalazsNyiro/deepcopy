package main

import (
	"fmt"
)

func main() {
	fmt.Print("deepcopy")
	Img := Img_read_from_file("test/general_A_thin.png")
	bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax := background_detect_rgb_ranges()
	pixel_groups_char_creators(Img, bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax)

	/*
		Histogram := Histogram_create(Img)
		Histogram_result_print(Histogram)
		fmt.Print("\ndir exists:", Dir_exists("/tmp"))
		fmt.Print("\ndir not exists:", Dir_exists("/tmp_unknown"))
		fmt.Print("\nfile exists:", Dir_exists("/tmp/test/test.txt"))

	fmt.Println("POINTER TEST")
	pixel_test := pixel_new__link_empty_neighbours("char_creator", 1, 2, 3, 4, 5)
	fmt.Println("1a pixel_test.x", pixel_test.x)
	pixel_test_pointer := &pixel_test
	pixel_test_2 := *pixel_test_pointer
	pixel_test.x = -111
	fmt.Println("1b pixel_test.x", pixel_test.x)
	pixel_test_2.x = -2
	fmt.Println("2 pixel_test.x", pixel_test.x)
	fmt.Println("2 pixel_test_2.x", pixel_test_2.x)
	fmt.Println("pointerprint pixel_test_pp.x", pixel_test_pointer.x)
	print_pixel_debug(*pixel_test_pointer)
	*/
}
