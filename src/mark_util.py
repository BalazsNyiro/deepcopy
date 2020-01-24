import util

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

    NotImportantInfoKeys = {"x_min":1, "y_min":1, "x_max":1, "y_max":1}

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

# TESTED, coordinate based data structure with foreground pixels only
def mark_to_string(Prg, Mark):
    Xmin, Xmax, Ymin, Ymax, Width, Height = mark_min_max_width_height(Prg, Mark)

    Area = mark_area_empty_making(Width, Height)

    for Coord in Mark:
        X, Y = Coord
        Xrelative = X - Xmin
        Yrelative = Y - Ymin
        Area[Xrelative][Yrelative] = MarkFg

    return mark_area_to_string(Area)


# TESTED. Array like data structure, with foreground/background pixels
def mark_area_to_string(Area):
    Width = len(Area)
    Height = len(Area[0])

    Rows = []
    for Y in range(0, Height):
        Row = []
        for X in range(0, Width):
            Row.append(Area[X][Y])
        Rows.append("".join(Row))
    return "\n".join(Rows)

# TESTED
def mark_area_empty_making(Width, Height):
    OneColumn = []
    for I in range(0, Height):
        OneColumn.append(MarkBg)
    Columns = []
    for I in range(0, Width):
        Columns.append(list(OneColumn)) # we have to duplicate OneColumn, not insert same one
    return Columns

# TESTED
def markstats_insert_id(MarkStats, MarkId):
    if MarkId not in MarkStats:
        MarkStats[MarkId] = dict()

# TESTED
def mark_area_convex(Prg, Mark):
    Xmin, _Xmax, Ymin, _Ymax, Width, Height = mark_min_max_width_height(Prg, Mark)
    AreaConvex = mark_area_empty_making(Width, Height)

    # naive implementation,
    # maybe there is better solution
    # connect all points with each other
    PixelCoords = [P for P in Mark.keys()]
    while PixelCoords:
        FromX, FromY = PixelCoords.pop(0)
        for ToX, ToY in PixelCoords:
            for ConnectionPointX, ConnectionPointY in util.connect_coords(FromX, FromY, ToX, ToY):
                # -Xmin, -Ymin: A mark contains pixels with relative coords: the minimum is in the left/top corner
                AreaConvex[ConnectionPointX - Xmin][ConnectionPointY - Ymin] = MarkFg
    return AreaConvex
