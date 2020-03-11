
def find_all_possible_path(PathAll, PathNow, Neighbours, Spirals):
    print("PathNow:", PathNow)
    SpiralCoordActual = PathNow[-1]

    for Connection in Neighbours[SpiralCoordActual]:

        if Connection not in PathNow:
            PathNew = list(PathNow)
            PathNew.append(Connection)
            find_all_possible_path(PathAll, PathNew, Neighbours, Spirals)

        else: # Connection in PathNow:
            PathAll.append(PathNow)

