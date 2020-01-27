# -*- coding: utf-8 -*-
import util, sys
import mark_util


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

    print("TODO: convert marks to text")
    print(mark_util.mark_to_string(Prg, Marks[1]))

# the root dir is the program's parent dir
# TESTED
def mark_collect_from_img_file(Prg, FilePathElems):
    FilePathElems = [Prg["DirPrgParent"], *FilePathElems]
    Img, _ImgId = util.img_load_into_prg_structure__get_imgid(Prg, FilePathElems)
    Marks = mark_collect_from_img_object(Prg, Img)
    return Marks

# TESTED with mark_collect_from_img_file
def mark_collect_from_img_object(Prg, Img,
                                 ColorBlockBackgroundRgb=(255, 255, 255),
                                 ColorBlockBackgroundRgbDelta=(30, 30, 30),
                                 ColorBlockBackgroundGray=30,
                                 ColorBlockBackgroundGrayDelta=30,
                                 ):

    # Ink Pixel: a pixel that is not in background: wanted/detected foreground pixel
    # Ink is shorter name than Foreground so I chose that
    InkPixelCoords_and_MarkId = mark_pixels_select_from_img(Prg, Img,
                                                       ColorBlockBackgroundRgb, ColorBlockBackgroundRgbDelta,
                                                       ColorBlockBackgroundGray, ColorBlockBackgroundGrayDelta)
    Marks = dict()
    MarkIdIfNoNeighbour = 0

    for Coord, MarkIdCurrentPixel in InkPixelCoords_and_MarkId.items():

        MarkIdsInNeighbourhood, MarkIdIfNoNeighbour = \
            mark_ids_collect_from_neighbourhood(Coord, MarkIdIfNoNeighbour,
                                                InkPixelCoords_and_MarkId)

        MarkIdCurrentPixel = MarkIdsInNeighbourhood.pop(0) # select first id from the possible list

        # we can connect more than one MarkIds from the neighbourhood
        # so this pixel merge more separated marks into one new
        mark_ids_set_for_pixels(Marks, MarkIdCurrentPixel,
                                InkPixelCoords_and_MarkId,
                                MarkIdsInNeighbourhood, Img, Coord)

    print("num of Mark pixels: ", len(InkPixelCoords_and_MarkId))

    return Marks

# TESTED
def mark_ids_set_for_pixels(Marks, MarkIdCurrentPixel,
                            InkPixelCoords_and_MarkId,
                            MarkIdsInNeighbourhood, Img, Coord):
    ##########################
    # set id for current pixel:
    if MarkIdCurrentPixel not in Marks:
        Marks[MarkIdCurrentPixel] = {"Coords": dict()}

    # store original pixel's color info. If Img is RGB, its (R,G,B), if Gray, it's 0-255 int
    # THIS IS THE MAIN STRUCTURE OF A MARK:
    # [id]["Coords"][(1,2)]=pixelValue
    Marks[MarkIdCurrentPixel]["Coords"][Coord] = Img["Pixels"][Coord]

    InkPixelCoords_and_MarkId[Coord] = MarkIdCurrentPixel

    ##########################
    # set id for neighbours
    if MarkIdsInNeighbourhood:
        for CoordMaybeMoved, MarkIdBeforeMoving in InkPixelCoords_and_MarkId.items():
            if MarkIdBeforeMoving is not None:
                if MarkIdBeforeMoving in MarkIdsInNeighbourhood:
                    # print(" ", CoordMaybeMoved, MarkIdBeforeMoving, " id moving -> ", MarkId)
                    InkPixelCoords_and_MarkId[CoordMaybeMoved] = MarkIdCurrentPixel

                    # copy the color value of the pixel to the new place
                    Marks[MarkIdCurrentPixel]["Coords"][CoordMaybeMoved] = Marks[MarkIdBeforeMoving]["Coords"][CoordMaybeMoved]

        # we can delete the old MarkId at the end because more than one pixel can belong to one MarkId
        for MarkIdNotMoreUsed in MarkIdsInNeighbourhood:
            del Marks[MarkIdNotMoreUsed]
    ##########################


# return with new MarkIdNext if it used the original one
# TESTED
def mark_ids_collect_from_neighbourhood(Coord, MarkIdIfNoNeighbour,
                                        InkPixelCoords_and_MarkId):
    MarkIdsInNeighbourhood = []  # if in the neighbours are a known mark, connect the current pixel into that mark

    for CoordNeighbour in util.coords_neighbours(Coord):
        markid_of_coord_append_if_unknown(CoordNeighbour,
                                          MarkIdsInNeighbourhood,
                                          InkPixelCoords_and_MarkId)
    if not MarkIdsInNeighbourhood:
        MarkIdsInNeighbourhood.append(MarkIdIfNoNeighbour)
        MarkIdIfNoNeighbour += 1

    return MarkIdsInNeighbourhood, MarkIdIfNoNeighbour

# TESTED
def mark_pixels_select_from_img(Prg, Img,
                                ColorBlockBackgroundRgb,
                                ColorBlockBackgroundRgbDelta,
                                ColorBlockBackgroundGray,
                                ColorBlockBackgroundGrayDelta):

    if not util.is_rgb(Img) and not util.is_grayscale(Img):
        print(util.ui_msg(Prg, "ocr.pixel_data_size_unknown"))
        PixelDataSize = Img.get("PixelDataSize", -1)
        sys.exit(PixelDataSize)

    InkPixels_and_MarkId = dict()
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

    if util.is_rgb(Img):
        def is_mark(Img, X, Y):
            if is_mark_rgb(Img, X, Y, BgRedMin, BgRedMax, BgGreenMin, BgGreenMax, BgBlueMin, BgBlueMax):
                return True
            return False

    if util.is_grayscale(Img):
        def is_mark(Img, X, Y):
            if is_mark_grayscale(Img, X, Y, BgGrayMin, BgGrayMax):
                return True
            return False

    for X in range(0, Img["Width"]):
        for Y in range(0, Img["Height"]):
            if is_mark(Img, X, Y):
                InkPixels_and_MarkId[(X, Y)] = None

    return InkPixels_and_MarkId

# display func, tested with usage

# TESTED, here we know that CoordNeighbour is next to our current pixel
def markid_of_coord_append_if_unknown(Coord, MarkIds, PixelCoords_and_MarkId):
    # print("  possible? ", Coord)
    MarkIdNeighbour = PixelCoords_and_MarkId.get(Coord, None)
    # same MarkId can be in more than one neighbour
    if MarkIdNeighbour is not None and MarkIdNeighbour not in MarkIds:
        MarkIds.append(MarkIdNeighbour)


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
