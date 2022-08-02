package main

import (
	"image"
	_ "image/jpeg"
	_ "image/png"
	"log"
	"os"
)

func Img_read_from_file(FileName string, callerLevel int) image.Image {
	trace("Img_read_from_file", ">", callerLevel+1)
	reader, err := os.Open(FileName)
	if err != nil {
		log.Fatal(err)
	}
	ImageFromFile, _, err := image.Decode(reader)
	if err != nil {
		log.Fatal(err)
	}
	reader.Close()
	trace("Img_read_from_file", "<", callerLevel+1)
	return ImageFromFile
}

func trace(funcName string, direction string, depth int) {
	var skippedFuncs	 = []string{
		"pixel_group_link_pixels",
		"pixel_neighbours_linking__distance_1"}
	for _, skipThis := range skippedFuncs {
		if skipThis == funcName {
			return
		}
	}

	prefix := ""
	for i := 0; i<depth; i++{
		prefix += " "
	}
	arrow := ">>> "
	if direction == "<" { arrow = "<<< "}

	txt := prefix + arrow + funcName

	f, err := os.OpenFile("trace.txt", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatal(err)
	}
	if _, err := f.Write([]byte(txt + "\n")); err != nil {
		log.Fatal(err)
	}
	if err := f.Close(); err != nil {
		log.Fatal(err)
	}
}
