package main

import (
	"fmt"
	"testing"
)

func Test_pixel_neighbours_linking(t *testing.T) {
	fmt.Println(" Test_pixel_neighbours_linking BEGINNING  ...")
	Img := Img_read_from_file("test/test_simple_ligature_fj.png")
	bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax := background_detect_rgb_ranges()
	pixelMap := pixels_char_creators_list__map_from_img(Img, bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax)
	page := Page {pixelMapPointer: &pixelMap}
	pixel_group_link_pixels(0, 3, &page)

	fmt.Println(" Test_pixel_neighbours_linking END  ...")
}