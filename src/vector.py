# -*- coding: utf-8 -*-
import mark_util, area

# return: block exists, PixelWithProblem(Coords or None)
# TESTED
def block_exist_in_coords(Coords, XTopLeft, YTopLeft, XBottomRight, YBottomRight):
    CoordsOfBlock = []
    for XMaybe in range(XTopLeft, XBottomRight + 1):
        for YMaybe in range(YTopLeft, YBottomRight + 1):
            if (XMaybe, YMaybe) not in Coords:
                return (False, (XMaybe, YMaybe), [])
                # Block doesnt exist, PixelWithProblem
            CoordsOfBlock.append((XMaybe, YMaybe))

    return (True, None, CoordsOfBlock) # Block exists, No Problem

# TESTED directly
def block_nonoverlap_search_in_mark(Mark):
    BlockWidthMax = min(Mark["Width"], Mark["Height"])
    print("Block max width:", BlockWidthMax)

    BlocksInMark = {}
    CoordsTry = dict(Mark["Coords"])

    def coordinates_possible_block(Coord, BlockWidth):
        XTopLeft, YTopLeft = Coord
        XBottomRight = XTopLeft + BlockWidth - 1
        YBottomRight = YTopLeft + BlockWidth - 1
        return XTopLeft, YTopLeft, XBottomRight, YBottomRight

    def coords_delete(Coords, CoordsDeleted):
        for CoordDel in CoordsDeleted:
            print("  del:", CoordDel)
            del Coords[CoordDel]

    def blocks_in_mark_save(BlockWidth, BlocksInMark, CoordsOfBlock):
        if BlockWidth not in BlocksInMark:
            BlocksInMark[BlockWidth] = []
        BlocksInMark[BlockWidth].append(CoordsOfBlock)

    for BlockWidth in range(BlockWidthMax, 0, -1):
        print("\nBlockWidth: ", BlockWidth) # 4, 3, 2, 1

        # CoordsTry has to be a dict because we delete elements during the cycle
        for Coord in dict(CoordsTry).keys(): # duplicate Coords because it changes in the cycle
            if Coord not in CoordsTry: continue # runtime we delete from Coords

            XTopLeft, YTopLeft, XBottomRight, YBottomRight = coordinates_possible_block(Coord, BlockWidth)
            print(" Coord >", Coord, XTopLeft, YTopLeft, XBottomRight, YBottomRight )

            BlockExists, _FirstProblem, CoordsOfBlock = \
                block_exist_in_coords(CoordsTry, XTopLeft, YTopLeft, XBottomRight, YBottomRight)

            if BlockExists:
                print("  CoordsOfBlock", CoordsOfBlock)
                coords_delete(CoordsTry, CoordsOfBlock)
                blocks_in_mark_save(BlockWidth, BlocksInMark, CoordsOfBlock)


    print("Non-overlap Blocks in Mark: ")
    for CoordStart, BlockList in BlocksInMark.items():
        print(CoordStart, BlockList)

    return BlocksInMark


# these chars have colors in Linux terminal, I hope in windows there are colored chars, too
# https://apps.timwhitlock.info/emoji/tables/unicode

CharBg = "🔸" #small orange diamond
CharsetColorful = [
    "", # the [0] size isn't in blocks
    "🔅",  # low brightness symbol
    "🌑", # new moon symbol
    "💜", #purple heart
    "🔴", #large red circle
    "🔵", #large blue circle,
    "🔆", # high brightness symbol
    "🔘", #radio button,
]
def block_to_string(Mark, BlocksInMark, CharSet=CharsetColorful, CharBg=CharBg, Prefix=""):
    # print("Chars:")
    #for C in CharSet:
    #    print(C, C, C)

    Area = mark_util.mark_to_area(Mark)
    for BlockSize, CoordsInBlock in BlocksInMark.items():
        print("Coords in block: ", CoordsInBlock)
        for CoordBlock in CoordsInBlock:
            for X, Y in CoordBlock:
                Area[X][Y] = CharSet[BlockSize]
    return area.to_string(Area, Prefix=Prefix).replace(".", CharBg)

