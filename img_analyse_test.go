package main

import (
	"fmt"
	"testing"
)

func linking_test(testId string, x, y int, neighbour string, targetX, targetY int, pixelMap PixelMap, t *testing.T) {
	neighbourId := pixelMap[x][y].n1.id
	if neighbour == "n2" { neighbourId = pixelMap[x][y].n2.id }
	if neighbour == "n3" { neighbourId = pixelMap[x][y].n3.id }
	if neighbour == "n4" { neighbourId = pixelMap[x][y].n4.id }
	if neighbour == "n5" { neighbourId = pixelMap[x][y].n5.id }
	if neighbour == "n6" { neighbourId = pixelMap[x][y].n6.id }
	if neighbour == "n7" { neighbourId = pixelMap[x][y].n7.id }
	if neighbour == "n8" { neighbourId = pixelMap[x][y].n8.id }

	if neighbourId != pixelMap[targetX][targetY].id {
		t.Fatalf("TestId %s - linking problem! %d,%d.%s.id = %d 0,1.id = %d",
			testId, x, y, neighbour, neighbourId, pixelMap[targetX][targetY].id)
	}

}

func Test_pixel_neighbours_linking(t *testing.T) {
	fmt.Println(" Test_pixel_neighbours_linking BEGINNING  ...")
	Img := Img_read_from_file("test/test_simple_H.png")
	bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax := background_detect_rgb_ranges()
	pixelMap := pixelmap_from_img(Img, bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax)
	page := Page {pixelMapPointer: &pixelMap}

	pixel_group_link_pixels(0, 0, &page)
	print_pixel_map(pixelMap, "debug")

	linking_test("neighbour_link_0_0 a", 0, 0, "n4", 1, 1, pixelMap, t)
	linking_test("neighbour_link_0_0 b", 0, 0, "n5", 0, 1, pixelMap, t)

	linking_test("neighbour_link_0_1", 0, 1, "n5", 0, 2, pixelMap, t)



}