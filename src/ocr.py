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

    BgRedMax = BackgroundR + DeltaR
    BgRedMin = BackgroundR - DeltaR
    BgGreenMax = BackgroundG + DeltaG
    BgGreenMin = BackgroundG - DeltaG
    BgBlueMax = BackgroundB + DeltaB
    BgBlueMin = BackgroundB - DeltaB

    BgGrayMin = ColorBlockBackgroundGray - ColorBlockBackgroundGrayDelta
    BgGrayMax = ColorBlockBackgroundGray + ColorBlockBackgroundGrayDelta

    # find marks and remove backgrounds
    # print("Mark detection, Img dimensions:", Img["Width"], Img["Height"])
    RangeY = range(0, Img["Height"]) # create range only once
    for X in range(0, Img["Width"]):
        for Y in RangeY:
            PixelIsMark = False

            if is_rgb(Img):
                R, G, B = Img["Pixels"][(X, Y)]
                if R < BgRedMin or R > BgRedMax:
                    if G < BgGreenMin or G > BgGreenMax:
                        if B < BgBlueMin or B > BgBlueMax:
                            PixelIsMark = True

            elif is_grayscale(Img):
                GrayLevel = Img["Pixels"][(X, Y)]
                if GrayLevel < BgGrayMin or GrayLevel > BgGrayMax:
                    PixelIsMark = True
            else:
                print(util.ui_msg(Prg, "ocr.pixel_data_size_unknown"))
                sys.exit(1)

            if PixelIsMark:
                # print(PixelNowCoords, " -- MARK --> ", Img["Pixels"][(X, Y)])
                CoordsMarkPixels_and_parent_MarkId[(X, Y)] = None
                # MarkId is unknown by default

    Marks = dict()

    def markid_detect_possible_neighbour(Coord, MarkIdsPossible):
        # print("  possible? ", Coord)
        MarkIdNeighbour = CoordsMarkPixels_and_parent_MarkId.get(Coord, None)
        # same MarkId can be in more than one neighbour
        if MarkIdNeighbour is not None and MarkIdNeighbour not in MarkIdsPossible:
            MarkIdsPossible.append(MarkIdNeighbour)

    MarkIdNext = 0
    for Coord, MarkIdCurrentPixel in CoordsMarkPixels_and_parent_MarkId.items():
        if MarkIdCurrentPixel is None:
            # print("\n\nCoord now: ", Coord)
            MarkIdsPossible = []

            for CoordNeighbour in util.coords_neighbours(Coord):
                markid_detect_possible_neighbour(CoordNeighbour, MarkIdsPossible)

            if not MarkIdsPossible:
                MarkIdsPossible.append(MarkIdNext)
                MarkIdNext += 1

            MarkIdCurrentPixel = MarkIdsPossible[0]
            # print("Active coords", Coord, MarkId, MarkIdsPossible)
            if len(MarkIdsPossible) > 1:
                # we can connect more MarkIds into One.
                # Move all pixels into the first markId

                for CoordMaybeMoved, MarkIdBeforeMoving in CoordsMarkPixels_and_parent_MarkId.items():
                    if MarkIdBeforeMoving is not None:
                        if MarkIdBeforeMoving in MarkIdsPossible and MarkIdBeforeMoving != MarkIdCurrentPixel:
                            # print(" ", CoordMaybeMoved, MarkIdBeforeMoving, " id moving -> ", MarkId)
                            CoordsMarkPixels_and_parent_MarkId[CoordMaybeMoved] = MarkIdCurrentPixel
                            Marks[MarkIdCurrentPixel][CoordMaybeMoved] = True

                for MarkIdNotMoreUsed in MarkIdsPossible[1:]:
                    del Marks[MarkIdNotMoreUsed]

            if MarkIdCurrentPixel not in Marks:
                Marks[MarkIdCurrentPixel] = dict()
            Marks[MarkIdCurrentPixel][Coord] = True

            CoordsMarkPixels_and_parent_MarkId[Coord] = MarkIdCurrentPixel


    print("num of Mark pixels: ", len(CoordsMarkPixels_and_parent_MarkId) )

    # the keys can be missing: [0, 2, 3]
    MarkReturn = dict()
    Id = 0
    for Val in Marks.values(): # here the keys will be re-setted: 0, 1, 2
        MarkReturn[Id] = Val
        Id += 1
    return MarkReturn

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

def is_rgb(Img):
    if Img["PixelDataSize"] == 3:
        return True
    return False

def is_grayscale(Img):
    if Img["PixelDataSize"] == 1:
        return True
    return False
