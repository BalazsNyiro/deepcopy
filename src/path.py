
def find_all_possible_path(SpiralCoord, Neighbours, Path, Spirals):
    print(" path_find_next_spirals")
    return []

    if not NeighboursUsed: NeighboursUsed = {}
    NeighboursUsed = dict(NeighboursUsed) # duplicate it

    for Connection in Neighbours[SpiralCoord]:
        if Connection not in NeighboursUsed:
            Next[Connection] = {}
            NeighboursUsed[Connection] = {}

    return Next, NeighboursUsed
