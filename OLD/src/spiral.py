# -*- coding: utf-8 -*-
import area, time, util, os

# TESTED
def spirals_sort_by_len(SpiralsAll, SpiralsSelected, ReturnObj="DetailedInfo"): # DetailedInfo | SimpleSpirals

    SortedGroups = dict()
    for Selected in SpiralsSelected:
        SelectedLen = len(SpiralsAll[Selected])
        if SelectedLen not in SortedGroups:
            SortedGroups[SelectedLen] = []
        SortedGroups[SelectedLen].append(Selected)

    LengthSortedKeys = list(SortedGroups.keys())
    LengthSortedKeys.sort()

    util.dict_with_lists_display_simple_data(SortedGroups, Title="SortedGroups")

    SortedSpirals = []
    for Len in LengthSortedKeys:
        while SortedGroups[Len]:
            OneSpiralFromLengthGroup = SortedGroups[Len].pop()
            if ReturnObj == "DetailedInfo":
                SortedSpirals.append({"Len":Len, "Spiral": OneSpiralFromLengthGroup})
            else:
                SortedSpirals.append(OneSpiralFromLengthGroup)

    # print("SortedGroups", SortedGroups)
    return SortedSpirals

# TESTED
def neighbours_find_for_all_spirals(Spirals):
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

_Up    = (0, -1)
_Down  = (0, 1)
_Left  = (-1, 0)
_Right = (1, 0)

_SpiralOperators = {"CounterClockwise": {
                              "Down" : [_Down, _Right, _Up, _Left],
                              "Right": [_Right, _Up, _Left, _Down],
                              "Up"   : [_Up, _Left, _Down, _Right],
                              "Left" : [_Left, _Down, _Right, _Up] },
                         "Clockwise": {
                             "Down" : [_Down, _Left, _Up, _Right],
                             "Left" : [_Left, _Up, _Right, _Down],
                             "Up"   : [_Up, _Right, _Down, _Left],
                             "Right": [_Right, _Down, _Left, _Up] }}

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
    DirectionOperators = _SpiralOperators[Direction][Start]

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
# return with all spirals in mark
def spirals_nonoverlap_search_in_mark(Mark):
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
        util.dict_delete_keys(CoordsTry, SpiralBiggestCoords)

    return SpiralsInMark

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

# TESTED
def spirals_weight_summa(SpiralsSelected, SpiralsAllInfo):
    SummaPointNum = 0
    for Spiral in SpiralsSelected:
        SummaPointNum += len(SpiralsAllInfo[Spiral])
    return SummaPointNum