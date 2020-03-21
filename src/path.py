import spiral

# TODO: TEST it very carefully
def find_spiral_with_longest_summarised_pathA_and_PathB(Spirals, SpiralsAndNeighbours=None, SpiralsUsed=None):
    if SpiralsUsed is None: SpiralsUsed = []
    if SpiralsAndNeighbours is None: SpiralsAndNeighbours = spiral.find_neighbours_for_all_spiral(Spirals)


    SpiralWithMaxLen_AB = None
    MaxLen = 0
    PathAfromSpiral = None
    PathBfromSpiral = None

    for Spiral in Spirals:
        AvoidThem = list()
        AvoidThem.extend(SpiralsUsed)

        PathAll, PathAnow = find_all_possible_path_from_one_Spiral([Spiral], SpiralsAndNeighbours, Spirals, SpiralsSkippedAvoidThem=AvoidThem)
        print(Spiral, ">> Path Longest 1:", PathAnow)

        AvoidThem.extend(list(PathAnow["Path"])) # to find the second longest path, avoid the first path elems
        # print("Avoid them: ", AvoidThem)
        PathAll, PathBnow = find_all_possible_path_from_one_Spiral([Spiral], SpiralsAndNeighbours, Spirals, SpiralsSkippedAvoidThem=AvoidThem)
        print(Spiral, ">> Path Longest 2:", PathBnow)

        PathLenSumma = PathAnow["PathTotalPointNumber"] + PathBnow["PathTotalPointNumber"]
        print(Spiral, ">> Path Longest A+B:", PathLenSumma)

        if PathLenSumma > MaxLen:
            MaxLen = PathLenSumma
            SpiralWithMaxLen_AB = Spiral
            PathAfromSpiral = PathAnow
            PathBfromSpiral = PathBnow

    # print("Spiral with longest path A + path B =", MaxLen, SpiralWithMaxLen_AB)
    return SpiralWithMaxLen_AB, MaxLen, PathAfromSpiral, PathBfromSpiral

# TODO: test it
def path_total_spiral_weight(Path, Spirals):
    PathTotalPointNumber = 0
    for Spiral in Path:
        PathTotalPointNumber += len(Spirals[Spiral])
    return PathTotalPointNumber

def find_all_possible_path_from_one_Spiral(PathNow, Neighbours, Spirals, PathTotalPointNumber=None,
                                           PathAll = None,
                                           SpiralsSkippedAvoidThem = None,
                                           PathLongest = None
                                           ):
    if PathAll is None: PathAll = []
    if SpiralsSkippedAvoidThem is None: SpiralsSkippedAvoidThem = []

    SpiralCoordActual = PathNow[-1]
    if PathTotalPointNumber is None:
        PathTotalPointNumber = path_total_spiral_weight(PathNow, Spirals)

    if PathLongest is None:
        PathDefault = [SpiralCoordActual]
        PathLongest = {"PathTotalPointNumber": path_total_spiral_weight(PathDefault, Spirals), "Path": PathDefault} # the len of first elem is not used because we are there.

    for Connection in Neighbours[SpiralCoordActual]:

        if Connection not in SpiralsSkippedAvoidThem:

            if Connection not in PathNow:
                PathNew = list(PathNow)
                PathNew.append(Connection)
                find_all_possible_path_from_one_Spiral(PathNew, Neighbours, Spirals,
                                                       PathTotalPointNumber + len(Spirals[Connection]),
                                                       PathAll=PathAll,
                                                       SpiralsSkippedAvoidThem=SpiralsSkippedAvoidThem,
                                                       PathLongest=PathLongest)
            else: # Connection in PathNow:
                PathAll.append({"PathTotalPointNumber": PathTotalPointNumber, "Path": PathNow})

                if PathTotalPointNumber > PathLongest["PathTotalPointNumber"]:
                    PathLongest["PathTotalPointNumber"] = PathTotalPointNumber
                    PathLongest["Path"] = PathNow

    return PathAll, PathLongest