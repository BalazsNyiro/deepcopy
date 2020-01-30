# -*- coding: utf-8 -*-

def block_search_in_mark(Mark):
    BlockWidthMax = min(Mark["Width"], Mark["Height"])
    print("Block max width:", BlockWidthMax)

    BlocksInMark = {}

    for BlockWidth in range(BlockWidthMax, 0, -1):
        print("Search, BlockWidth:", BlockWidth)

        for X, Y in Mark["Coords"]:

            CornerX = X+BlockWidth -1
            CornerY = Y+BlockWidth -1

            # if we try to leave the original dimensions:
            if CornerX > Mark["Width"] - 1: continue
            if CornerY > Mark["Height"] - 1: continue

            print("analyse: ", X, Y, " -> ", CornerX, CornerY)


