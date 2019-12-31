import util, sys

def text_block_analyse(Prg,
                       PositionStart=(0, 0),
                       ScanDirectionHorizontal="from_left_to_righ",
                       ScanDirectionVertical="from_top_to_bottom"
                       ):

    # I want to handle RGB or Grayscale images only,
    # so I handle 3 or 1 color channels
    print("Selected Image Id", Prg["ImageIdSelected"])
    Img = Prg["ImagesLoaded"][Prg["ImageIdSelected"]]
    print("Img width, height: ", Img["Width"], Img["Height"])

    Marks = mark_collect(Prg, Img)
    print("Num of Marks:", len(Marks.keys()))
    mark_display_on_console(Marks[1])

def mark_collect(  Prg, Img,
                   ColorBlockBackgroundRgb=(255, 255, 255),
                   ColorBlockBackgroundRgbDelta=(30, 30, 30),
                   ColorBlockBackgroundGray=30,
                   ColorBlockBackgroundGrayDelta=30,
                   ):

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
                print(PixelNowCoords, " -- MARK --> ", Img["Pixels"][(X, Y)])
                CoordsMarkPixels_and_parent_MarkId[(X,Y)] = None
                # MarkId is unknown by default

    Marks = dict()

    def markid_detect_possible_neighbour(Coord, MarkIdsPossible):
        MarkIdNeighbour = CoordsMarkPixels_and_parent_MarkId.get(Coord, None)
        if MarkIdNeighbour: MarkIdsPossible.append(MarkIdNeighbour)

    for Coord, MarkId in CoordsMarkPixels_and_parent_MarkId.items():
        X, Y = Coord
        # print("Active coords", Coord)
        if not MarkId:
            MarkIdsPossible = []

            CoordLeftUp  = (X-1, Y-1); CoordLeft  = (X-1, Y); CoordLeftDown = (X-1, Y+1)
            CoordRightUp = (X+1, Y-1); CoordRight = (X+1, Y); CoordRightDown = (X+1, Y+1)

            CoordUp = (X, Y-1); CoordDown = (X, Y+1)

            markid_detect_possible_neighbour(CoordLeftUp,    MarkIdsPossible)
            markid_detect_possible_neighbour(CoordLeft,      MarkIdsPossible)
            markid_detect_possible_neighbour(CoordLeftDown,  MarkIdsPossible)
            markid_detect_possible_neighbour(CoordRightUp,   MarkIdsPossible)
            markid_detect_possible_neighbour(CoordRight,     MarkIdsPossible)
            markid_detect_possible_neighbour(CoordRightDown, MarkIdsPossible)
            markid_detect_possible_neighbour(CoordUp,        MarkIdsPossible)
            markid_detect_possible_neighbour(CoordDown,      MarkIdsPossible)
            if not MarkIdsPossible:
                MarkIdsPossible.append(len(Marks.keys())+1)

            MarkId = MarkIdsPossible[0]

            if len(MarkIdsPossible) > 1:
                # we can connect more MarkIds into One.
                # Move all pixels into the first markId
                for CoordMaybeMoved, MarkIdBeforeMoving in CoordsMarkPixels_and_parent_MarkId.items():
                    if MarkIdBeforeMoving in MarkIdsPossible:
                        CoordsMarkPixels_and_parent_MarkId[CoordMaybeMoved] = MarkId

            if MarkId not in Marks:
                Marks[MarkId] = dict()
            Marks[MarkId][Coord] = True

            CoordsMarkPixels_and_parent_MarkId[Coord] = MarkId

    print("num of Mark pixels: ", len(CoordsMarkPixels_and_parent_MarkId) )
    print("total / mark pixel ratio: ", X*Y / len(CoordsMarkPixels_and_parent_MarkId))

    return Marks

def mark_display_on_console(Mark):
    Xmin = None
    Ymin = None
    Xmax = None
    Ymax = None
    # Determine Xmin, Ymin
    for Coord in Mark:
        X, Y = Coord
        if Xmin is None:
            Xmin = X
            Ymin = Y
            Xmax = X
            Ymax = Y
        if X < Xmin: Xmin = X
        if Y < Ymin: Ymin = Y
        if X > Xmax: Xmax = X
        if Y > Ymax: Ymax = Y

    # print("Xmin, Ymin, Xmax, Ymax", Xmin, Ymin, Xmax, Ymax)
    RowNum = Ymax - Ymin + 1
    ColumnNum = Xmax - Xmin + 1
    OneRowTemplate = "." * ColumnNum + "\n"
    Rows = (OneRowTemplate * RowNum).split()
    #print("\n".join(Rows))

    #print("RowNum:", RowNum)
    #print("ColumnNum:", ColumnNum)

    for Coord in Mark:
        X, Y = Coord
        Xrelative = X - Xmin
        Yrelative = Y - Ymin
        Rows[Yrelative] = Rows[Yrelative][:Xrelative] + "O" + Rows[Yrelative][Xrelative+1:]
        # print(Xrelative, Yrelative)

    print("\n".join(Rows) + "\n")
