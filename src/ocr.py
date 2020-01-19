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
    mark_to_string(Prg, Marks[1])

# the root dir is the program's parent dir
# TESTED
def mark_collect_from_img_file(Prg, FilePathElems):
    FilePathImg = os.path.join(Prg["DirPrgParent"], *FilePathElems)
    ImgId = util.img_generate_id_for_loaded_list(Prg, PreFix="thumbnail", PostFix=FilePathImg)
    util.img_load_into_prg_structure(Prg, FilePathImg, ImgId)
    Img = Prg["ImagesLoaded"][ImgId]
    Marks = mark_collect_from_img_object(Prg, Img)
    return Marks

# TESTED with mark_collect_from_img_file
def mark_collect_from_img_object(Prg, Img,
                                 ColorBlockBackgroundRgb=(255, 255, 255),
                                 ColorBlockBackgroundRgbDelta=(30, 30, 30),
                                 ColorBlockBackgroundGray=30,
                                 ColorBlockBackgroundGrayDelta=30,
                                 ):

    CoordsMarkPixels_and_parent_MarkId = mark_pixels_select_from_img(Img,
                                                                     ColorBlockBackgroundRgbDelta, ColorBlockBackgroundRgb,
                                                                     ColorBlockBackgroundGray, ColorBlockBackgroundGrayDelta)
    Marks = dict()
    MarkIdDefault = 0

    for Coord, MarkIdCurrentPixel in CoordsMarkPixels_and_parent_MarkId.items():
        if MarkIdCurrentPixel is None: # MarkId can be 0!!! so check with is-None

            MarkIdsInNeighbourhood, MarkIdDefault = \
                mark_ids_collect_from_neighbourhood(Coord, MarkIdDefault,
                                                    CoordsMarkPixels_and_parent_MarkId)

            MarkIdCurrentPixel = MarkIdsInNeighbourhood.pop(0) # select first id from the possible list

            if MarkIdsInNeighbourhood: # if there are more than the selected one possible Id:
                # we can connect more MarkIds into One.
                # Move all pixels into the first markId

                for CoordMaybeMoved, MarkIdBeforeMoving in CoordsMarkPixels_and_parent_MarkId.items():
                    if MarkIdBeforeMoving is not None:
                        if MarkIdBeforeMoving in MarkIdsInNeighbourhood:
                            # print(" ", CoordMaybeMoved, MarkIdBeforeMoving, " id moving -> ", MarkId)
                            CoordsMarkPixels_and_parent_MarkId[CoordMaybeMoved] = MarkIdCurrentPixel
                            Marks[MarkIdCurrentPixel][CoordMaybeMoved] = True

                for MarkIdNotMoreUsed in MarkIdsInNeighbourhood:
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


# return with new MarkIdNext if it used the original one
# TODO: TEST IT
def mark_ids_collect_from_neighbourhood(Coord, MarkIdDefault,
                                        CoordsMarkPixels_and_parent_MarkId):
    MarkIdsInNeighbourhood = []  # if in the neighbours are a known mark, connect the current pixel into that mark

    for CoordNeighbour in util.coords_neighbours(Coord):
        markid_detect_possible_neighbour_marks(CoordNeighbour,
                                               MarkIdsInNeighbourhood,
                                               CoordsMarkPixels_and_parent_MarkId)
    if not MarkIdsInNeighbourhood:
        MarkIdsInNeighbourhood.append(MarkIdDefault)
        MarkIdDefault += 1

    return MarkIdsInNeighbourhood, MarkIdDefault

# TODO: TEST IT
def mark_pixels_select_from_img(Img,
                                ColorBlockBackgroundRgbDelta,
                                ColorBlockBackgroundRgb,
                                ColorBlockBackgroundGray,
                                ColorBlockBackgroundGrayDelta):

    if not is_rgb(Img) and not is_grayscale(Img):
        print(util.ui_msg(Prg, "ocr.pixel_data_size_unknown"))
        sys.exit(1)

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

    RangeX = range(0, Img["Width"])
    RangeY = range(0, Img["Height"])
    if is_rgb(Img):
        for X in RangeX:
            for Y in RangeY:
                if is_mark_rgb(Img, X, Y, BgRedMin, BgRedMax, BgGreenMin, BgGreenMax, BgBlueMin, BgBlueMax):
                    CoordsMarkPixels_and_parent_MarkId[(X, Y)] = None

    if is_grayscale(Img):
        for X in RangeX:
            for Y in RangeY:
                if is_mark_grayscale(Img, X, Y, BgGrayMin, BgGrayMax):
                    CoordsMarkPixels_and_parent_MarkId[(X, Y)] = None

    return CoordsMarkPixels_and_parent_MarkId

# display func, tested with usage
def mark_to_string(Prg, Mark):
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


# TODO: write test
def markid_detect_possible_neighbour_marks(Coord, MarkIdsPossible, CoordsMarkPixels_and_parent_MarkId):
    # print("  possible? ", Coord)
    MarkIdNeighbour = CoordsMarkPixels_and_parent_MarkId.get(Coord, None)
    # same MarkId can be in more than one neighbour
    if MarkIdNeighbour is not None and MarkIdNeighbour not in MarkIdsPossible:
        MarkIdsPossible.append(MarkIdNeighbour)


# TESTED
# where we call it, we know that it is a grayscale img
def is_mark_grayscale(Img, X, Y, BgGrayMin, BgGrayMax):
    # We have a Background Color, Delta pairs -> Min, Max
    # are calculate from the color+delta, color-delta values
    # if something between the range, it belongs to background colors
    # if a value is out of range of background color, it's a foreground color
    GrayLevel = Img["Pixels"][(X, Y)]
    if GrayLevel < BgGrayMin or GrayLevel > BgGrayMax:
        return True
    return False



# where we call it, we know that it is an rgb image
# if the pixel in BG range the it's a background color
# it handles ONE Background colour. on a scanned page where
# theoretically the background is white and the printed letters
# are black, it's enough.

# If you have more than one background color, you have to
# call it more than once to check all color range
# Tested
def is_mark_rgb(Img, X, Y, BgRedMin, BgRedMax, BgGreenMin, BgGreenMax, BgBlueMin, BgBlueMax, PrintRgb=False, PrintRetVal=False):
    R, G, B = Img["Pixels"][(X, Y)]
    if PrintRgb:
        print("is mark rgb: ", R, G, B)
    if R < BgRedMin or R > BgRedMax:
        if G < BgGreenMin or G > BgGreenMax:
            if B < BgBlueMin or B > BgBlueMax:
                if PrintRetVal:
                    print("is_mark_rgb ret val: True")
                return True

    if PrintRetVal:
        print("is_mark_rgb ret val: False")
    return False

# TESTED
def is_rgb(Img):
    Size = Img.get("PixelDataSize", -1)
    if Size == 3:
        return True
    return False

# TESTED
def is_grayscale(Img):
    Size = Img.get("PixelDataSize", -1)
    if Size == 1:
        return True
    return False
