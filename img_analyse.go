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
	pixel_now.neighboursLinkingExecuted = false
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

			pixel_type := "background"

			// if the current r,g,b is in background ranges than it's a background pixel
			if r >= bgRmin && r <= bgRmax && g >= bgGmin && g <= bgGmax && b >= bgBmin && b <= bgBmax {
				// r, g, b are in the background ranges - pass, nothing happens
			} else { // not in the backround -> char_creator/active pixel
				pixel_type = "char_creator"
			}
			pixelNow := pixel_new__link_empty_neighbours(pixel_type, x, y, r, g, b)
			pixelsColumn = append(pixelsColumn, pixelNow)
			// fmt.Println("pixelsColumn len", len(pixelsColumn))
		}

		// pack long vertical |||| blades into PixelMap
		pixelMap = append(pixelMap, pixelsColumn)
	}
	return pixelMap
}

func print_pixel_debug(pixel Pixel) string {
	if ! pixel.IsCharCreator(){
		return "     \n     \n     "
	}
	p1_id := pixel.n1.id
	p2_id := pixel.n2.id
	p3_id := pixel.n3.id
	p4_id := pixel.n4.id
	p5_id := pixel.n5.id
	p6_id := pixel.n6.id
	p7_id := pixel.n7.id
	p8_id := pixel.n8.id
	return fmt.Sprintf("%d %d %d\n%d %d %d\n%d %d %d",
		p8_id, p1_id,    p2_id,
		p7_id, pixel.id, p3_id,
		p6_id, p5_id,    p4_id)
}

func print_pixel_wide1(pixel Pixel) string {
	if pixel.pixelType == "char_creator" {
		return "*"
	} else {
		return " "
	}
}
func numbering_rows(rowNum int, numOfLinesInInfo int) string {
	numbering := fmt.Sprintf("% 3d", rowNum)
	var out string
	for i :=0; i < numOfLinesInInfo; i++ {
		if len(out) > 0 {
			out = out + "\n"
		}
		out = out + numbering
	}
	return out
}

func print_pixel_map(pixelMap PixelMap, mode string) {
	width := len(pixelMap)
	height := len(pixelMap[0])

	fun_represent_pixel := print_pixel_wide1 // this is the default print mode
	separator_vertical := ""
	separator_horizontal := ""

	if mode == "debug" {
		fun_represent_pixel = print_pixel_debug
		separator_vertical = "|"
		separator_horizontal = "-"
	}

	samplePixelInfoToCountNewlines := fun_represent_pixel(pixelMap[0][0])
	numLinesInInfo := strings.Count(samplePixelInfoToCountNewlines, "\n") + 1

	for y := 0; y < height; y++ {
		row := []string{numbering_rows(y, numLinesInInfo)}
		for x := 0; x < width; x++ {
			row = append(row, fun_represent_pixel(pixelMap[x][y]))
		}

		char_used_horizontally := 0
		for lineInPixelOutput := 0; lineInPixelOutput < numLinesInInfo; lineInPixelOutput++ {
			char_used_horizontally = 0
			for x := 0; x < width; x++ {
				displayed := strings.Split(row[x], "\n")[lineInPixelOutput]
				fmt.Print(displayed)
				fmt.Print(separator_vertical)
				char_used_horizontally += len(displayed) + len(separator_vertical)
			}
			fmt.Print("\n")
		}

		separator_horizontal_used := false
		for x := 0; x < char_used_horizontally; x++ {
			fmt.Print(separator_horizontal)
			separator_horizontal_used = true
		}
		if separator_horizontal_used && len(separator_horizontal) > 0  {
			fmt.Print("\n") // if something was displayed as row separator,
			                // create newline again
		}
	}
}

// link connected pixels to each other
// important: here a pixel knows only his nearest neighbours.
// so a pixel doesn't know all other pixels in the same group at this point.
func pixel_groups_linking_in_page(Img image.Image, bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax pixint) Page {
	fmt.Println("char creators - select all pixel")

	pixelMap := pixelmap_from_img(Img, bgRmin, bgRmax, bgGmin, bgGmax, bgBmin, bgBmax)
	fmt.Println("len pixel map ", len(pixelMap))
	page := Page {pixelMapPointer: &pixelMap}

	// one pixel group is represented with one pixel-map
	pixel_groups_link_all_pixels(&page)

	return page
}

func print_group_starter_pixels(page Page) {

	fmt.Println("=================== num of pixelgroup starters: ", len(page.pixelGroupStarters), " =====================" )
	for id, pixelGroupStarterPointer := range page.pixelGroupStarters {
	 	fmt.Println(id, "pixel group starter pixel: ", pixelGroupStarterPointer.x, pixelGroupStarterPointer.y)
	}
	fmt.Println("=================== END =====================" )
}

/* one group: character creator pixels that form one sign.
you can find a path with only character creator pixels between all group elems
- with other words you can walk from creator-pixel
to creator pixel and reach all group members,
because they are not separated
*/


// you can be sure that it returns with a pixel, if the coords is outside of it or not
func pixel_pointer_get_from_map(pixelMapPointer *PixelMap, x, y int) *Pixel {
	pixelMap := *pixelMapPointer
	pixelMapWidth, pixelMapHeight := pixel_map_get_w_h(*pixelMapPointer)
	if x >= 0 && x < pixelMapWidth {
		if y >= 0 && y < pixelMapHeight{
			return &pixelMap[x][y]
		}
	}
	pixelEmpty := pixel_empty_create()
	return &pixelEmpty
}

// active pixels only
func pixel_neighbours_linking__distance_1(pixelPointer *Pixel, pagePointer *Page,
	                                      pixelsInGroupPointer *[]Pixel) {
	/* neighbours coords:
	    812
	    7P3
	    654
	*/
	if ! pixelPointer.IsCharCreator() { return }
	if pixelPointer.neighboursLinkingExecuted { return }
	pixelPointer.neighboursLinkingExecuted = true

	pixelMapPointer := pagePointer.pixelMapPointer

	pixelNeighbourPointer1 := pixel_pointer_get_from_map(pixelMapPointer, pixelPointer.x,  pixelPointer.y-1)
	pixelNeighbourPointer2 := pixel_pointer_get_from_map(pixelMapPointer, pixelPointer.x+1, pixelPointer.y-1)
	pixelNeighbourPointer3 := pixel_pointer_get_from_map(pixelMapPointer, pixelPointer.x+1, pixelPointer.y  )
	pixelNeighbourPointer4 := pixel_pointer_get_from_map(pixelMapPointer, pixelPointer.x+1, pixelPointer.y+1)
	pixelNeighbourPointer5 := pixel_pointer_get_from_map(pixelMapPointer, pixelPointer.x  , pixelPointer.y+1)
	pixelNeighbourPointer6 := pixel_pointer_get_from_map(pixelMapPointer, pixelPointer.x-1, pixelPointer.y+1)
	pixelNeighbourPointer7 := pixel_pointer_get_from_map(pixelMapPointer, pixelPointer.x-1, pixelPointer.y  )
	pixelNeighbourPointer8 := pixel_pointer_get_from_map(pixelMapPointer, pixelPointer.x-1, pixelPointer.y-1)

	// with this solution there is repetition in the code but the structure is visible.
	// if you refactor it, you will loose the structure.
	neighbour := pixelNeighbourPointer1; if neighbour.IsCharCreator() { pixelPointer.n1 = pixelNeighbourPointer1; neighbour.n5 = pixelPointer; neighbour.inPixelGroup = true}
	neighbour =  pixelNeighbourPointer2; if neighbour.IsCharCreator() { pixelPointer.n2 = pixelNeighbourPointer2; neighbour.n6 = pixelPointer; neighbour.inPixelGroup = true}
	neighbour =  pixelNeighbourPointer3; if neighbour.IsCharCreator() { pixelPointer.n3 = pixelNeighbourPointer3; neighbour.n7 = pixelPointer; neighbour.inPixelGroup = true}
	neighbour =  pixelNeighbourPointer4; if neighbour.IsCharCreator() { pixelPointer.n4 = pixelNeighbourPointer4; neighbour.n8 = pixelPointer; neighbour.inPixelGroup = true}
	neighbour =  pixelNeighbourPointer5; if neighbour.IsCharCreator() { pixelPointer.n5 = pixelNeighbourPointer5; neighbour.n1 = pixelPointer; neighbour.inPixelGroup = true}
	neighbour =  pixelNeighbourPointer6; if neighbour.IsCharCreator() { pixelPointer.n6 = pixelNeighbourPointer6; neighbour.n2 = pixelPointer; neighbour.inPixelGroup = true}
	neighbour =  pixelNeighbourPointer7; if neighbour.IsCharCreator() { pixelPointer.n7 = pixelNeighbourPointer7; neighbour.n3 = pixelPointer; neighbour.inPixelGroup = true}
	neighbour =  pixelNeighbourPointer8; if neighbour.IsCharCreator() { pixelPointer.n8 = pixelNeighbourPointer8; neighbour.n4 = pixelPointer; neighbour.inPixelGroup = true}

	if ! pixelNeighbourPointer1.neighboursLinkingExecuted { pixel_neighbours_linking__distance_1(pixelNeighbourPointer1, pagePointer, pixelsInGroupPointer) }
	if ! pixelNeighbourPointer2.neighboursLinkingExecuted { pixel_neighbours_linking__distance_1(pixelNeighbourPointer2, pagePointer, pixelsInGroupPointer) }
	if ! pixelNeighbourPointer3.neighboursLinkingExecuted { pixel_neighbours_linking__distance_1(pixelNeighbourPointer3, pagePointer, pixelsInGroupPointer) }
	if ! pixelNeighbourPointer4.neighboursLinkingExecuted { pixel_neighbours_linking__distance_1(pixelNeighbourPointer4, pagePointer, pixelsInGroupPointer) }
	if ! pixelNeighbourPointer5.neighboursLinkingExecuted { pixel_neighbours_linking__distance_1(pixelNeighbourPointer5, pagePointer, pixelsInGroupPointer) }
	if ! pixelNeighbourPointer6.neighboursLinkingExecuted { pixel_neighbours_linking__distance_1(pixelNeighbourPointer6, pagePointer, pixelsInGroupPointer) }
	if ! pixelNeighbourPointer7.neighboursLinkingExecuted { pixel_neighbours_linking__distance_1(pixelNeighbourPointer7, pagePointer, pixelsInGroupPointer) }
	if ! pixelNeighbourPointer8.neighboursLinkingExecuted { pixel_neighbours_linking__distance_1(pixelNeighbourPointer8, pagePointer, pixelsInGroupPointer) }
}

func pixel_map_get_w_h(pixelMap PixelMap) (int, int) {
	width := len(pixelMap)
	height := len(pixelMap[0])
	return width, height
}

//  Test_pixel_neighbours_linking
func pixel_group_link_pixels(x, y int, pagePointer *Page) {
	pixelMap := *pagePointer.pixelMapPointer
	pixelPointer := &pixelMap[x][y]

	if ! pixelPointer.IsCharCreator() || pixelPointer.inPixelGroup{
		return
	}
	pixelPointer.groupStarter = true
	pixelPointer.inPixelGroup = true

	pixelsInGroup := []Pixel{}
	pagePointer.pixelGroupStarters = append(pagePointer.pixelGroupStarters, pixelPointer)
	pixel_neighbours_linking__distance_1(pixelPointer, pagePointer, &pixelsInGroup)
	_=pixelsInGroup
	// TODO: use the collected pixel list
	return
}

func pixel_groups_link_all_pixels(pagePointer *Page) {
	for x, column := range *pagePointer.pixelMapPointer {
		for y, _:= range column {
			pixel_group_link_pixels(x, y, pagePointer)
		}
	}
}
