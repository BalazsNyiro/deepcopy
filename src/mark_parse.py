import mark_util, util

# Mark analyser algorithms, main logic
# OutputType can be: human | data

def mark_convex_area(Prg, Marks, MarkId, MarkStats):
    Mark = Marks[MarkId]
    Xmin, Xmax, Ymin, Ymax, Width, Height = mark_util.mark_min_max_width_height(Prg, Mark)
    AreaConvex = mark_util.mark_area_empty_making(Width, Height)

    # naive implementation,
    # maybe there is better solution
    # connect all points with each other
    PixelCoords = [P for P in Mark.keys()]
    while PixelCoords:
        FromX, FromY = PixelCoords.pop(0)
        for ToX, ToY in PixelCoords:
            for ConnectionPointX, ConnectionPointY in util.connect_coords(FromX, FromY, ToX, ToY):

                # -Xmin, -Ymin: A mark contains pixels with relative coords: the minimum is in the left/top corner
                AreaConvex[ConnectionPointX-Xmin][ConnectionPointY-Ymin] = mark_util.MarkFg

    StringPrefix = " " * MarkStats["keywords_len_max"]
    mark_info_insert(Prg, MarkStats, MarkId, [("mark_convex_area", "\n"+mark_util.mark_area_to_string(AreaConvex, StringPrefix))])


def mark_convex_hull(Prg, Marks, MarkId, MarkStats):
    # TODO: implement it, based on convex_area
    pass

def mark_info_basic(Prg, Marks, MarkId, MarkStats):
    Xmin, Xmax, Ymin, Ymax, Width, Height = mark_util.mark_min_max_width_height(Prg, Marks[MarkId])

    mark_info_insert(Prg, MarkStats, MarkId, [
        ("width",  Width),
        ("height", Height),
        ("area_bounding_box", Width*Height),
        ("pixelnum", len(Marks[MarkId])),
#        ("==notImportant==", ""),
        ("x_min", Xmin),
        ("x_max", Xmax),
        ("y_min", Ymin),
        ("y_max", Ymax),
    ])

    return "parser mark_width_height: " + str(Width) + ", " + str(Height)

def mark_info_insert(_Prg, MarkStats, MarkId, KeyVals):
    Mark = MarkStats[MarkId]
    for Key, Val in KeyVals:
        if Key in Mark:
            print("ERROR: owerwrite existing key: " + Key + "  oldval: " + Mark[Key] + "   new val:" + Val)
        Mark[Key] = Val

        if len(Key) > MarkStats["keywords_len_max"]:
            MarkStats["keywords_len_max"] = len(Key)


