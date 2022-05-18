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
	var minGeneral uint32 = maxGeneral - 45000
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

	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		var pixels_row PixelList
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			fmt.Println("x", x, "y", y)
			r, g, b, _ := Img.At(x, y).RGBA() // last value: a, alpha
			if r >= bgRmin && r <= bgRmax && g >= bgGmin && g <= bgGmax && b >= bgBmin && b <= bgBmax {
				pixel_now := pixel_new("char_creator", uint32(x), uint32(y), r, g, b)
				pixels_row = append(pixels_row, pixel_now)
				pixels_all = append(pixels_all, pixel_now)
				// fmt.Println("foreground pixel")
			} else {
				pixel_now := pixel_new("background", uint32(x), uint32(y), 0, 0, 0)
				pixels_row = append(pixels_row, pixel_now)
			}
			fmt.Println("pixels_row len", len(pixels_row))
		}
		fmt.Printf("addr: %p", &pixels_row)
		pixelMap = append(pixelMap, pixels_row)
	}
	return pixels_all, pixelMap
}

/*
 pixelMap has lines/rows
	0: [a, b, c, d, e, f, g, h]
	1: [a, b, c, d, e, f, g, h]
	1: [a, b, c, d, e, f, g, h]
in one line, the pixels are in order: 0-> a, 1->b, 2->c

if you want to reach this: x=2, y=1:
 pixelMap[1][2] because read row 1 (go down) and
 in the row read the 2->c value.
*/
func pixel_map_print(pixelMap PixelMap) {
	fmt.Println("PRINT len pixel map ", len(pixelMap))
	for y := 0; y < len(pixelMap); y++ {
		row := pixelMap[y]
		// fmt.Println("PRINT y", y)
		// fmt.Println("PRINT row len:", len(row))
		for x := 0; x < len(row); x++ {
			char := " "
			if pixelMap[y][x].pixel_type == "char_creator" {
				char = "*"
			}
			// fmt.Println("pixel map", "x", x, "y", y, char)
			fmt.Print(char)
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
