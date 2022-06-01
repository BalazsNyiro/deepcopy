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

var pixel_id_next = 0
func pixel_new(pixel_type string, x, y int, r, g, b pixint) Pixel {
	var pixel_now Pixel
	pixel_now.pixel_type = pixel_type
	pixel_now.x = x
	pixel_now.y = y
	pixel_now.r = r
	pixel_now.g = g
	pixel_now.b = b
	pixel_now.in_pixel_group = false
	pixel_now.id = pixel_id_next
	pixel_id_next++
	return pixel_now
}

func pixels_char_creators_list__map_from_img(Img image.Image, bgRmin, bgRmax,
	bgGmin, bgGmax, bgBmin, bgBmax pixint) PixelMap {

	bounds := Img.Bounds()
	var pixelMap PixelMap

	// select a column (x value) and go down from line 0 to line last (y)
	for x := bounds.Min.X; x < bounds.Max.X; x++ {
		var pixelsColumn Pixels
		for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
			fmt.Println("x", x, "y", y)
			rUint32, gUint32, bUint32, _ := Img.At(x, y).RGBA() // last value: a, alpha
			r := PixFromUInt32(rUint32)
			g := PixFromUInt32(gUint32)
			b := PixFromUInt32(bUint32)

			// if the current r,g,b is in background ranges than it's a background pixel
			if r >= bgRmin && r <= bgRmax && g >= bgGmin && g <= bgGmax && b >= bgBmin && b <= bgBmax {
				pixelNow := pixel_new("background", x, y, 0, 0, 0)
				pixelsColumn = append(pixelsColumn, pixelNow)
			} else { // not in the backround -> char_creator/active pixel
				pixelNow := pixel_new("char_creator", x, y, r, g, b)
				pixelsColumn = append(pixelsColumn, pixelNow)
			}
			fmt.Println("pixelsColumn len", len(pixelsColumn))
		}
		fmt.Printf("addr: %p", &pixelsColumn)

		// pack long vertical |||| blades into PixelMap
		pixelMap = append(pixelMap, pixelsColumn)
	}
	return pixelMap
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

	pixelMap := pixels_char_creators_list__map_from_img(Img, bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax)
	fmt.Println("len pixel map ", len(pixelMap))

	// one pixel group is represented with one pixel-map
	pixelGroups := pixel_groups_detect_in_map(pixelMap)
	pixel_map_print(pixelMap)

	for _, pixels := range pixelGroups {
		pixel_map_print(pixels_to_pixelmap(pixels))
	}
}

/* one group: character creator pixels that form one sign.
you can find a path with only character creator pixels between all group elems
- with other words you can walk from creator-pixel
to creator pixel and reach all group members,
because they are not separated
*/


// you can be sure that it returns with a pixel, if the coords is outside of it or not
func pixel_get_from_map(pixelMap PixelMap, x, y int) Pixel {
	pixelMapWidth, pixelMapHeight := pixel_map_get_w_h(pixelMap)
	if x >= 0 && x < pixelMapWidth {
		if y >= 0 && y < pixelMapHeight{
			return pixelMap[x][y]
		}
	}
	return pixel_empty()
}

func append_pixels(collector Pixels, new_elems Pixels) Pixels {
	for _, pixel := range new_elems {
		collector = append(collector, pixel)
	}
	return collector
}

// active pixels only
func pixel_neighbours_collect(pixel Pixel, pixelMap PixelMap) Pixels {
	// the coords: 0, 0 is left top corner, this is the natural,
	// because the detect of the columns happens from top to down
	/*  123
	    8P4
	    765
	*/
	neighbours := Pixels{}
	if pixel.pixel_type != "char_creator" {return neighbours} // don't collect empty pixel's neighbours

	p1 := pixel_get_from_map(pixelMap, pixel.x-1,pixel.y-1)
	p2 := pixel_get_from_map(pixelMap, pixel.x,  pixel.y-1)
	p3 := pixel_get_from_map(pixelMap, pixel.x+1,pixel.y-1)
	p4 := pixel_get_from_map(pixelMap, pixel.x+1,pixel.y  )
	p5 := pixel_get_from_map(pixelMap, pixel.x+1,pixel.y+1)
	p6 := pixel_get_from_map(pixelMap, pixel.x  ,pixel.y+1)
	p7 := pixel_get_from_map(pixelMap, pixel.x-1,pixel.y+1)
	p8 := pixel_get_from_map(pixelMap, pixel.x-1,pixel.y  )
	if p1.pixel_type == "char_creator" {neighbours = append(neighbours, p1)}
	if p2.pixel_type == "char_creator" {neighbours = append(neighbours, p2)}
	if p3.pixel_type == "char_creator" {neighbours = append(neighbours, p3)}
	if p4.pixel_type == "char_creator" {neighbours = append(neighbours, p4)}
	if p5.pixel_type == "char_creator" {neighbours = append(neighbours, p5)}
	if p6.pixel_type == "char_creator" {neighbours = append(neighbours, p6)}
	if p7.pixel_type == "char_creator" {neighbours = append(neighbours, p7)}
	if p8.pixel_type == "char_creator" {neighbours = append(neighbours, p8)}
	return neighbours
}

func pixel_group_detect(pixel Pixel, pixelMap PixelMap) Pixels {
	group_ids := make(map[int]bool)
	find_neighbours_ids := make(map[int]bool)

	group := Pixels{pixel}
	pixel.in_pixel_group = true
	group_ids[pixel.id] = true

	find_neighbours := Pixels{pixel}
	find_neighbours_ids[pixel.id] = true

	for len(find_neighbours) > 0 {
		// pop the last elem...
		id_last := len(find_neighbours) - 1
		pixel_now := find_neighbours[id_last]
		find_neighbours = find_neighbours[:id_last]
		delete(find_neighbours_ids, pixel_now.id)

		neighbours := pixel_neighbours_collect(pixel_now, pixelMap)

		neighbours_new := Pixels{} // select new elems
		for _, pixel_neighbour := range neighbours {
			_, in_group := group_ids[pixel_neighbour.id]
			if ! in_group {
				neighbours_new = append(neighbours_new, pixel_neighbour)
			}
		}

		for _, pixel_neighbour_new := range neighbours_new {
			group = append(group, pixel_neighbour_new)
			group_ids[pixel.id] = true
			pixel_neighbour_new.in_pixel_group = true
		}

		/*
		for _, pixel_neighbour_new := range neighbours_new {
			_, neighbours_tested := find_neighbours_ids[pixel_neighbour_new.id]
			if ! neighbours_tested{
				find_neighbours = append(find_neighbours, pixel_neighbour_new)
				find_neighbours_ids[pixel_neighbour_new.id] = true
			}
		}
		
		 */
	}
	return group
}
func pixel_map_get_w_h(pixelMap PixelMap) (int, int) {
	width := len(pixelMap)
	height := len(pixelMap[0])
	return width, height
}

func pixel_groups_detect_in_map(pixelMap PixelMap) PixelMap {
	var pixelGroups PixelMap

	// select the most lefts->top pixel in a group
	for x, column := range pixelMap {
		for y, pixel := range column {
			fmt.Println("XY:", x, y, pixel.pixel_type)
			if pixel.pixel_type == "char_creator" && ! pixel.in_pixel_group {
				fmt.Println("creator:", x, y)
				// pixelGroup := pixel_group_detect(pixel, pixelMap)
				//pixelGroups = append(pixelGroups, pixelGroup)
			}
			break
		}
	}

	return pixelGroups
}
