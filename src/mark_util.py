# -*- coding: utf-8 -*-
import util, area

MarkBg = "." # the sigh of background area, no active pixel
MarkFg = "O" # if active pixel is in the mark

def markstats_init():
    return {"keywords_len_max": 0}




# return with info about Marks
def marks_info_table(Prg, Marks, WantedIdNums=None, OutputType="txt", MarkParserFuns=[]):
    Result = []

    Source = Marks.items()
    Errors = []
    MarkStats = markstats_init()

    NotImportantInfoKeys = {}

    if WantedIdNums and isinstance(WantedIdNums, list):
        MarksWanted = dict()
        for Id in WantedIdNums:
            if Id in Marks:
                MarksWanted[Id] = Marks[Id]
            else:
                Errors.append("unknown wanted Mark id:" + str(Id))
        Source = MarksWanted.items()

    for MarkId, Mark in Source:
        markstats_insert_id(MarkStats, MarkId)

        for MarkParserFun in MarkParserFuns:
            MarkParserFun(Prg, Marks, MarkId, MarkStats)

        if OutputType == "txt":
            Result.append("\n") # empty line
            Result.append("Mark id: " + str(MarkId))
            Result.append("") # empty line
            Result.append(mark_to_string(Prg, Mark))

            if MarkStats[MarkId]:
                Stats = []
                for K, V in MarkStats[MarkId].items():
                    if K in NotImportantInfoKeys:
                        continue

                    Vformatted = str(V)
                    Kformatted = "{txt: >{fill}}".format(txt=K, fill=MarkStats["keywords_len_max"]) # maybe f strings?
                    if isinstance(V, str) and "\n" in V:
                        Vformatted = util.multiline_txt_insert_prefix(Prg, V, Prefix=" "*(MarkStats["keywords_len_max"]+2))

                    Stats.append(str(Kformatted) + ": " + Vformatted)
                Result.append("")
                Result.append("\n".join(Stats))


        elif OutputType == "html":
            Result.append("TODO: html info display")

        elif OutputType == "latex":
            Result.append("TODO: latex info display")


    ResultToStr = [str(Val) for Val in Result]

    if OutputType == "txt":
        return "\n".join(ResultToStr) + "\n" + "\n".join(Errors)

    elif OutputType == "html":
        return "\n".join(ResultToStr) + "\n" + "\n".join(Errors)

    elif OutputType == "latex":
        return "\n".join(ResultToStr) + "\n" + "\n".join(Errors)


# TESTED
def mark_min_max_width_height(Prg, Mark):
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

    Width = Xmax - Xmin + 1
    Height = Ymax - Ymin + 1
    return (Xmin, Xmax, Ymin, Ymax, Width, Height)

# TESTED from mark_to_string
def mark_to_area(Prg, Mark):
    Xmin, Xmax, Ymin, Ymax, Width, Height = mark_min_max_width_height(Prg, Mark)
    Area = area.make_empty(Width, Height, MarkBg)
    area.coords_insert(Area, Mark, MarkFg, Xshift= -Xmin, Yshift= -Ymin)
    return Area

# TESTED
def mark_to_string(Prg, Mark):
    return area.to_string(mark_to_area(Prg, Mark))


# TESTED
def markstats_insert_id(MarkStats, MarkId):
    if MarkId not in MarkStats:
        MarkStats[MarkId] = dict()

# TESTED
def mark_area_convex(Prg, Mark, PointsWanted=False):
    Xmin, _Xmax, Ymin, _Ymax, Width, Height = mark_min_max_width_height(Prg, Mark)
    AreaConvex = area.make_empty(Width, Height, MarkBg)

    ConnectionPointLines = []
    # naive implementation, it based on Mark's special attributes: there aren't gaps in marks.
    # I want to revise it later.
    # TODO: maybe if we have more time: Gift Wrapping Algorithm (Convex Hull)
    # maybe there is better solution
    # connect all points with each other
    PixelCoords = [P for P in Mark.keys()]
    while PixelCoords:
        FromX, FromY = PixelCoords.pop(0)
        for ToX, ToY in PixelCoords:
            Points = util.connect_coords(FromX, FromY, ToX, ToY)
            if PointsWanted:
                ConnectionPointLines.append(Points)
            for ConnectionPointX, ConnectionPointY in Points:
                # -Xmin, -Ymin: A mark contains pixels with relative coords: the minimum is in the left/top corner
                AreaConvex[ConnectionPointX - Xmin][ConnectionPointY - Ymin] = MarkFg

    if PointsWanted:
        return AreaConvex, ConnectionPointLines
    return AreaConvex
