import spiral

# TODO: TEST it very carefully
def find_longest_path_with_unused_spirals(Spirals, UnusedSpirals=None):
    if UnusedSpirals is None: UnusedSpirals = []
    print("")
    SpiralsAndNeighbours = spiral.find_neighbours(Spirals)
    for Spiral in SpiralsAndNeighbours:
        PathAll, PathLongest = find_all_possible_path_from_one_Spiral([Spiral], SpiralsAndNeighbours, Spirals)
        print(Spiral, ">> Path Longest:", PathLongest)


def find_all_possible_path_from_one_Spiral(PathNow, Neighbours, Spirals, PathTotalPointNumber=0,
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
                find_all_possible_path_from_one_Spiral(PathNew, Neighbours, Spirals, PathTotalPointNumber + len(Spirals[Connection]), PathAll=PathAll, SpiralsSkippedAvoidThem=SpiralsSkippedAvoidThem, PathLongest=PathLongest)

            else: # Connection in PathNow:
                PathAll.append({"PathTotalPointNumber": PathTotalPointNumber, "Path": PathNow})

                if PathTotalPointNumber > PathLongest["PathTotalPointNumber"]:
                    PathLongest["PathTotalPointNumber"] = PathTotalPointNumber
                    PathLongest["Path"] = PathNow

    return PathAll, PathLongest