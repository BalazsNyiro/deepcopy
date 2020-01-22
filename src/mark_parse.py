import mark_util
# Mark analyser algorithms, main logic
# OutputType can be: human | data

def mark_width_height(Prg, Marks, MarkId, OutputType="data"):
    _, _, _, _, Width, Height = mark_util.mark_min_max_width_height(Prg, Marks[MarkId])
    Result = (Width, Height)
    if OutputType == "human":
        Result = "parser mark_width_height: " + str(Result)
    return Result
