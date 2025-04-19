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