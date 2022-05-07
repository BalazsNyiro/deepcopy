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

// select all pixels that is the part of the image
func foreground_select_pixels(Img image.Image, bgRmin uint32, bgRmax uint32, bgGmin uint32, bgGmax uint32, bgBmin uint32, bgBmax uint32) {
	fmt.Println("foreground select all pixel")
	bounds := Img.Bounds()
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			// last value: a, alpha
			r, g, b, _ := Img.At(x, y).RGBA()

			if r >= bgRmin && r <= bgRmax && g >= bgGmin && g <= bgGmax && b >= bgBmin && b <= bgBmax {
				fmt.Println("foreground pixel")
			}
		}
	}
}
