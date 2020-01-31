# -*- coding: utf-8 -*-
# return: block exists, PixelWithProblem(Coords or None)
# TESTED
def block_check_exist_in_mark(Mark, XTopLeft, YTopLeft, XBottomRight, YBottomRight):
    CoordsOfBlock = []
    for XMaybe in range(XTopLeft, XBottomRight + 1):
        for YMaybe in range(YTopLeft, YBottomRight + 1):
            if (XMaybe, YMaybe) not in Mark["Coords"]:
                return (False, (XMaybe, YMaybe), [])
                # Block doesnt exist, PixelWithProblem
            CoordsOfBlock.append((XMaybe, YMaybe))

    return (True, None, CoordsOfBlock) # Block exists, No Problem

# TESTED directly
def block_nonoverlap_search_in_mark(Mark):
    BlockWidthMax = min(Mark["Width"], Mark["Height"])
    print("Block max width:", BlockWidthMax)

    BlocksInMark = {}

    for BlockWidth in range(BlockWidthMax, 0, -1):
        # print("Search, BlockWidth:", BlockWidth)

        # duplication of keys, I will remove the
        # detected points so at the end Coords will be empty
        Coords = dict(Mark["Coords"])
        while Coords:
            X, Y = list(Coords.keys())[0]
            del Coords[(X, Y)]

            # if we try to leave the original dimensions:
            XBottomRight = X+BlockWidth -1;
            if XBottomRight > Mark["Width"] - 1:  continue
            YBottomRight = Y+BlockWidth -1;
            if YBottomRight > Mark["Height"] - 1: continue

            BlockCheckExist, FirstProblem, CoordsOfBlock = block_check_exist_in_mark(Mark, X, Y, XBottomRight, YBottomRight)
            # ProblemReport = ""
            if FirstProblem is not None:
                # ProblemReport = " first problem: " + str(FirstProblem)
                pass
            else:
                if BlockWidth not in BlocksInMark:
                    BlocksInMark[BlockWidth] = []
                BlocksInMark[BlockWidth].append((X,Y))

                # remove founded area from the set
                # to avoid overlapping areas
                for CoordInBlock in CoordsOfBlock:
                    if CoordInBlock in Coords: # we delete the top left pixel after the while immediately
                                               # so one pixel maybe not in the dict
                        del Coords[CoordInBlock]

            # print("analyse: ", X, Y, " -> ", XBottomRight, YBottomRight, BlockCheckExist, ProblemReport)

    print("Non-overlap Blocks in Mark: ")
    for CoordStart, BlockList in BlocksInMark.items():
        print(CoordStart, BlockList)

    return BlocksInMark
