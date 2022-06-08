package main

import (
	"fmt"
	"image"
	"strings"
)

// TEST IT
// separate background from char_creator pixels is elemental.
// precondition: the background is homogeneus.
// R, G, B min/max values
// A color's RGBA method returns values in the range [0, 65535].
// 0: black
func background_detect_rgb_ranges() (pixint, pixint, pixint, pixint, pixint, pixint) {
	// fmt.Println("background detect ...")
	var maxGeneral pixint = 65535
	var minGeneral = maxGeneral - 45000
	// R min, R max - G min, G max - B min, B max
	// if a pixel is in these ranges, then it is in the backround.
	// else: it is a char_creator pixel
	return minGeneral, maxGeneral, minGeneral, maxGeneral, minGeneral, maxGeneral
}

var pixel_id_next = 0
func pixel_new_obj__no_neighbours(pixel_type string, x, y int, r, g, b pixint) Pixel {
	var pixel_now Pixel
	pixel_now.pixelType = pixel_type
	pixel_now.x = x
	pixel_now.y = y
	pixel_now.r = r
	pixel_now.g = g
	pixel_now.b = b
	pixel_now.inPixelGroup = false
	pixel_now.groupStarter = false
	pixel_now.id = pixel_id_next
	pixel_id_next++
	return pixel_now
}

var pixel_empty = pixel_empty_create()
func pixel_new__link_empty_neighbours(pixel_type string, x, y int, r, g, b pixint) Pixel {
	pixel_now := pixel_new_obj__no_neighbours(pixel_type, x, y, r, g, b)
	pixel_now.n1 = &pixel_empty
	pixel_now.n2 = &pixel_empty
	pixel_now.n3 = &pixel_empty
	pixel_now.n4 = &pixel_empty
	pixel_now.n5 = &pixel_empty
	pixel_now.n6 = &pixel_empty
	pixel_now.n7 = &pixel_empty
	pixel_now.n8 = &pixel_empty
	return pixel_now
}

func pixelmap_from_img(Img image.Image, bgRmin, bgRmax,
	bgGmin, bgGmax, bgBmin, bgBmax pixint) PixelMap {

	bounds := Img.Bounds()
	var pixelMap PixelMap

	// select a column (x value) and go down from line 0 to line last (y)
	fmt.Println("x min:", bounds.Min.X, "x max", bounds.Max.X)
	fmt.Println("y min:", bounds.Min.Y, "y max", bounds.Max.Y)
	for x := bounds.Min.X; x < bounds.Max.X; x++ {
		var pixelsColumn []Pixel
		for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
			// fmt.Println(">>> x", x, "y", y)
			rUint32, gUint32, bUint32, _ := Img.At(x, y).RGBA() // last value: a, alpha
			r := PixFromUInt32(rUint32)
			g := PixFromUInt32(gUint32)
			b := PixFromUInt32(bUint32)

			// if the current r,g,b is in background ranges than it's a background pixel
			if r >= bgRmin && r <= bgRmax && g >= bgGmin && g <= bgGmax && b >= bgBmin && b <= bgBmax {
				pixelNow := pixel_new__link_empty_neighbours("background", x, y, 0, 0, 0)
				pixelsColumn = append(pixelsColumn, pixelNow)
			} else { // not in the backround -> char_creator/active pixel
				pixelNow := pixel_new__link_empty_neighbours("char_creator", x, y, r, g, b)
				pixelsColumn = append(pixelsColumn, pixelNow)
			}
			// fmt.Println("pixelsColumn len", len(pixelsColumn))
		}

		// pack long vertical |||| blades into PixelMap
		pixelMap = append(pixelMap, pixelsColumn)
	}
	return pixelMap
}

func print_pixel_debug(pixel Pixel) string {
	return fmt.Sprintf("%d %d %d\n%d %d %d\n%d %d %d",
		(*pixel.n8).id, (*pixel.n1).id, (*pixel.n2).id,
		(*pixel.n7).id, pixel.id,       (*pixel.n3).id,
		(*pixel.n6).id, (*pixel.n5).id, (*pixel.n5).id)
}

func print_pixel_wide1(pixel Pixel) string {
	if pixel.pixelType == "char_creator" {
		return "*"
	} else {
		return " "
	}
}

func print_pixel_map(pixelMap PixelMap, mode string) {
	width := len(pixelMap)
	height := len(pixelMap[0])

	fun_represent_pixel := print_pixel_wide1 // this is the default print mode
	separator_x := ""
	separator_y := ""

	if mode == "debug" {
		fun_represent_pixel = print_pixel_debug
		separator_x = "|"
		separator_y = "-"
	}

	for y := 0; y < height; y++ {
		row := []string{}
		for x := 0; x < width; x++ {
			row = append(row, fun_represent_pixel(pixelMap[x][y]))
		}
		numlines := strings.Count(row[0], "\n") + 1

		char_used_horizontally := 0
		for lineInPixelOutput := 0; lineInPixelOutput < numlines; lineInPixelOutput++ {
			char_used_horizontally = 0
			for x := 0; x < width; x++ {
				displayed := strings.Split(row[x], "\n")[lineInPixelOutput]
				fmt.Print(displayed)
				fmt.Print(separator_x)
				char_used_horizontally += len(displayed) + len(separator_x)
			}
			fmt.Print("\n")
		}
		for x := 0; x < char_used_horizontally; x++ {
			fmt.Print(separator_y)
		}
		fmt.Print("\n")
	}
}

// select all pixels that is the part of the image
func pixel_groups_char_creators(Img image.Image, bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax pixint) {
	fmt.Println("char creators - select all pixel")

	pixelMap := pixelmap_from_img(Img, bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax)
	fmt.Println("len pixel map ", len(pixelMap))
	page := Page {pixelMapPointer: &pixelMap}

	// one pixel group is represented with one pixel-map
	pixel_groups_detect(&page)
	print_pixel_map(pixelMap, "wide1")


	fmt.Println("end")
}

func print_group_starters(page Page) {

	fmt.Println("=================== BEGIN ", len(page.pixelGroupStarters), " =====================" )
	// for id, pixel_GroupStarter_pointer := range page.pixelGroupStarters {
	// 	fmt.Println(id, "pixel group starter pointer: ", pixel_GroupStarter_pointer)
	// }
	fmt.Println("=================== END =====================" )
}

/* one group: character creator pixels that form one sign.
you can find a path with only character creator pixels between all group elems
- with other words you can walk from creator-pixel
to creator pixel and reach all group members,
because they are not separated
*/


// you can be sure that it returns with a pixel, if the coords is outside of it or not
func pixel_get_from_map(pixelMapPointer *PixelMap, x, y int) *Pixel {
	pixelMap := *pixelMapPointer
	pixelMapWidth, pixelMapHeight := pixel_map_get_w_h(pixelMap)
	if x >= 0 && x < pixelMapWidth {
		if y >= 0 && y < pixelMapHeight{
			return &pixelMap[x][y]
		}
	}
	pixelEmpty := pixel_empty_create()
	return &pixelEmpty
}

// active pixels only
func pixel_neighbours_linking__distance_1(pixelPointer *Pixel, page *Page) {
	/* neighbours coords:
	    812
	    7P3
	    654
	*/
	pixelMapPointer := (*page).pixelMapPointer
	pixel := *pixelPointer
	if pixel.pixelType != "char_creator" {return}

	pixelNeighbourPointer1 := pixel_get_from_map(pixelMapPointer, pixel.x,  pixel.y-1)
	pixelNeighbourPointer2 := pixel_get_from_map(pixelMapPointer, pixel.x+1, pixel.y-1)
	pixelNeighbourPointer3 := pixel_get_from_map(pixelMapPointer, pixel.x+1, pixel.y  )
	pixelNeighbourPointer4 := pixel_get_from_map(pixelMapPointer, pixel.x+1, pixel.y+1)
	pixelNeighbourPointer5 := pixel_get_from_map(pixelMapPointer, pixel.x  , pixel.y+1)
	pixelNeighbourPointer6 := pixel_get_from_map(pixelMapPointer, pixel.x-1, pixel.y+1)
	pixelNeighbourPointer7 := pixel_get_from_map(pixelMapPointer, pixel.x-1, pixel.y  )
	pixelNeighbourPointer8 := pixel_get_from_map(pixelMapPointer, pixel.x-1, pixel.y-1)

	// with this solution there is repetition in the code but the structure is visible.
	// if you refactor it, you will loose the structure.
	if pixelNeighbourPointer1.pixelType == "char_creator" {pixel.n1 = pixelNeighbourPointer1; (*pixelNeighbourPointer1).n5 = pixelPointer; (*pixelNeighbourPointer1).inPixelGroup = true}
	if pixelNeighbourPointer2.pixelType == "char_creator" {pixel.n2 = pixelNeighbourPointer2; (*pixelNeighbourPointer6).n6 = pixelPointer; (*pixelNeighbourPointer6).inPixelGroup = true}
	if pixelNeighbourPointer3.pixelType == "char_creator" {pixel.n3 = pixelNeighbourPointer3; (*pixelNeighbourPointer7).n7 = pixelPointer; (*pixelNeighbourPointer7).inPixelGroup = true}
	if pixelNeighbourPointer4.pixelType == "char_creator" {pixel.n4 = pixelNeighbourPointer4; (*pixelNeighbourPointer8).n8 = pixelPointer; (*pixelNeighbourPointer8).inPixelGroup = true}
	if pixelNeighbourPointer5.pixelType == "char_creator" {pixel.n5 = pixelNeighbourPointer5; (*pixelNeighbourPointer1).n1 = pixelPointer; (*pixelNeighbourPointer1).inPixelGroup = true}
	if pixelNeighbourPointer6.pixelType == "char_creator" {pixel.n6 = pixelNeighbourPointer6; (*pixelNeighbourPointer2).n2 = pixelPointer; (*pixelNeighbourPointer2).inPixelGroup = true}
	if pixelNeighbourPointer7.pixelType == "char_creator" {pixel.n7 = pixelNeighbourPointer7; (*pixelNeighbourPointer3).n3 = pixelPointer; (*pixelNeighbourPointer3).inPixelGroup = true}
	if pixelNeighbourPointer8.pixelType == "char_creator" {pixel.n8 = pixelNeighbourPointer8; (*pixelNeighbourPointer4).n4 = pixelPointer; (*pixelNeighbourPointer4).inPixelGroup = true}
}

func pixel_map_get_w_h(pixelMap PixelMap) (int, int) {
	width := len(pixelMap)
	height := len(pixelMap[0])
	return width, height
}

// TODO: test it
func pixel_group_link_pixels(x, y int, pagePointer *Page) {
	pixelMap := *pagePointer.pixelMapPointer
	pixelPointer := &pixelMap[x][y]

	if (*pixelPointer).pixelType != "char_creator" || (*pixelPointer).inPixelGroup{
		return
	}
	(*pixelPointer).groupStarter = true
	(*pixelPointer).inPixelGroup = true

	(*pagePointer).pixelGroupStarters = append((*pagePointer).pixelGroupStarters, pixelPointer)
	pixel_neighbours_linking__distance_1(pixelPointer, pagePointer)
}

func pixel_groups_detect(pagePointer *Page) {
	for x, column := range *pagePointer.pixelMapPointer {
		for y, _:= range column {
			pixel_group_link_pixels(x, y, pagePointer)
			print_group_starters(*pagePointer)
		}
	}
}
