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

    CoordsMarkPixels_and_parent_MarkId = dict()

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
                CoordsMarkPixels_and_parent_MarkId[(X,Y)] = None
                # MarkId is unknown by default

    Marks = dict()
    for Coord, MarkId in CoordsMarkPixels_and_parent_MarkId.items():
        X, Y = Coord
        print("Active coords", Coord)
        if not MarkId:

            # if a neighbour elem has MarkId, use the same.
            # in Python 3.8 you can assign (X-1, Y)  to a variable
            if   (X-1, Y) in CoordsMarkPixels_and_parent_MarkId and CoordsMarkPixels_and_parent_MarkId[(X-1, Y)]:
                MarkId = CoordsMarkPixels_and_parent_MarkId[(X-1, Y)]

            elif (X-1, Y-1) in CoordsMarkPixels_and_parent_MarkId and CoordsMarkPixels_and_parent_MarkId[(X-1, Y-1)]:
                MarkId = CoordsMarkPixels_and_parent_MarkId[(X-1, Y-1)]

            elif (X,   Y-1) in CoordsMarkPixels_and_parent_MarkId and CoordsMarkPixels_and_parent_MarkId[(X,   Y-1)]:
                MarkId = CoordsMarkPixels_and_parent_MarkId[(X,   Y-1)]

            elif (X+1, Y-1) in CoordsMarkPixels_and_parent_MarkId and CoordsMarkPixels_and_parent_MarkId[(X+1, Y-1)]:
                MarkId = CoordsMarkPixels_and_parent_MarkId[(X+1, Y-1)]

            elif (X+1, Y  ) in CoordsMarkPixels_and_parent_MarkId and CoordsMarkPixels_and_parent_MarkId[(X+1, Y  )]:
                MarkId = CoordsMarkPixels_and_parent_MarkId[(X+1, Y  )]

            elif (X+1, Y+1) in CoordsMarkPixels_and_parent_MarkId and CoordsMarkPixels_and_parent_MarkId[(X+1, Y+1)]:
                MarkId = CoordsMarkPixels_and_parent_MarkId[(X+1, Y+1)]

            elif (X,   Y+1) in CoordsMarkPixels_and_parent_MarkId and CoordsMarkPixels_and_parent_MarkId[(X,   Y+1)]:
                MarkId = CoordsMarkPixels_and_parent_MarkId[(X,   Y+1)]

            elif (X-1, Y+1) in CoordsMarkPixels_and_parent_MarkId and CoordsMarkPixels_and_parent_MarkId[(X-1, Y+1)]:
                MarkId = CoordsMarkPixels_and_parent_MarkId[(X-1, Y+1)]

            elif (X-1, Y-1) in CoordsMarkPixels_and_parent_MarkId and CoordsMarkPixels_and_parent_MarkId[(X-1, Y-1)]:
                MarkId = CoordsMarkPixels_and_parent_MarkId[(X-1, Y-1)]

            else:
                MarkId = len(Marks.keys())+1

            Marks[MarkId] = {Coord: True}
            CoordsMarkPixels_and_parent_MarkId[Coord] = MarkId

    print("num of Mark pixels: ", len(CoordsMarkPixels_and_parent_MarkId) )
    print("total / mark pixel ratio: ", X*Y / len(CoordsMarkPixels_and_parent_MarkId))

    print("Num of Marks:", len(Marks.keys()))

    mark_display_on_console(Marks[1])
    return Marks


def mark_display_on_console(Mark):
    print(Mark)
