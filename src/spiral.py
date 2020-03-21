# -*- coding: utf-8 -*-
import area, time, util, os


# THIS FUNC DOESNT't work properly, I have to create in path module
# def find_longest_path_with_unused_spirals(Spirals, UnusedSpirals):

# TESTED
# algorithm: keep the two strongest neighbour group as connection
def find_path_in_char_with_spirals(Spirals, ReturnObj="DetailedInfo"): # DetailedInfo | SimpleSpirals
    Path = []
    SpiralsAndNeighbours = find_neighbours_for_all_spiral(Spirals)

    SpiralsUnused = list(Spirals)

    while SpiralsUnused:
        PathAll, PathNewLongest = path.find_all_possible_path_from_one_Spiral([Coord], NeighboursDetected, Spirals, SpiralsSkippedAvoidThem=[(6, 1)])
        # PathNew = find the longest path with unused Spirals
        # if not Path:
        #   Path.append(PathNew)
        # else:
        #   connect_with_previous_path: PathNew

        # SpiralsUnused = SpiralsUnused - Spirals_in_PathNew

        if Spiral not in Path: Path[Spiral] = []
        if NeighboursUnused:
            if len(NeighboursUnused) == 1:
                Path[Spiral].append(NeighboursUnused[0])

    return Path

def _sort_neighbours_by_len(Spirals, Neighbours, ReturnObj="DetailedInfo"): # DetailedInfo | SimpleSpirals
    Sorted = dict()
    for Neighbour in Neighbours:
        NeighbourLen = len(Spirals[Neighbour])
        if NeighbourLen not in Sorted:
            Sorted[NeighbourLen] = []
        Sorted[NeighbourLen].append(Neighbour)

    LengthSortedKeys = list(Sorted.keys())
    LengthSortedKeys.sort()

    NeighboursSortedByLen = []
    for Len in LengthSortedKeys:
        while Sorted[Len]:
            OneSpiralFromLengthGroup = Sorted[Len].pop()
            if ReturnObj == "DetailedInfo":
                NeighboursSortedByLen.append({"Len":Len, "Spiral": OneSpiralFromLengthGroup})
            else:
                NeighboursSortedByLen.append(OneSpiralFromLengthGroup)

    # print("NeighboursSortedByLen", NeighboursSortedByLen)
    return NeighboursSortedByLen


# TESTED
def find_neighbours_for_all_spiral(Spirals):
    SpiralConnections= dict()
    Point_ParentSpiral = dict()

    # init: create Point->Spiral pairs and SpiralConnections base data struct
    for SpiralStartPoint in Spirals:
        for Point in Spirals[SpiralStartPoint]:
            Point_ParentSpiral[Point] = SpiralStartPoint

    Deltas = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (1, -1), (1, 0), (1, 1), (0, -1)]
    for SpiralStartPoint, SpiralPointsFromCenterToTail in Spirals.items():
        SpiralPointsFromTailToCenter = SpiralPointsFromCenterToTail[::-1]
        Neighbours = list()
        for PointX, PointY in SpiralPointsFromTailToCenter:

            # you don't have to check all point from tail
            # to center: you can stop if you have only original parent points
            # around the tested
            PointsFromSameSpiral = 0

            for DeltaX, DeltaY in Deltas:
                TestedX = PointX + DeltaX
                TestedY = PointY + DeltaY
                TestedPoint = (TestedX, TestedY)
                if TestedPoint in Point_ParentSpiral:
                    SpiralOfTestedPoint = Point_ParentSpiral[TestedPoint]

                    # if: we found a real neighbour
                    if SpiralOfTestedPoint != SpiralStartPoint:
                        if SpiralOfTestedPoint not in Neighbours:
                            Neighbours.append(SpiralOfTestedPoint)
                    else: # we found a point from same spiral
                        PointsFromSameSpiral += 1

            if PointsFromSameSpiral == 8:
                break # you can finish, the next points to the center
                      # are INSIDE of the spiral, you won't find new neighbours
        SpiralConnections[SpiralStartPoint] = Neighbours
    # print("connections: ", SpiralConnections)
    return SpiralConnections

Up    = ( 0,-1)
Down  = ( 0, 1)
Left  = (-1, 0)
Right = ( 1, 0)

def _spiral_operators(): return  {"CounterClockwise": {
                                      "Down" : [Down, Right, Up, Left],
                                      "Right": [Right, Up, Left, Down],
                                      "Up"   : [Up, Left, Down, Right],
                                      "Left" : [Left, Down, Right, Up] },
                                 "Clockwise": {
                                     "Down" : [Down, Left, Up, Right],
                                     "Left" : [Left, Up, Right, Down],
                                     "Up"   : [Up, Right, Down, Left],
                                     "Right": [Right, Down, Left, Up] }}

def _operator_next(DirectionOperators, OperatorNextCounter):
    OperatorX, OperatorY = DirectionOperators[OperatorNextCounter % 4] # we always use 4 operators
    return OperatorX, OperatorY, OperatorNextCounter+1

_Ranges = dict() # cached ranges, I don't want to recreate them always

# Spiral search from point 1, Clockwise, Down start:
#                  5   56  567  567  567  567  567  567   567   567   567  g567
#    1  1   1  41  41  41  41   418  418  418  418  418   418   418  f418  f418
#       2  32  32  32  32  32   32   329  329  329  329   329  e329  e329  e329
#                                           a   ba  cba  dcba  dcba  dcba  dcba
# TESTED
def _spiral_coords_list_from_coord(MarkCoords, Coord, Direction="CounterClockwise", Start="Down"):
    OperatorNextCounter = 0
    DirectionOperators = _spiral_operators()[Direction][Start]

    SpiralCoords = [(Coord)]
    X, Y = Coord
    Repetition = 1

    while True:
        if Repetition not in _Ranges:
            _Ranges[Repetition] = range(0, Repetition) # cached ranges to avoid nonstop range creation

        # I have to repeat twice this step to create the spiral
        for _ in ["TurnFirstOperator", "TurnSecondOperator"]:
            OperatorDeltaX, OperatorDeltaY, OperatorNextCounter = _operator_next(DirectionOperators, OperatorNextCounter)
            for _ in _Ranges[Repetition]: # to follow and understand
                X += OperatorDeltaX
                Y += OperatorDeltaY
                CoordNew = (X, Y)
                if CoordNew in MarkCoords:
                    SpiralCoords.append(CoordNew)
                else:
                    return SpiralCoords

        Repetition += 1

# TESTED
def _spiral_max_coords_list_from_coord(MarkCoords, Coord):
    CoordsLongest = list()
    Variations = [  ("Clockwise", "Up"),
                    ("Clockwise", "Down"),
                    ("Clockwise", "Left"),
                    ("Clockwise", "Right"),

                    ("CounterClockwise", "Up"),
                    ("CounterClockwise", "Down"),
                    ("CounterClockwise", "Left"),
                    ("CounterClockwise", "Right") ]

    for Clock, Direction in Variations:
        Spiral = _spiral_coords_list_from_coord(MarkCoords, Coord, Clock, Direction)
        if len(Spiral) > len(CoordsLongest):
            CoordsLongest = Spiral

    return CoordsLongest

# TESTED
def spiral_nonoverlap_search_in_mark(Mark):
    SpiralsInMark = dict()
    CoordsTry = dict(Mark["Coords"])

    while CoordsTry:

        SpiralBiggestCoordStart = (-1, -1)
        SpiralBiggestCoords = list() # the order of coords are important to represent the spiral

        for Coord in CoordsTry:
            SpiralMaxNow = _spiral_max_coords_list_from_coord(CoordsTry, Coord)
            if len(SpiralMaxNow) > len(SpiralBiggestCoords):
                SpiralBiggestCoords = SpiralMaxNow
                SpiralBiggestCoordStart = Coord

        SpiralsInMark[SpiralBiggestCoordStart] = SpiralBiggestCoords
        _coords_delete(CoordsTry, SpiralBiggestCoords)

    return SpiralsInMark

def _coords_delete(CoordsDict, CoordsDeletedList):
    for CoordDel in CoordsDeletedList:
        # print("  del:", CoordDel)
        del CoordsDict[CoordDel]

# these chars have colors in Linux terminal, I hope in windows there are colored chars, too
# https://apps.timwhitlock.info/emoji/tables/unicode

def spirals_display(Prg, Spirals, Width, Height, SleepTime=0, Prefix="", PauseAtEnd=0, PauseAtStart=0, SaveAsFilename=None):
    SaveAsTxt = list()

    CharBg = "🔸" #small orange diamond
    CharsetColorful = [
        "😎", # smiling face with sunglasses
        "🔘", #radio button,
        "🌼",
        "🍀",
        "🐙",
        "🎃", # jack-o-lantern
        "🐸",  # frog face
        "🎅", # father christmas
        "🐨",  # koala
        "🎁",  # Wrapped present,
        "🌷",  # tulip
        "🏀",  # basketball and hoop
        "😈", # smiling face with horns
        "🕐",  # clock face, one o'clock
        "🔴", #large red circle
        "🔵", #large blue circle,
        "🔆", # high brightness symbol
        "💜", #purple heart
        "🔅",  # low brightness symbol
        "🌑", # new moon symbol
        "💡",  # electric light bulb

    ]

    Area = area.make_empty(Width, Height, CharBg)
    print(area.to_string(Area, Prefix=Prefix, AfterString="\n\n", BeforeString="\n" * 33))
    time.sleep(PauseAtStart)

    for Coords in Spirals.values():
        CharColorful = CharsetColorful.pop(0)
        CharsetColorful.append(CharColorful)  # shifting elements in Colorful chars

        for X, Y in Coords:
            Area[X][Y] = CharColorful
            AreaTxt = area.to_string(Area, Prefix=Prefix, AfterString="\n\n", BeforeString="\n"*33)
            SaveAsTxt.append(AreaTxt)
            print(AreaTxt)
            if SleepTime:
                time.sleep(SleepTime)

    if PauseAtEnd:
        time.sleep(PauseAtEnd)

    if SaveAsFilename:
        util.file_write(Prg, os.path.join(Prg["DirTmpPath"], SaveAsFilename), "".join(SaveAsTxt))



