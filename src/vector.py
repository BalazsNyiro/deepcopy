# -*- coding: utf-8 -*-
# return: block exists, PixelWithProblem(Coords or None)
# TODO: WRITE SEPARATED TEST for positive and negative cases
def block_check_exist_in_mark(Mark, XTopLeft, YTopLeft, XBottomRight, YBottomRight):
    for XMaybe in range(XTopLeft, XBottomRight + 1):
        for YMaybe in range(YTopLeft, YBottomRight + 1):
            if (XMaybe, YMaybe) not in Mark["Coords"]:
                return False, (XMaybe, YMaybe)
    return (True, None)

# TESTED directly
def block_search_in_mark(Mark):
    BlockWidthMax = min(Mark["Width"], Mark["Height"])
    print("Block max width:", BlockWidthMax)

    BlocksInMark = {}

    for BlockWidth in range(BlockWidthMax, 0, -1):
        # print("Search, BlockWidth:", BlockWidth)

        for X, Y in Mark["Coords"]:

            XBottomRight = X+BlockWidth -1
            YBottomRight = Y+BlockWidth -1

            # if we try to leave the original dimensions:
            if XBottomRight > Mark["Width"] - 1: continue
            if YBottomRight > Mark["Height"] - 1: continue

            BlockCheckExist, FirstProblem = block_check_exist_in_mark(Mark, X, Y, XBottomRight, YBottomRight)
            ProblemReport = ""
            if FirstProblem is not None:
                ProblemReport = " first problem: " + str(FirstProblem)
            else:
                if BlockWidth not in BlocksInMark:
                    BlocksInMark[BlockWidth] = []
                BlocksInMark[BlockWidth].append((X,Y))

            # print("analyse: ", X, Y, " -> ", XBottomRight, YBottomRight, BlockCheckExist, ProblemReport)

    print("Blocks in Mark: ")
    for CoordStart, BlockList in BlocksInMark.items():
        print(CoordStart, BlockList)

    return BlocksInMark
