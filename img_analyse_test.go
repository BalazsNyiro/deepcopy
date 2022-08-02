package main

import (
	"fmt"
	"testing"
)

func neighbours_linking_test_pixel_pairs(testId string, x, y int, direction string, targetX, targetY int, pixelMap PixelMap, t *testing.T) {
	neighbourId := pixelMap[x][y].n1.id
	if direction == "n2" { neighbourId = pixelMap[x][y].n2.id }
	if direction == "n3" { neighbourId = pixelMap[x][y].n3.id }
	if direction == "n4" { neighbourId = pixelMap[x][y].n4.id }
	if direction == "n5" { neighbourId = pixelMap[x][y].n5.id }
	if direction == "n6" { neighbourId = pixelMap[x][y].n6.id }
	if direction == "n7" { neighbourId = pixelMap[x][y].n7.id }
	if direction == "n8" { neighbourId = pixelMap[x][y].n8.id }

	if neighbourId != pixelMap[targetX][targetY].id {
		t.Fatalf("TestId %s - linking problem! %d,%d.%s.id = %d 0,1.id = %d",
			testId, x, y, direction, neighbourId, pixelMap[targetX][targetY].id)
	}
}

func Test_pixel_neighbours_linking(t *testing.T) {
	fmt.Println(" Test_pixel_neighbours_linking BEGINNING  ...")
	Img := Img_read_from_file("test/test_simple_H.png", 0)
	bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax := background_detect_rgb_ranges(0)
	pixelMap := pixelmap_from_img(Img, bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax, 0)
	page := Page {pixelMapPointer: &pixelMap}

	pixel_group_link_pixels(0, 0, &page, 0)
	print_pixel_map(pixelMap, "debug")

	neighbours_linking_test_pixel_pairs("neighbour_link_0_0_a", 0, 0, "n4", 1, 1, pixelMap, t)
	neighbours_linking_test_pixel_pairs("neighbour_link_0_0_b", 0, 0, "n5", 0, 1, pixelMap, t)

	// 0, 1 -> 0, 0 is tested previously
	neighbours_linking_test_pixel_pairs("neighbour_link_0_1_a", 0, 1, "n3", 1, 1, pixelMap, t)
	neighbours_linking_test_pixel_pairs("neighbour_link_0_1_b", 0, 1, "n5", 0, 2, pixelMap, t)

	neighbours_linking_test_pixel_pairs("neighbour_link_1_1_a", 1, 1, "n2", 2, 0, pixelMap, t)

	neighbours_linking_test_pixel_pairs("neighbour_link_2_0_a", 2, 0, "n5", 2, 1, pixelMap, t)
	neighbours_linking_test_pixel_pairs("neighbour_link_2_0_b", 2, 0, "n6", 1, 1, pixelMap, t)

	neighbours_linking_test_pixel_pairs("neighbour_link_2_1", 2, 1, "n7", 1, 1, pixelMap, t)

	neighbours_linking_test_pixel_pairs("neighbour_link_2_2_a", 2, 2, "n1", 2, 1, pixelMap, t)
	neighbours_linking_test_pixel_pairs("neighbour_link_2_2_b", 2, 2, "n8", 1, 1, pixelMap, t)
}