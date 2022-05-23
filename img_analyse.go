package main

import (
	"fmt"
	"image"
)

// TEST IT
// separate background from char_creator pixels is elemental.
// precondition: the background is homogeneus.
// R, G, B min/max values
// A color's RGBA method returns values in the range [0, 65535].
// 0: black
func background_detect_rgb_ranges() (pixint, pixint, pixint, pixint, pixint, pixint) {
	fmt.Println("background detect ...")
	var maxGeneral pixint = 65535
	var minGeneral = maxGeneral - 45000
	// R min, R max - G min, G max - B min, B max
	// if a pixel is in these ranges, then it is in the backround.
	// else: it is a char_creator pixel
	return minGeneral, maxGeneral, minGeneral, maxGeneral, minGeneral, maxGeneral
}
func pixel_new(pixel_type string, x, y, r, g, b pixint) Pixel {
	var pixel_now Pixel
	pixel_now.pixel_type = pixel_type
	pixel_now.x = x
	pixel_now.y = y
	pixel_now.r = r
	pixel_now.g = g
	pixel_now.b = b
	return pixel_now
}

func pixels_char_creators_list__layer_from_img(Img image.Image, bgRmin, bgRmax,
	bgGmin, bgGmax, bgBmin, bgBmax pixint) (PixelList, PixelMap) {

	bounds := Img.Bounds()
	var pixelMap PixelMap
	var pixels_all PixelList

	// select a column (x value) and go down from line 0 to line last (y)
	for x := bounds.Min.X; x < bounds.Max.X; x++ {
		var pixels_column PixelList
		for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
			fmt.Println("x", x, "y", y)
			rUint32, gUint32, bUint32, _ := Img.At(x, y).RGBA() // last value: a, alpha
			r := PixFromUInt32(rUint32)
			g := PixFromUInt32(gUint32)
			b := PixFromUInt32(bUint32)

			// if the current r,g,b is in background ranges than it's a background pixel
			if r >= bgRmin && r <= bgRmax && g >= bgGmin && g <= bgGmax && b >= bgBmin && b <= bgBmax {
				pixel_now := pixel_new("background", PixFromInt(x), PixFromInt(y), 0, 0, 0)
				pixels_column = append(pixels_column, pixel_now)
			} else { // not in the backround -> char_creator/active pixel
				pixel_now := pixel_new("char_creator", PixFromInt(x), PixFromInt(y), r, g, b)
				pixels_column = append(pixels_column, pixel_now)
				pixels_all = append(pixels_all, pixel_now)
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
func pixel_groups_char_creators(Img image.Image, bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax pixint) {
	fmt.Println("char creators - select all pixel")

	pixelsCharCreators, pixelMap := pixels_char_creators_list__layer_from_img(Img, bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax)
	fmt.Println("\nlen pixelCharCreators", len(pixelsCharCreators))
	fmt.Println("len pixel map ", len(pixelMap))

	pixel_map_print(pixelMap)
}
