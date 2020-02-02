# -*- coding: utf-8 -*-
import copy, sys

###   TODO:   line scanning, horizontal
###   TODO:  mask area with area

#####################################################################
# a MARK is the original pixel with color and coordinate infos.
# an AREA is a sandbox where I can modify/draw anything, it's a duplication
#
# AREAS are important because sometime I want to draw on the top of
# the marks and I can't avoid the duplication making
#####################################################################



#############################################
# a nicer wrapper func
def mask_with_convex_shape(AreaA, AreaB, ForegroundChar, BackgroundChar):
    FuncProcessor = processor_mask_with_area
    AreaResult, _Accumulator = process_pixels(AreaA, AreaB, FuncProcessor, ForegroundChar, BackgroundChar)
    return AreaResult

# TODO: TEST IT # make decision at one pixel
def processor_mask_with_area(X, Y, AreaSrc, AreaMask, AreaResult, Fg, Bg, Accumulator=None):
    Pixel = Bg
    if AreaMask[X][Y] == Fg:
        Pixel = AreaSrc[X][Y]
    AreaResult[X][Y] = Pixel

# TESTED. General processor function
def process_pixels(AreaA, AreaB, FuncProcessor, ForegroundChar, BackgroundChar):
    WidthA, HeightA = width_height_get(AreaA)
    WidthB, HeightB = width_height_get(AreaB)
    if WidthA != WidthB or HeightA != HeightB:
        # TODO: correct error message
        print("process pixels, AreaA dimensions <> AreaB dimensions")
        sys.exit(1)

    Accumulator = dict() # a global area where the processor fun can leave information
                         # between different pixel position processing and maybe as a return value
                         # if a simple Area is not enough

    AreaResult = make_empty(WidthB, HeightB, BackgroundChar)
    for Y in range(0, HeightB):
        for X in range(0, WidthB):
            FuncProcessor(X, Y, AreaA, AreaB, AreaResult, ForegroundChar, BackgroundChar, Accumulator=Accumulator)
    return (AreaResult, Accumulator)
#############################################

# how many separated block is in the Area?
# the func return with size of separated blocks, too, with one of its coordinates
# TESTED
def count_separated_blocks(AreaOrig, WantedChar, FireBlockingChars):
    Area = duplicate(AreaOrig) # don't modify the original Area

    NumOfAreas = 0
    BlockSizes = {"total_size_of_closed_areas": 0}

    while True:
        Counter = pattern_count(Area, WantedPatterns=[WantedChar])
        NumOfChars = Counter[WantedChar]

        if NumOfChars == 0:
            return (NumOfAreas, BlockSizes)

        NumOfAreas += 1
        OneCharacterPosition = Counter["Coords"][WantedChar][0]

        FireInfo = fire(Area, [OneCharacterPosition], FireBlockingChars)
        BlockSizes[OneCharacterPosition] = FireInfo
        BlockSizes["total_size_of_closed_areas"] += FireInfo["BurntAreaSize"]

# TESTED
# From Area you want to get back the position of one Specific char, return with the first
def pattern_position_find_first(Area, Pattern):
    Width, Height = width_height_get(Area)
    for X in range(0, Width):
        for Y in range(0, Height):
            if Area[X][Y] == Pattern:
                return (X, Y)
    return None

# WantedPatterns example = ["Pattern1", "P2"]
# TESTED
# it's slow if you count once the chars and later loop over the whole Area to find their positions
def pattern_count(Area, WantedPatterns=[], UnwantedPatterns=[]):
    # if you define wanted patterns, you search specific patterns.
    # if you use Unwanted patterns, then you find everything that is not unwanted
    if WantedPatterns and UnwantedPatterns:
        print("count pattern: only WantedPatterns OR UnwantedPatterns")
        sys.exit(1)

    Result = {"Coords": dict() } # I won't search Coords in an Area :-)

    for Pattern in WantedPatterns:
        Result[Pattern] = 0

    X = -1
    for OneColumn in Area:
        X += 1
        Y = -1

        for Pattern in OneColumn:
            Y += 1

            PatternFounded = False

            if UnwantedPatterns:
                if Pattern not in UnwantedPatterns:
                    PatternFounded = True
                    if Pattern not in Result:
                        Result[Pattern] = 1
                    else:
                        Result[Pattern] += 1
            else:
                if Pattern in WantedPatterns:
                    PatternFounded = True
                    Result[Pattern] += 1

            if PatternFounded:
                if Pattern not in Result["Coords"]:
                    Result["Coords"][Pattern] = []
                Result["Coords"][Pattern].append((X, Y))

    return Result

def fire_from_side(Area, StartSide, CharsBlocking, Directions=None, CharFire="F"):
    Width, Height = width_height_get(Area)

    if Directions == "All":
        Directions = ["Left", "Right", "Up", "Down", "LeftUp", "LeftDown", "RightUp", "RightDown"]

    if CharFire not in CharsBlocking:
        CharsBlocking.append(CharFire)  # if fire is somewhere, it's blocking, too

    if   StartSide == "Top":
        CoordsFireStart = [(X,0) for X in range(0, Width) if Area[X][0] not in CharsBlocking]
        if Directions is None:
            Directions = ["Down", "Left", "Right", "LeftDown", "RightDown"]

    elif StartSide == "Bottom": # -1 means: the last elem in the column, the bottom...
        CoordsFireStart = [(X,Height-1) for X in range(0, Width) if Area[X][Height-1] not in CharsBlocking]
        if Directions is None:
            Directions = ["Up", "Left", "Right", "LeftUp", "RightUp"]

    elif StartSide == "Left":
        CoordsFireStart = [(0,Y) for Y in range(0, Height) if Area[0][Y] not in CharsBlocking]
        if Directions is None:
            Directions = ["Right", "Up", "Down", "RightUp", "RightDown"]

    elif StartSide == "Right": # coord -1: the last element, so the most-right column :-)
        CoordsFireStart = [(Width-1,Y) for Y in range(0, Height) if Area[Width-1][Y] not in CharsBlocking]
        if Directions is None:
            Directions = ["Left", "Up", "Down", "LeftUp", "LeftDown"]

    return fire(Area, CoordsFireStart,  CharsBlocking, Directions)

# Directions: Left, Right, Up, Down, LeftUp, LeftDown, RightUp, RightDown
# TESTED
def fire(Area, CoordsFireStart, CharsBlocking, Directions=None, CharFire="F"):
    if Directions == "All" or Directions == None:
        Directions = ["Left", "Right", "Up", "Down", "LeftUp", "LeftDown", "RightUp", "RightDown"]

    Width, Height = width_height_get(Area)

    if CharFire not in CharsBlocking:
        CharsBlocking.append(CharFire)  # if fire is somewhere, it's blocking, too

    Result = {"BurntAreaSize": 0,
              "AreaXmin": None,
              "AreaXmax": None,
              "AreaYmin": None,
              "AreaYmax": None
    }

    def local_fire(CoordsFireStart):
        Local = fire(Area, CoordsFireStart, CharsBlocking, Directions, CharFire)
        Result["BurntAreaSize"] += Local["BurntAreaSize"]
        if Local["AreaXmin"] is not None and Local["AreaXmin"] < Result["AreaXmin"]: Result["AreaXmin"] = Local["AreaXmin"]
        if Local["AreaXmax"] is not None and Local["AreaXmax"] > Result["AreaXmax"]: Result["AreaXmax"] = Local["AreaXmax"]
        if Local["AreaYmin"] is not None and Local["AreaYmin"] < Result["AreaYmin"]: Result["AreaYmin"] = Local["AreaYmin"]
        if Local["AreaYmax"] is not None and Local["AreaYmax"] > Result["AreaYmax"]: Result["AreaYmax"] = Local["AreaYmax"]

    # TODO: handle MIN/MAX VALUES

    # 0 based X, Y coords!
    # these are Area coords, not pixel coords!
    for X, Y in CoordsFireStart:
        if X < Width and X >= 0:
            if Y < Height and Y >= 0:
                if Area[X][Y] not in CharsBlocking:
                    Area[X][Y] = CharFire

                    Result["BurntAreaSize"] += 1
                    Result["AreaXmin"] = X
                    Result["AreaXmax"] = X
                    Result["AreaYmin"] = Y
                    Result["AreaYmax"] = Y

                    if "Left"      in Directions: local_fire([(X-1,Y  )])
                    if "Right"     in Directions: local_fire([(X+1,Y  )])
                    if "Up"        in Directions: local_fire([(X  ,Y-1)])
                    if "Down"      in Directions: local_fire([(X  ,Y+1)])

                    if "LeftUp"    in Directions: local_fire([(X-1,Y-1)])
                    if "LeftDown"  in Directions: local_fire([(X-1,Y+1)])
                    if "RightUp"   in Directions: local_fire([(X+1,Y-1)])
                    if "RightDown" in Directions: local_fire([(X+1,Y+1)])

    # return (Result, AreaXmin, AreaXmax, AreaYmin, AreaYmax)
    return Result

# TESTED
def make_empty(Width, Height, Bg):
    OneColumn = []
    for I in range(0, Height):
        OneColumn.append(Bg)
    Columns = []
    for I in range(0, Width):
        Columns.append(list(OneColumn)) # we have to duplicate OneColumn, not insert same one
    return Columns

# TESTED
def duplicate(AreaSource):
    return copy.deepcopy(AreaSource)

# TESTED
def width_height_get(Area):
    Width = len(Area)
    Height = len(Area[0])
    return (Width, Height)

# I know that OneLine is an alias for a separator,
# but from caller's side it's easier to use OneLine only
# TESTED. Array like data structure, with foreground/background pixels
def to_string(Area, OneLine=False, Separator="\n", Prefix="", AfterString="", BeforeString=""):
    if OneLine:
        Separator = ""

    Width, Height = width_height_get(Area)

    Rows = []
    for Y in range(0, Height):
        Row = []
        for X in range(0, Width):
            Row.append(Area[X][Y])
        Rows.append(Prefix + "".join(Row))
    return BeforeString + Separator.join(Rows) + AfterString

# TESTED
def coords_insert_from_mark(Area, Mark, Char, Xshift=0, Yshift=0):
    for X, Y in Mark["Coords"]:
        Xrelative = X + Xshift
        Yrelative = Y + Yshift
        Area[Xrelative][Yrelative] = Char
