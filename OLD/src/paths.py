import spiral

# TESTED
def find_spiral_with_longest_summarised_pathA_and_PathB(Spirals, SpiralsAndNeighbours=None, SpiralsUsed=None):
    if SpiralsUsed is None: SpiralsUsed = []
    if SpiralsAndNeighbours is None: SpiralsAndNeighbours = spiral.neighbours_find_for_all_spirals(Spirals)

    SpiralWithMaxLen_AB = None
    MaxLen = 0
    PathAfromSpiral = None
    PathBfromSpiral = None

    for Spiral in Spirals:
        AvoidThem = list()
        AvoidThem.extend(SpiralsUsed)

        if Spiral not in AvoidThem:

            PathAll, PathAnow = find_all_possible_path_from_one_Spiral([Spiral], SpiralsAndNeighbours, Spirals, SpiralsSkippedAvoidThem=AvoidThem)
            # print(Spiral, ">> Path Longest 1:", PathAnow)

            AvoidThem.extend(list(PathAnow["Path"])) # to find the second longest path, avoid the first path elems
            # print("Avoid them: ", AvoidThem)
            PathAll, PathBnow = find_all_possible_path_from_one_Spiral([Spiral], SpiralsAndNeighbours, Spirals, SpiralsSkippedAvoidThem=AvoidThem)
            if PathBnow["Path"]:
                PathFirstElem = PathBnow["Path"].pop(0)
                PathBnow["PathTotalPointNumber"] -= len(Spirals[PathFirstElem])

            # Path A: Spiral -> Elems of A
            # Path B: Spiral -> Elems of B,  Start spiral is removed.
            # Join the two list:
            # PathB reversed, Spiral -> Path A - this is a continuous path
            PathBnow["Path"].reverse() # and Spiral will be in the center as a CONNECTION POINT

            #print(Spiral, ">> Path Longest 2:", PathBnow)

            PathLenSumma = PathAnow["PathTotalPointNumber"] + PathBnow["PathTotalPointNumber"]
            #print(Spiral, ">> Path Longest B->Spiral->A:", PathLenSumma)

            if PathLenSumma > MaxLen:
                MaxLen = PathLenSumma
                SpiralWithMaxLen_AB = Spiral
                PathAfromSpiral = PathAnow
                PathBfromSpiral = PathBnow

    PathJoined = list()
    # we travel from PathB -> Spiral -> PathA direction
    if PathBfromSpiral["Path"]: PathJoined.extend(PathBfromSpiral["Path"])
    if PathAfromSpiral["Path"]: PathJoined.extend(PathAfromSpiral["Path"])
    PathTotal = {"PathTotalPointNumber": MaxLen, "Path": PathJoined}
    # print("Spiral with longest path A + path B =", MaxLen, SpiralWithMaxLen_AB)
    return SpiralWithMaxLen_AB, MaxLen, PathTotal

def find_all_possible_path_from_one_Spiral(PathNow, Neighbours, SpiralsAllInfo, PathTotalPointNumber=None,
                                           PathAll = None,
                                           SpiralsSkippedAvoidThem = None,
                                           PathLongest = None
                                          ):
    if PathAll is None: PathAll = []
    if SpiralsSkippedAvoidThem is None: SpiralsSkippedAvoidThem = []

    SpiralCoordActual = PathNow[-1]
    if PathTotalPointNumber is None:
        PathTotalPointNumber = spiral.spirals_weight_summa(PathNow, SpiralsAllInfo)

    if PathLongest is None:
        PathDefault = [SpiralCoordActual]
        PathLongest = {"PathTotalPointNumber": spiral.spirals_weight_summa(PathDefault, SpiralsAllInfo), "Path": PathDefault}

    for Connection in Neighbours[SpiralCoordActual]:

        if Connection not in SpiralsSkippedAvoidThem:

            if Connection not in PathNow:
                PathNew = list(PathNow)
                PathNew.append(Connection)
                find_all_possible_path_from_one_Spiral(PathNew, Neighbours, SpiralsAllInfo,
                                                       PathTotalPointNumber + len(SpiralsAllInfo[Connection]),
                                                       PathAll=PathAll,
                                                       SpiralsSkippedAvoidThem=SpiralsSkippedAvoidThem,
                                                       PathLongest=PathLongest)
            else: # Connection in PathNow:
                PathAll.append({"PathTotalPointNumber": PathTotalPointNumber, "Path": PathNow})

                if PathTotalPointNumber > PathLongest["PathTotalPointNumber"]:
                    PathLongest["PathTotalPointNumber"] = PathTotalPointNumber
                    PathLongest["Path"] = PathNow

    return PathAll, PathLongest
