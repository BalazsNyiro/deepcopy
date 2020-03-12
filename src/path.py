def find_all_possible_path(PathNow, Neighbours, Spirals, PathTotalPointNumber=0,
                           PathAll = None,
                           SpiralsSkippedAvoidThem = None,
                           PathLongest = None
                          ):

    if PathAll is None: PathAll = []
    if SpiralsSkippedAvoidThem is None: SpiralsSkippedAvoidThem = []
    if PathLongest is None: PathLongest = {"PathTotalPointNumber": 0, "Path": []}

    SpiralCoordActual = PathNow[-1]
    if not PathTotalPointNumber:
        PathTotalPointNumber = len(Spirals[SpiralCoordActual])

    for Connection in Neighbours[SpiralCoordActual]:

        if Connection not in SpiralsSkippedAvoidThem:

            if Connection not in PathNow:
                PathNew = list(PathNow)
                PathNew.append(Connection)
                find_all_possible_path(PathNew, Neighbours, Spirals, PathTotalPointNumber + len(Spirals[Connection]), PathAll=PathAll, SpiralsSkippedAvoidThem=SpiralsSkippedAvoidThem, PathLongest=PathLongest)

            else: # Connection in PathNow:
                PathAll.append({"PathTotalPointNumber": PathTotalPointNumber, "Path": PathNow})

                if PathTotalPointNumber > PathLongest["PathTotalPointNumber"]:
                    PathLongest["PathTotalPointNumber"] = PathTotalPointNumber
                    PathLongest["Path"] = PathNow

    return PathAll, PathLongest