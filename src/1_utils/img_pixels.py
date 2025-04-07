#!/usr/bin/env python3
# -*- coding: utf-8 -*-



def img_load_pixels(ImgPath):
    """return with one RGB matrix as the image representation.

    Grayscale images are converted to RGB, Alpha channel is neglected.
    """
    errors = []
    pixelsAllRow = []

    try:
        from PIL import Image
    except ImportError:
        errors.append("Missing PIL module: pillow, please install pillow: 'pip install pillow'")

    if not errors:
        imageLoaded = Image.open(ImgPath)

        ########################################
        colorModeCanBeUsed = False
        colorValSample = imageLoaded.getpixel((0, 0))

        if isinstance(colorValSample, int):
            colorModeCanBeUsed = True
        else:
            if isinstance(colorValSample, tuple):
                if len(colorValSample) >= 3: #rgb or rgba
                    colorModeCanBeUsed = True

        if not colorModeCanBeUsed:
            errors.append(f"in file {ImgPath} the color channel num is not 1 or 3 or higher. The image cannot be used")
        ########################################

        if not errors:
            imgWidth, imgHeight = imageLoaded.size

            for y in range(0, imgHeight):
                pixelRow = []
                for x in range(0, imgWidth):
                    colorVal= imageLoaded.getpixel((x, y))

                    # if it's a grayscale img, it is a simple int
                    # RGB:  3 elements are in the tuple
                    # RGBA: 4 elements are in the tuple
                    if isinstance(colorVal, int):
                        rgbDetected = (colorVal, colorVal, colorVal)
                    else:
                        rgbDetected = colorVal[0:3] # RGB value has 3 elems, RGBA has 4

                    pixelRow.append(rgbDetected)

                pixelsAllRow.append(pixelRow)

    return pixelsAllRow


