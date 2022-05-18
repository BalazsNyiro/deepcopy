package main

import (
	"fmt"
	"image"
)

// TEST IT
// separate background from foreground is elemental.
// precondition: the background is homogeneus.
// R, G, B min/max values
// A color's RGBA method returns values in the range [0, 65535].
// 0: black
func background_detect_rgb_ranges() (uint32, uint32, uint32, uint32, uint32, uint32) {
	fmt.Println("background detect ...")
	var maxGeneral uint32 = 65535
	var minGeneral = maxGeneral - 45000
	// R min, R max - G min, G max - B min, B max
	// if a pixel is in these ranges, then it is in the backround.
	// else: foreground
	return minGeneral, maxGeneral, minGeneral, maxGeneral, minGeneral, maxGeneral
}
func pixel_new(pixel_type string, x, y, r, g, b uint32) Pixel {
	var pixel_now Pixel
	pixel_now.pixel_type = pixel_type
	pixel_now.x = x
	pixel_now.y = y
	pixel_now.r = r
	pixel_now.g = g
	pixel_now.b = b
	return pixel_now
}

func pixel_list_and_layer_from_img(Img image.Image, bgRmin uint32, bgRmax uint32,
	bgGmin uint32, bgGmax uint32, bgBmin uint32, bgBmax uint32) (PixelList, PixelMap) {

	bounds := Img.Bounds()
	var pixelMap PixelMap
	var pixels_all PixelList

	// select a column (x value) and go down from line 0 to line last (y)
	for x := bounds.Min.X; x < bounds.Max.X; x++ {
		var pixels_column PixelList
		for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
			fmt.Println("x", x, "y", y)
			r, g, b, _ := Img.At(x, y).RGBA() // last value: a, alpha

			// if the current r,g,b is in background ranges than it's a background pixel
			if r >= bgRmin && r <= bgRmax && g >= bgGmin && g <= bgGmax && b >= bgBmin && b <= bgBmax {
				pixel_now := pixel_new("background", uint32(x), uint32(y), 0, 0, 0)
				pixels_column = append(pixels_column, pixel_now)
			} else { // not in the backround -> char_creator/active pixel
				pixel_now := pixel_new("char_creator", uint32(x), uint32(y), r, g, b)
				pixels_column = append(pixels_column, pixel_now)
				pixels_all = append(pixels_all, pixel_now)
				// fmt.Println("foreground pixel")
			}
			fmt.Println("pixels_column len", len(pixels_column))
		}
		fmt.Printf("addr: %p", &pixels_column)

		// pack long vertical |||| blades into PixelMap
		pixelMap = append(pixelMap, pixels_column)
	}
	return pixels_all, pixelMap
}

func pixel_map_print(pixelMap PixelMap) {
	width := len(pixelMap)
	height := len(pixelMap[0])
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			if pixelMap[x][y].pixel_type == "char_creator" {
				fmt.Print("*")
			} else {
				fmt.Print(" ")
			}
		}
		fmt.Print("\n")
	}
}

// select all pixels that is the part of the image
func pixel_groups_foreground(Img image.Image, bgRmin uint32, bgRmax uint32, bgGmin uint32, bgGmax uint32, bgBmin uint32, bgBmax uint32) {
	fmt.Println("foreground select all pixel")

	pixelsForeground, pixelMap := pixel_list_and_layer_from_img(Img, bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax)
	fmt.Println("\nlen pixel foreground", len(pixelsForeground))
	fmt.Println("len pixel map ", len(pixelMap))

	pixel_map_print(pixelMap)
}
