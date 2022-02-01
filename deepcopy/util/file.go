package util

import (
	"errors"
	"fmt"
	"image"
	_ "image/jpeg"
	_ "image/png"
	"log"
	"os"
)

type TypeHistogram [16][4]int

func Img_read_from_file(FileName string) image.Image {
	reader, err := os.Open(FileName)
	if err != nil {
		log.Fatal(err)
	}
	ImageFromFile, _, err := image.Decode(reader)
	if err != nil {
		log.Fatal(err)
	}
	reader.Close()
	return ImageFromFile
}

func Histogram_create(Img image.Image) TypeHistogram {
	bounds := Img.Bounds()
	// based on: https://pkg.go.dev/image@go1.17  (respect)

	// Calculate a 16-bin Histogram for m's red, green, blue and alpha components.
	//
	// An image's bounds do not necessarily start at (0, 0), so the two loops start
	// at bounds.Min.Y and bounds.Min.X. Looping over Y first and X second is more
	// likely to result in better memory access patterns than X first and Y second.
	var Histogram TypeHistogram
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			r, g, b, a := Img.At(x, y).RGBA()
			// A color's RGBA method returns values in the range [0, 65535].
			// Shifting by 12 reduces this to the range [0, 15].
			Histogram[r>>12][0]++
			Histogram[g>>12][1]++
			Histogram[b>>12][2]++
			Histogram[a>>12][3]++
		}
	}
	return Histogram
}

func Histogram_result_print(Histogram TypeHistogram) {
	fmt.Printf("%-14s %6s %6s %6s %6s\n", "bin", "red", "green", "blue", "alpha")
	for i, x := range Histogram {
		fmt.Printf("0x%04x-0x%04x: %6d %6d %6d %6d\n", i<<12, (i+1)<<12-1, x[0], x[1], x[2], x[3])
	}
}

func Dir_exists(Path string) bool {
	if _, err := os.Stat(Path); os.IsNotExist(err) {
		return false
	}
	return true
}

// TODO: create /tmp/test/test.txt
//              if you set chmod 0000 /tmp/test, this fun can say that the file exists == true
// check file existence:
// https://stackoverflow.com/questions/12518876/how-to-check-if-a-file-exists-in-go
func File_exists(Path string) bool {
	if _, err := os.Stat("/path/to/whatever"); err == nil {
		// path/to/whatever exists
		return true
	} else if errors.Is(err, os.ErrNotExist) {
		// path/to/whatever does *not* exist
		return false
	} else {
		// Schrodinger: file may or may not exist. See err for details.
		// Therefore, do *NOT* use !os.IsNotExist(err) to test for file existence
		fmt.Printf("File exist, unknown error:", err)
		return false
	}
}
