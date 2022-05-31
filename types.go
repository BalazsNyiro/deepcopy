package main

/* neighbours - the pixel can be linked with neighbours in 8 directions
123
9P4
765
*/
type Pixels []Pixel
type PixelMap []Pixels    // 2 dimensional representation of more pixels } || or list of (pixels)
type PixelMaps []PixelMap // more than one pixel map
type pixint uint32

func PixFromUInt32(i uint32) pixint { return pixint(i) }

// recursive type def:
// https://stackoverflow.com/a/8261789
type Pixel struct {

	/* background pixel: everything that doesn't hold active information, meaning.
	   I use char_creator instead of foreground, because if you have a colored
	   terminal output, a red and a yellow colored text both can be char_creator.
	so typically the background color range is a solid fix value,
	but the letters/chars can be created from different colored elems
	*/
	pixel_type string // char_creator, background, empty
	// n - neighbours (pointers):
	n1             *Pixel
	n2             *Pixel
	n3             *Pixel
	n4             *Pixel
	n5             *Pixel
	n6             *Pixel
	n7             *Pixel
	n8             *Pixel
	r              pixint
	g              pixint
	b              pixint
	x              int
	y              int
	pixel_group    int
	in_pixel_group bool
	id             int // a simple unique integer for all pixel
}
func pixels_find_min_max_coords(pixels Pixels) (int, int, int, int) {
	x_min, x_max, y_min, y_max := 0, 0, 0, 0
	for _, pixel := range pixels {
		if pixel.x < x_min { x_min = pixel.x }
		if pixel.x > x_max { x_max = pixel.x }
		if pixel.y < y_min { y_min = pixel.y }
		if pixel.y > y_max { y_max = pixel.y }
	}
	return x_min, x_max, y_min, y_max
}
func pixel_empty() Pixel {
	return pixel_new("empty", 0, 0, 0, 0, 0)
}
func pixelmap_new(width, height int) PixelMap{
	pixelEmpty := pixel_empty()
	var pixelMap PixelMap
	for x := 0; x < width; x++ {
		var pixelsColumn Pixels
		for y := 0; y < height; y++ {
			pixelsColumn = append(pixelsColumn, pixelEmpty)
		}
		pixelMap = append(pixelMap, pixelsColumn)
	}
	return pixelMap
}

func pixels_to_pixelmap(pixels Pixels) PixelMap {
	x_min, x_max, y_min, y_max := pixels_find_min_max_coords(pixels)
	pixelMap := pixelmap_new(x_max - x_min + 1, y_max - y_min + 1)
	for _, pixel := range pixels {
		pixelMap[pixel.x][pixel.y] = pixel
	}
	return pixelMap
}
