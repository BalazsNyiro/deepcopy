import mark_util

# return with info about Marks
def marks_info_table(Prg, Marks, WantedIdNums=None, OutputType="txt", MarkParserFuns=[]):
    Result = []

    Source = Marks.items()
    Errors = []
    MarkStats = dict()

    if WantedIdNums and isinstance(WantedIdNums, list):
        MarksWanted = dict()
        for Id in WantedIdNums:
            if Id in Marks:
                MarksWanted[Id] = Marks[Id]
            else:
                Errors.append("unknown wanted Mark id:" + str(Id))
        Source = MarksWanted.items()

    for MarkId, Mark in Source:
        mark_util.markstats_insert_id(MarkStats, MarkId)

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
                    Stats.append(str(K) + "")
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


# TODO: TEST IT
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
    return Xmin, Xmax, Ymin, Ymax, Width, Height

def mark_to_string(Prg, Mark):
    Xmin, Xmax, Ymin, Ymax, _Width, _Height = mark_min_max_width_height(Prg, Mark)

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


def markstats_insert_id(MarkStats, MarkId):
    if MarkId not in MarkStats:
        MarkStats[MarkId] = dict()