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

import math

import img_0_pixels

"""naive complex hull functions.

The Glyphs are typically small areas, so a naive algorithm can be enough first.
"""

# arctan: https://www.cuemath.com/trigonometry/arctan-0/
# https://stackoverflow.com/questions/9614109/how-to-calculate-an-angle-from-points
def radian_calculate_with_arctan(xStart: int, yStart: int, xEnd: int, yEnd: int, coordinatesAreScreenZeroZeroInTopLeftRightSystem=True) -> tuple[float, list[str]]:
    """from the coord of Start, what is the angle of End point?

    up: 0, right: 90, down: 180, left: 270 degrees.

    The two points cannot be the same, because in that case the angle cannot be calculated.

    returns with (radiant, list_of_errors)
    """

    dy = yEnd - yStart
    dx = xEnd - xStart

    # the matrix representation's (0,0) coord is in the top-left, so the smallest y is at the top!
    # in case of basic radian calculation, (0, 5) is ABOVE (0, 0).
    # but in screen representation (0, 0) is at the top, and (0, 5) is below that.
    if coordinatesAreScreenZeroZeroInTopLeftRightSystem:
        dy = -1*dy

    if dx == 0:

        if dy == 0:
            return 0.0, [
                f"angle of coords: same points cannot be used for calculation: {xStart},{yStart}  == {xEnd}, {yEnd}"]

        if dy > 0:
            return math.pi/2, []     # 90 degree
        else:
            return 3*math.pi/2, []

    arctan = math.atan2(dy, dx)

    # use only positive values, to see the relations between vectors
    if arctan < 0:
        arctan = arctan + 2*math.pi

    return arctan, []



def convex_hull_points_collect(pixelGroup_Glyph: img_0_pixels.PixelGroup_Glyph, wantedPixelGroupNames: set[str]) -> list[tuple[int, int], list[str]]:
    """detect convex hull points in a matrix representation

    naive implementation, this is a very frequently used fun, so optimization is necessary later

    The matrix representation is prepared before this fun call...
    """

    topLeftCoord, errors = img_0_pixels.pixelgroup_matrix_repr_select_top_left_coord(pixelGroup_Glyph)
    print(f"topLeft coord: {topLeftCoord}")

    convexHullPoints: list[tuple[int, int]] = list()

    radiansCalculated: dict[tuple[tuple[int, int], tuple[int, int]], float]

    coordinatesAll: list[tuple[int, int]] = img_0_pixels.pixelGroup_matrix_representation_collect_matrix_coords_with_represented_names(
        pixelGroup_Glyph.matrix_representation, wantedRepresentedNames=wantedPixelGroupNames,
        useAbsolutePixelCoordsInPage_insteadOf_relativeMatrixCoords=False)

    # find the smallest radian
    xSmallest = 0
    ySmallest = 0
    radianSmallest = 0
    firstCycle = True

    for (xTarget, yTarget) in coordinatesAll:

        if xTarget == topLeftCoord[0] and yTarget == topLeftCoord[1]:
            continue  # skip the start point, that cannot be checked

        if firstCycle:
            xSmallest = xTarget
            ySmallest = yTarget
            radianSmallest = radian_calculate_with_arctan(topLeftCoord[0], topLeftCoord[1], xSmallest, ySmallest)
            continue

        radianNow = radian_calculate_with_arctan(topLeftCoord[0], topLeftCoord[1], xTarget, yTarget)
        if radianNow < radianSmallest:
            xSmallest = xTarget
            ySmallest = yTarget
            radianSmallest = radianNow

    print(f"smallest radian coord: ({xSmallest}, {ySmallest})")

    return convexHullPoints, errors
