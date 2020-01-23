import mark_util
# Mark analyser algorithms, main logic
# OutputType can be: human | data

def mark_width_height(Prg, Marks, MarkId, MarkStats):
    Xmin, Xmax, Ymin, Ymax, Width, Height = mark_util.mark_min_max_width_height(Prg, Marks[MarkId])

    MarkStats[MarkId]["x_min"] = Xmin
    MarkStats[MarkId]["x_max"] = Xmax
    MarkStats[MarkId]["y_min"] = Ymin
    MarkStats[MarkId]["y_max"] = Ymax
    MarkStats[MarkId]["width"] = Width
    MarkStats[MarkId]["height"] = Height
    MarkStats[MarkId]["area_bounding_box"] = Width*Height

    return "parser mark_width_height: " + str(Width) + ", " + str(Height)
