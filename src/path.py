
def find_all_possible_path(PathNow, Neighbours, Spirals, PathTotalPointNumber=0, PathAll=None, SpiralsSkippedAvoidThem=None):
    if PathAll is None: PathAll = []
    if SpiralsSkippedAvoidThem is None: SpiralsSkippedAvoidThem = []

    SpiralCoordActual = PathNow[-1]
    if not PathTotalPointNumber:
        PathTotalPointNumber = len(Spirals[SpiralCoordActual])

    print("PathNow:", PathTotalPointNumber, PathNow)

    for Connection in Neighbours[SpiralCoordActual]:

        if Connection not in SpiralsSkippedAvoidThem:

            if Connection not in PathNow:
                PathNew = list(PathNow)
                PathNew.append(Connection)
                find_all_possible_path(PathNew, Neighbours, Spirals, PathTotalPointNumber + len(Spirals[Connection]), PathAll=PathAll, SpiralsSkippedAvoidThem=SpiralsSkippedAvoidThem)

            else: # Connection in PathNow:
                PathAll.append({"PathTotalPointNumber": PathTotalPointNumber, "Path": PathNow})

    return PathAll