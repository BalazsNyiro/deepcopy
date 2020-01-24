# TESTED
def make_empty(Width, Height, Bg):
    OneColumn = []
    for I in range(0, Height):
        OneColumn.append(Bg)
    Columns = []
    for I in range(0, Width):
        Columns.append(list(OneColumn)) # we have to duplicate OneColumn, not insert same one
    return Columns


# TESTED. Array like data structure, with foreground/background pixels
def to_string(Area):
    Width = len(Area)
    Height = len(Area[0])

    Rows = []
    for Y in range(0, Height):
        Row = []
        for X in range(0, Width):
            Row.append(Area[X][Y])
        Rows.append("".join(Row))
    return "\n".join(Rows)

# TODO: TEST IT
def coords_insert(Area, Coords, Char, Xshift=0, Yshift=0):
    for Coord in Coords:
        X, Y = Coord
        Xrelative = X + Xshift
        Yrelative = Y + Yshift
        Area[Xrelative][Yrelative] = Char
