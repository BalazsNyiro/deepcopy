package main

import (
	"fmt"
)

/*
 The goal: collect all pixel groups

*/
func main() {
	trace("main", ">", 0)
	fmt.Print("deepcopy")
	Img := Img_read_from_file("test/general_jim.png", 0)
	bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax := background_detect_rgb_ranges(0)

	page := pixel_groups_linking_in_page(Img, bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax, 0)
	// page.pixelGroupStarters is filled!
	pixel_groups_collect_pixels(page)

	// NEXT TASK: I'd like to know the list of pixels in a group

	fmt.Println("==== PIXEL MAP POINTER PRINT ====")
	print_pixel_map(*page.pixelMapPointer, "wide1")
	print_group_starter_pixels(page)
	trace("main", "<", 0)
}
