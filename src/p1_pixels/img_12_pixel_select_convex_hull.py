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

import img_10_pixels

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

    # radian 0 is always 2pi, there is no 0 value, to support counterClockWise complex hull searching
    # there is no 0 radian: every radian value is greater than 0, 0 is represented with 2pi,
    # to create a monotonous increasing radian range.

    # explanation, why radian 0 is not used
    """
    The theoretical 0 value is in right direction:
           pi/2
            ^ 
            | 
      pi<---.-----> right direction, this is the theoretical 0 pi, and 2pi too.
            |
            |
            V
         pi+1/2 pi 
   
    But practially, the start point to detect convex hull is the BOTTOM-RIGHT position,
    because the next elem's radiant will be a non-zero positive value in this case.
        ..432 
        ..51
    
    so point 1 is the start, and we go around to 2, 3, 4, 5 and return to 1.
    in the last step 5->1 the theoretical radia value would be 0, which is less
    than 4->5 radian 3/2pi, 
    so I use 2pi instead of 0 pi for 5->1 direction.
    
    in other words: radian 0 is NEVER used, it is represented with 2pi,
    because that is the bigger value in clockwise direction,
    and the convexHull's end point can be closed with the biggest radian val.
    
    
    """

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


def convex_hull_points_collect_from_matrix_representation(
        matrix_representation: img_10_pixels.typeAlias_matrix_representation,
        wantedPixelGroupNames: set[str]) -> tuple[list[tuple[int, int]], list[str]]:

    coordinatesAll: list[tuple[int, int]] = img_10_pixels.pixelGroup_matrix_representation_collect_matrix_coords_with_represented_names(
        matrix_representation, wantedRepresentedNames=wantedPixelGroupNames,
        useAbsolutePixelCoordsInPage_insteadOf_relativeMatrixCoords=False)

    return convex_hull_points_collect_from_coordinates(coordinatesAll)


def coord_find_bottom_right__minimumOneElemInTheList(coords_withMinimumOneElement: list[tuple[int, int]]) -> tuple[int, int]:
    """find bottom-right coord"""
    coordBottomRight: tuple[int, int] = coords_withMinimumOneElement[0]
    for coord in coords_withMinimumOneElement:
        # coord is below the old bottomRight (0, 0) is in top-left, so greater Y is below smaller Y:
        if coord[1] > coordBottomRight[1]:
            coordBottomRight = coord
            continue
        if coord[1] == coordBottomRight[1]:
            if coord[0] > coordBottomRight[0]:
                coordBottomRight = coord

    return coordBottomRight


def convex_hull_points_collect_from_coordinates(
        coordinatesAll: list[tuple[int, int]]) -> tuple[list[tuple[int, int]], list[str]]:
    """detect convex hull points in a matrix representation

    naive implementation, this is a very frequently used fun, so optimization is necessary later

    The matrix representation is prepared before this fun call...
    """

    errors: list[str] = []

    if not coordinatesAll:  # without coords, there is no hull.
        return list(), errors

    ########## search bottom-right ##############
    # from this point there is minimum one point in coordinatesAll
    coordBottomRight = coord_find_bottom_right__minimumOneElemInTheList(coordinatesAll)
    #############################################

    # the order of the points are important, so I need to use a list
    # convexHullPoints currently has only ONE element, the first point
    convexHullPoints = [coordBottomRight]
    print(f"Hull with bottom-right start point: {convexHullPoints}")

    # TODO: OPTIMIZE. remove middle pixels, they cannot be the part of the hull,
    # if the current solution is too slow
    #   *    *
    #  *m*  *m*   *m*     a middle pixel cannot be the part of the complex hull,
    #   *                 if it has 4 or 3 neighbours. or maybe '2 oppose only?' Check that.


    hullPointsSet = set(convexHullPoints)
    pointStart = coordBottomRight
    radianLastSelected = 0.0

    minimumOneElemDetected = True
    while minimumOneElemDetected:
        hullElemNext, radianLastSelected, minimumOneElemDetected, errorsFromHull = (
            _convex_hull_next_elem_detect(pointStart, coordinatesAll, radianLastSelected=radianLastSelected))
        errors.extend(errorsFromHull)

        if minimumOneElemDetected:
            convexHullPoints.append(hullElemNext)
            hullPointsSet.add(hullElemNext)  # it is faster to search in a set instead of convexHullPoints

            pointStart = hullElemNext

    return convexHullPoints, errors
