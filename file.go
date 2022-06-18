package main

import (
	"image"
	_ "image/jpeg"
	_ "image/png"
	"log"
	"os"
)

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

