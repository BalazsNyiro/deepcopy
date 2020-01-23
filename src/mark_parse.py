import mark_util
# Mark analyser algorithms, main logic
# OutputType can be: human | data


def mark_info_basic(Prg, Marks, MarkId, MarkStats):
    Xmin, Xmax, Ymin, Ymax, Width, Height = mark_util.mark_min_max_width_height(Prg, Marks[MarkId])

    mark_info_insert(Prg, MarkStats, MarkId, [
        ("width",  Width),
        ("height", Height),
        ("area_bounding_box", Width*Height),
        ("pixelnum", len(Marks[MarkId])),
        ("=================", "other infos"),
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


