import copy

# Directions: Left, Right, Up, Down, LeftUp, LeftDown, RightUp, RightDown
# TESTED
def fire(Area, BurningAreaCoords, Directions, CharsBlocking, CharFire="F"):

    Width, Height = width_height_get(Area)

    if CharFire not in CharsBlocking:
        CharsBlocking.append(CharFire)  # if fire is somewhere, it's blocking, too

    # 0 based X, Y coords!
    # these are Area coords, not pixel coords!
    for X, Y in BurningAreaCoords:
        if X < Width and X >= 0:
            if Y < Height and Y >= 0:
                if Area[X][Y] not in CharsBlocking:
                    Area[X][Y] = CharFire
                    if "Left"      in Directions: fire(Area, [(X-1,Y  )], Directions, CharsBlocking, CharFire)
                    if "Right"     in Directions: fire(Area, [(X+1,Y  )], Directions, CharsBlocking, CharFire)
                    if "Up"        in Directions: fire(Area, [(X  ,Y-1)], Directions, CharsBlocking, CharFire)
                    if "Down"      in Directions: fire(Area, [(X  ,Y+1)], Directions, CharsBlocking, CharFire)

                    if "LeftUp"    in Directions: fire(Area, [(X-1,Y-1)], Directions, CharsBlocking, CharFire)
                    if "LeftDown"  in Directions: fire(Area, [(X-1,Y+1)], Directions, CharsBlocking, CharFire)
                    if "RightUp"   in Directions: fire(Area, [(X+1,Y-1)], Directions, CharsBlocking, CharFire)
                    if "RightDown" in Directions: fire(Area, [(X+1,Y+1)], Directions, CharsBlocking, CharFire)

# TESTED
def make_empty(Width, Height, Bg):
    OneColumn = []
    for I in range(0, Height):
        OneColumn.append(Bg)
    Columns = []
    for I in range(0, Width):
        Columns.append(list(OneColumn)) # we have to duplicate OneColumn, not insert same one
    return Columns

# TESTED
def duplicate(AreaSource):
    return copy.deepcopy(AreaSource)

# TESTED
def width_height_get(Area):
    Width = len(Area)
    Height = len(Area[0])
    return (Width, Height)

# I know that OneLine is an alias for a separator,
# but from caller's side it's easier to use OneLine only
# TESTED. Array like data structure, with foreground/background pixels
def to_string(Area, OneLine=False, Separator="\n"):
    if OneLine:
        Separator = ""

    Width, Height = width_height_get(Area)

    Rows = []
    for Y in range(0, Height):
        Row = []
        for X in range(0, Width):
            Row.append(Area[X][Y])
        Rows.append("".join(Row))
    return Separator.join(Rows)

# TESTED
def coords_insert(Area, Coords, Char, Xshift=0, Yshift=0):
    for X, Y in Coords:
        Xrelative = X + Xshift
        Yrelative = Y + Yshift
        Area[Xrelative][Yrelative] = Char
