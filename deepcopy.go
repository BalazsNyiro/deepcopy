package main

import (
	"fmt"
)

func main() {
	fmt.Print("deepcopy")
	Img := Img_read_from_file("test/general_jim.png")
	bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax := background_detect_rgb_ranges()
	page := pixel_groups_linking_in_page(Img, bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax)

	fmt.Println("==== PIXEL MAP POINTER PRINT ====")
	print_pixel_map(*page.pixelMapPointer, "wide1")
	print_group_starter_pixels(page)

}
