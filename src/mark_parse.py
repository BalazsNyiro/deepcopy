import mark_util

# Mark analyser algorithms, main logic
# OutputType can be: human | data

# naive implementation,
# maybe there is better solution
def mark_convex_area(Prg, Marks, MarkId, MarkStats):
    Mark = Marks[MarkId]
    PixelCoords = [P for P in Mark.keys()]
    Xmin, Xmax, Ymin, Ymax, Width, Height = mark_util.mark_min_max_width_height(Prg, Mark)
    AreaConvex = mark_util.mark_area_empty_making(Width, Height)

    mark_info_insert(Prg, MarkStats, MarkId, [("mark_convex_area", 1)])

    while PixelCoords:
        X, Y = PixelCoords.pop(0)
    pass

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


