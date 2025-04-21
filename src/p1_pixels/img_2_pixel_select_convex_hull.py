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
    # The next point cannot be in right direction, the searching is always go in counterClockWise
    # to the bigger radian direction.
    # So radian 0 is always 2pi, there is no 0 value, to support counterClockWise complex hull searching
    # there is no 0 radian: every radian value is greater than 0, 0 is represented with 2pi,
    # to create a monotonous increasing radian range.

    if arctan <= 0:
        arctan = arctan + 2*math.pi

    return arctan, []


def _convex_hull_next_elem_detect(pointStart: tuple[int, int], coordinatesAll: list[tuple[int, int]], radianLastSelected: float=0.0) -> (
        tuple)[tuple[int, int], float, bool, list[str]]:
    """in a given point set, find the next elem of the hull,
    if start point is defined.

    radianLastSelected = 0.0 is the smallest possible radian val, every calculated value is greater than this
    """
    errors: list[str] = list()
    minimumOneElemDetected: bool = False
    radianMinInPoints: float = 0.0

    if len(coordinatesAll) == 1:  # if there is only one elem, it's easy to select the next hull elem...
        return pointStart, radianMinInPoints, minimumOneElemDetected, errors

    if len(coordinatesAll) == 0:
        return (0, 0), radianMinInPoints, minimumOneElemDetected, ["if there is no elem, there is no possible candidate as next hull elem"]


    radianMinNextHullPoint = (0, 0)

    for coordTarget in coordinatesAll:

        if coordTarget == pointStart:
            continue  # start and end point cannot be the same.

        # there is no 0 radian: every radian value is greater than 0, 0 is represented with 2pi,
        # to create a monotonous increasing radian range.
        radianNow, errorsRadian = radian_calculate_with_arctan(
            pointStart[0], pointStart[1], coordTarget[0], coordTarget[1])

        # print(f"coordtarget: {coordTarget} {radianNow}")

        errors.extend(errorsRadian)
        if errorsRadian: continue
        # don't continue the work if there was a problem with radian calc

        # if this is the first point, so there is no better option, use this:
        if radianNow >= radianLastSelected:  # so go under-clock-wise
            if not minimumOneElemDetected:
                minimumOneElemDetected = True
                radianMinInPoints = radianNow
                radianMinNextHullPoint = coordTarget
            else:
                if radianNow < radianMinInPoints:
                    radianMinInPoints = radianNow
                    radianMinNextHullPoint = coordTarget

    # print(f"selected radian coord: {radianMinNextHullPoint} {radianMinInPoints} errors: {errors}")
    return radianMinNextHullPoint, radianMinInPoints, minimumOneElemDetected, errors



def convex_hull_points_collect(pixelGroup_Glyph: img_0_pixels.PixelGroup_Glyph, wantedPixelGroupNames: set[str]) -> tuple[list[tuple[int, int]], list[str]]:
    """detect convex hull points in a matrix representation

    naive implementation, this is a very frequently used fun, so optimization is necessary later

    The matrix representation is prepared before this fun call...
    """

    # the order of the points are important, so I need to use a list
    # convexHullPoints currently has only ONE element, the first point
    convexHullPoints, errors = img_0_pixels.pixelgroup_matrix_repr_select_corner_coord(
        pixelGroup_Glyph, wantedRepresentedNames=wantedPixelGroupNames, wantedCorner=("bottom", "right"))
    print(f"Hull with one start point: {convexHullPoints}")

    if not convexHullPoints:  # theoretically for an empty set an empty answer is correct.
        msg = f"WARNING: no selected top right coord in given PixelGroup!! wantedNames: {wantedPixelGroupNames} pixelGroup: {pixelGroup_Glyph}"
        print(msg)
        return list(), errors  # no hull coord in empty selection
    ###################################################################################################

    if len(pixelGroup_Glyph.pixels) == 1:  # for 1 point the hull has 1 elem
        return convexHullPoints, errors

    coordinatesAll: list[tuple[int, int]] = img_0_pixels.pixelGroup_matrix_representation_collect_matrix_coords_with_represented_names(
        pixelGroup_Glyph.matrix_representation, wantedRepresentedNames=wantedPixelGroupNames,
        useAbsolutePixelCoordsInPage_insteadOf_relativeMatrixCoords=False)

    # TODO: OPTIMIZE. remove middle pixels, they cannot be the part of the hull,
    # if the current solution is too slow
    #   *    *
    #  *m*  *m*   *m*     a middle pixel cannot be the part of the complex hull,
    #   *                 if it has 4 or 3 neighbours. or maybe '2 oppose only?' Check that.




    hullPointsSet = set(convexHullPoints)
    pointStart = convexHullPoints[0]
    radianLastSelected = 0.0

    minimumOneElemDetected = True
    while minimumOneElemDetected:
        hullElemNext, radianLastSelected, minimumOneElemDetected, errorsFromHull = _convex_hull_next_elem_detect(pointStart, coordinatesAll, radianLastSelected=radianLastSelected)
        errors.extend(errorsFromHull)

        if minimumOneElemDetected:
            convexHullPoints.append(hullElemNext)
            hullPointsSet.add(hullElemNext)  # it is faster to search in a set instead of convexHullPoints

            pointStart = hullElemNext

    return convexHullPoints, errors
