# -*- coding: utf-8 -*-
import copy, sys

###   TODO:   line scanning, horizontal
###   TODO:  mask area with area


# TODO: SAVE INFO: the size of the first, second, third block
# how many separated block is in the Area?
# TESTED
def count_separated_blocks(AreaOrig, WantedChar, FireBlockingChars):
    Area = duplicate(AreaOrig) # don't modify the original Area

    NumOfAreas = 0

    while True:
        Counter = pattern_count(Area, WantedPatterns=[WantedChar])
        NumOfChars = Counter[WantedChar]

        if NumOfChars == 0:
            return NumOfAreas

        NumOfAreas += 1
        OneCharacterposition = Counter["Coords"][WantedChar][0]
        fire(Area, [OneCharacterposition], FireBlockingChars)


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
        BurningAreaCoords = [(X,0) for X in range(0, Width) if Area[X][0] not in CharsBlocking]
        if Directions is None:
            Directions = ["Down", "Left", "Right", "LeftDown", "RightDown"]

    elif StartSide == "Bottom": # -1 means: the last elem in the column, the bottom...
        BurningAreaCoords = [(X,Height-1) for X in range(0, Width) if Area[X][Height-1] not in CharsBlocking]
        if Directions is None:
            Directions = ["Up", "Left", "Right", "LeftUp", "RightUp"]

    elif StartSide == "Left":
        BurningAreaCoords = [(0,Y) for Y in range(0, Height) if Area[0][Y] not in CharsBlocking]
        if Directions is None:
            Directions = ["Right", "Up", "Down", "RightUp", "RightDown"]

    elif StartSide == "Right": # coord -1: the last element, so the most-right column :-)
        BurningAreaCoords = [(Width-1,Y) for Y in range(0, Height) if Area[Width-1][Y] not in CharsBlocking]
        if Directions is None:
            Directions = ["Left", "Up", "Down", "LeftUp", "LeftDown"]

    return fire(Area, BurningAreaCoords,  CharsBlocking, Directions)

# Directions: Left, Right, Up, Down, LeftUp, LeftDown, RightUp, RightDown
# TESTED
def fire(Area, BurningAreaCoords, CharsBlocking, Directions=None, CharFire="F"):
    if Directions == "All" or Directions == None:
        Directions = ["Left", "Right", "Up", "Down", "LeftUp", "LeftDown", "RightUp", "RightDown"]

    Width, Height = width_height_get(Area)

    if CharFire not in CharsBlocking:
        CharsBlocking.append(CharFire)  # if fire is somewhere, it's blocking, too

    BurntAreaSize = 0

    # 0 based X, Y coords!
    # these are Area coords, not pixel coords!
    for X, Y in BurningAreaCoords:
        if X < Width and X >= 0:
            if Y < Height and Y >= 0:
                if Area[X][Y] not in CharsBlocking:
                    Area[X][Y] = CharFire
                    BurntAreaSize += 1
                    if "Left"      in Directions: BurntAreaSize += fire(Area, [(X-1,Y  )], CharsBlocking, Directions, CharFire)
                    if "Right"     in Directions: BurntAreaSize += fire(Area, [(X+1,Y  )], CharsBlocking, Directions, CharFire)
                    if "Up"        in Directions: BurntAreaSize += fire(Area, [(X  ,Y-1)], CharsBlocking, Directions, CharFire)
                    if "Down"      in Directions: BurntAreaSize += fire(Area, [(X  ,Y+1)], CharsBlocking, Directions, CharFire)

                    if "LeftUp"    in Directions: BurntAreaSize += fire(Area, [(X-1,Y-1)], CharsBlocking, Directions, CharFire)
                    if "LeftDown"  in Directions: BurntAreaSize += fire(Area, [(X-1,Y+1)], CharsBlocking, Directions, CharFire)
                    if "RightUp"   in Directions: BurntAreaSize += fire(Area, [(X+1,Y-1)], CharsBlocking, Directions, CharFire)
                    if "RightDown" in Directions: BurntAreaSize += fire(Area, [(X+1,Y+1)], CharsBlocking, Directions, CharFire)

    return BurntAreaSize
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
def to_string(Area, OneLine=False, Separator="\n"):
    if OneLine:
        Separator = ""

    Width, Height = width_height_get(Area)

    Rows = []
    for Y in range(0, Height):
        Row = []
        for X in range(0, Width):
            Row.append(Area[X][Y])
        Rows.append("".join(Row))
    return Separator.join(Rows)

# TESTED
def coords_insert(Area, Coords, Char, Xshift=0, Yshift=0):
    for X, Y in Coords:
        Xrelative = X + Xshift
        Yrelative = Y + Yshift
        Area[Xrelative][Yrelative] = Char
