#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2025 Balazs Nyiro
# All rights reserved.

# This source code (all file in this repo)
# is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Please read the complete LICENSE file
# in the root directory of this source tree.


def coords_neighbours(x: int, y: int,
                      xMinValidPossibleCoordValue: int, yMinValidPossibleCoordValue: int,
                      xMaxValidPossibleCoordValue: int, yMaxValidPossibleCoordValue: int,
                      allowedDirections: set[int]={1,2,3,4,5,6,7,8}
                      ) -> list[tuple[int, int], ]:
    """return with possible neighbour coordinates"""

    neighbours = list()

    directions = { 1: (x,   y-1),
                   2: (x+1, y-1),
                   3: (x+1, y  ),
                   4: (x+1, y+1),
                   5: (x,   y+1),
                   6: (x-1, y+1),
                   7: (x-1, y  ),
                   8: (x-1, y-1)
                   }

    for direction, (xNeighbour, yNeighbour) in directions.items():

        if direction not in allowedDirections:
            continue

        if xNeighbour < xMinValidPossibleCoordValue or yNeighbour < yMinValidPossibleCoordValue:
            continue # cannot go over the limits...

        if xNeighbour > xMaxValidPossibleCoordValue or yNeighbour > yMaxValidPossibleCoordValue:
            continue # cannot go over the limits...

        neighbours.append( (xNeighbour, yNeighbour) )

    return sorted(neighbours)
