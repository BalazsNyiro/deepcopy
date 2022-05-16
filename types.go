package main

/* neighbours - the pixel can be linked with neighbours in 8 directions
123
9P4
765
*/

// recursive type def:
// https://stackoverflow.com/a/8261789
type Pixel struct {
	pixel_type string  // char_creator, background
	// n - neighbours (pointers):
	n1 *Pixel
	n2 *Pixel
	n3 *Pixel
	n4 *Pixel
	n5 *Pixel
	n6 *Pixel
	n7 *Pixel
	n8 *Pixel
	r  uint32
	g  uint32
	b  uint32
	x  uint32
	y  uint32
}

/*
func PixelNew(r, uint32, g, uint32, b, uint32, x uint32, y uint32) Pixel {
	return
}

*/
