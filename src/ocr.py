import util, sys

def text_block_analyse(Prg,
                       PositionStart=(0,0),
                       ColorBlockBackgroundRgb=(255, 255, 255),
                       ColorBlockBackgroundRgbDelta=(30, 30, 30),
                       ColorBlockBackgroundGray=30,
                       ColorBlockBackgroundGrayDelta=30,
                       ScanDirectionHorizontal="from_left_to_righ",
                       ScanDirectionVertical="from_top_to_bottom"
                       ):
    # I want to handle RGB or Grayscale images only,
    # so I handle 3 or 1 color channels
    print("Selected Image Id", Prg["ImageIdSelected"])
    Img = Prg["ImagesLoaded"][Prg["ImageIdSelected"]]
    print("Img width, height: ", Img["Width"], Img["Height"])

    CoordsMaybeMarks = []
    DeltaR, DeltaG, DeltaB = ColorBlockBackgroundRgbDelta
    BackgroundR, BackgroundG, BackgroundB = ColorBlockBackgroundRgb

    RedMax = BackgroundR + DeltaR
    RedMin = BackgroundR - DeltaR
    GreenMax = BackgroundG + DeltaG
    GreenMin = BackgroundG - DeltaG
    BlueMax = BackgroundB + DeltaB
    BlueMin = BackgroundB - DeltaB

    GrayMin = ColorBlockBackgroundGray - ColorBlockBackgroundGrayDelta
    GrayMax = ColorBlockBackgroundGray + ColorBlockBackgroundGrayDelta

    # find marks and remove backgrounds
    for X in range(0, Img["Width"]):
        for Y in range(0, Img["Height"]):

            PixelIsMark = False
            PixelNowCoords = (-1, -1)

            if Img["PixelDataSize"] == 3: # if RGB
                R, G, B = Img["Pixels"][(X, Y)]

                if R < RedMin or R > RedMax:
                    if G < GreenMin or G > GreenMax:
                        if B < BlueMin or B > BlueMax:
                            PixelIsMark = True
                            PixelNowCoords = (X, Y)

            elif Img["PixelDataSize"] == 1:  # if grayscale
                GrayLevel = Img["Pixels"][(X, Y)]
                if GrayLevel < GrayMin or GrayLevel > GrayMax:
                    PixelIsMark = True
                    PixelNowCoords = (X, Y)
            else:
                print(util.ui_msg(Prg, "ocr.pixel_data_size_unknown"))
                sys.exit(1)

            if PixelIsMark:
                print(PixelNowCoords, ">>>", Img["Pixels"][(X, Y)])

