package main

/* neighbours - the pixel can be linked with neighbours in 8 directions
123
9P4
765
*/
type Pixels []Pixel
type PixelMap []Pixels
type PixelMaps []PixelMap // more than one pixel map
type pixint uint32

func PixFromInt(i int) pixint       { return pixint(uint32(i)) }
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
	pixel_type string // char_creator, background
	// n - neighbours (pointers):
	n1 *Pixel
	n2 *Pixel
	n3 *Pixel
	n4 *Pixel
	n5 *Pixel
	n6 *Pixel
	n7 *Pixel
	n8 *Pixel
	r  pixint
	g  pixint
	b  pixint
	x  pixint
	y  pixint
}
