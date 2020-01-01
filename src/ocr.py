import util, sys, os

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

    Marks = mark_collect_from_img_object(Prg, Img)
    print("Num of Marks:", len(Marks.keys()))
    mark_display_on_console(Prg, Marks[1])

# the root dir is the program's parent dir
def mark_collect_from_img_file(Prg, FilePathElems):
    FilePathImg = os.path.join(Prg["DirPrgParent"], *FilePathElems)
    ImgId = util.img_generate_id_for_loaded_list(Prg, PreFix="thumbnail", PostFix=FilePathImg)
    util.img_load_into_prg_structure(Prg, FilePathImg, ImgId)
    Img = Prg["ImagesLoaded"][ImgId]
    Marks = mark_collect_from_img_object(Prg, Img)
    return Marks


def mark_collect_from_img_object(Prg, Img,
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
                # print(PixelNowCoords, " -- MARK --> ", Img["Pixels"][(X, Y)])
                CoordsMarkPixels_and_parent_MarkId[(X,Y)] = None
                # MarkId is unknown by default

    Marks = dict()

    def markid_detect_possible_neighbour(Coord, MarkIdsPossible):
        # print("  possible? ", Coord)
        MarkIdNeighbour = CoordsMarkPixels_and_parent_MarkId.get(Coord, None)
        # same MarkId can be in more than one neighbour
        if MarkIdNeighbour is not None and MarkIdNeighbour not in MarkIdsPossible:
            MarkIdsPossible.append(MarkIdNeighbour)

    for Coord, MarkId in CoordsMarkPixels_and_parent_MarkId.items():
        X, Y = Coord
        if MarkId is None:
            # print("\n\nCoord now: ", Coord)
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
                MarkIdsPossible.append(len(Marks.keys()))

            MarkId = MarkIdsPossible[0]

            # print("Active coords", Coord, MarkId, MarkIdsPossible)
            if len(MarkIdsPossible) > 1:
                # print("  MarkId moving")

                # we can connect more MarkIds into One.
                # Move all pixels into the first markId

                # in this example we move id_1 to id_1, in this case don't move  the id
                #   (2, 11) 1  id moving ->  1
                #   (3, 11) 1  id moving ->  1
                #   (4, 11) 1  id moving ->  1
                #   (5, 6) 2  id moving ->  1
                #   (5, 7) 2  id moving ->  1
                #   (5, 8) 2  id moving ->  1
                #   (5, 9) 2  id moving ->  1
                for CoordMaybeMoved, MarkIdBeforeMoving in CoordsMarkPixels_and_parent_MarkId.items():
                    if MarkIdBeforeMoving in MarkIdsPossible and MarkIdBeforeMoving != MarkId:
                        # print(" ", CoordMaybeMoved, MarkIdBeforeMoving, " id moving -> ", MarkId)
                        CoordsMarkPixels_and_parent_MarkId[CoordMaybeMoved] = MarkId
                        Marks[MarkId][CoordMaybeMoved] = True

                for MarkIdNotMoreUsed in MarkIdsPossible[1:]:
                    del Marks[MarkIdNotMoreUsed]

            if MarkId not in Marks:
                Marks[MarkId] = dict()
            Marks[MarkId][Coord] = True

            CoordsMarkPixels_and_parent_MarkId[Coord] = MarkId


    print("num of Mark pixels: ", len(CoordsMarkPixels_and_parent_MarkId) )
    print("total / mark pixel ratio: ", X*Y / len(CoordsMarkPixels_and_parent_MarkId))

    return Marks

def mark_display_on_console(Prg, Mark):
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

    return "\n".join(Rows)
