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


"""Preparation step: collect statistics about pixelgroups to support recognition decisions

Every pixelgroup has a unique ID, the statistics are stored based on that id.

"""

import typing
import img_0_pixels
import img_1_pixel_select


def statistics_collect_about_pixelgroups(pixelGroups_glyphs_all: list[img_0_pixels.PixelGroup_Glyph]) -> dict[int, dict[str, int]]:
    """analyse every glyphs one by one to support the recognise step later.

    This section is about data collection about the pixelgroups.
    """

    # every pixelGroup_glyph has a unique ID, that is the first INT.
    # the second layer is the stat info name about the pixelgroup.
    # the third layer is the stat about the group
    # stats = {
    #           pixelGroup_glyph_id:  {
    #                                   "stat_simple": 1,      # a simple key-val pair
    #                                   "stat_dict"  : {0: 3}  # number-number related data,
    #                                   "stat_name"  : {
    #                                                   pixelCoord1 -> data1
    #                                                   pixelCoord2 -> data2
    #                                                   }
    #                                 }
    #         }
    stats_of_pixelGroups_glyphs: dict[int, dict[str, int ]] = dict()
    # list[list[(int, int)]] |       # list of (list of pixels)
    # int |
    # dict[int, int]

    for pixelGroup_glyph in pixelGroups_glyphs_all:

        pixelGroup_glyph.matrix_representation_refresh((1, 1, 1, 1))

        stats_of_pixelGroups_glyphs[pixelGroup_glyph.groupId] = {
            "glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph":
                glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph(pixelGroup_glyph.matrix_representation, checkEmptyBorderAroundMatrixRepresentation=False)}




    return stats_of_pixelGroups_glyphs


def glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph(
        pixelGroup_glyph_matrix_representation: list[list[img_0_pixels.PixelGroup_Glyph]],
        checkEmptyBorderAroundMatrixRepresentation: bool = True
) -> int: #  list[ list[(int, int) ] ]:
    """count the closed inactive segments inside of a glyph.

    The matrix representation HAS to have an empty border around the glyph: matrix_representation_refresh(1,1,1,1) in the caller function.



    This can be tricky; a simple example:
     - 'A' glyph has one closed section which is totally bordered with active pixels.
     - '8' glyph has two (non-overlapped) sections, totally separated from the outside inactive area
     
     Special cases :-) 
     - 'R' has one segment
     - '®' copyright symbol has 2, but they are embedded/overlapped, because the R is inside in a circle
           currently the overlapping is not analysed, the isolated segments are detected as pixel-sets only
           theoretically the copyright symbol has 2 pixelgroups, because the R and O are separated.
           TODO: decide: does the program need to be prepared for overlapping symbols or not?
    """

    print(f"matrix representation for stat creation:")
    img_0_pixels.pixelGroup_matrix_representation_str(pixelGroup_glyph_matrix_representation, printStr=True)
    print(f" create a general 'drop' function with gravity_directions_at_start and gravity_directions_after_first_collision params ")





    ######################## This validation can be turned off IF the caller has a declared border creation in matrix representation ##########
    # def matrix_representation_has_emptyborder_around_glyph()
    if checkEmptyBorderAroundMatrixRepresentation:
        img_0_pixels.pixelGroup_matrix_representation_has_emptyborder_around_glyph(
            pixelGroup_glyph_matrix_representation, raiseExceptionIfNoBorder=True)
    ######################## This validation can be turned off IF the caller has a declared border creation in matrix representation ##########






    # at this point we know that the matrix has an empty border, so the outside pixels can be collected

    pixelCoordsOutside_glyph = set()


    # TODO: DROP function
    pixelCoordsToAnalyse = [(0,0)]
    pixelCoordsAnalysed = set()

    x_max_in_representation = len(pixelGroup_glyph_matrix_representation[0])-1
    y_max_in_representation = len(pixelGroup_glyph_matrix_representation)-1

    while pixelCoordsToAnalyse:
        (pixelX, pixelY) = pixelCoordNow = pixelCoordsToAnalyse.pop(0)
        if pixelCoordNow in pixelCoordsAnalysed: continue

        pixelCoordsAnalysed.add(pixelCoordNow)

        if pixelGroup_glyph_matrix_representation[pixelY][pixelX].representedPixelGroupName != img_0_pixels.pixelTypeForegroundActive:
            pixelCoordsOutside_glyph.add(pixelCoordNow)

            neighbours = img_1_pixel_select.coords_neighbours(
                pixelCoordNow[0], pixelCoordNow[1], 0, 0,
                x_max_in_representation, y_max_in_representation, allowedDirections={1, 3, 5, 7})

            for neighbourXyCoord in neighbours:
                pixelCoordsToAnalyse.append(neighbourXyCoord)


    ############################################################
    pixelGroup_outside_the_char = img_0_pixels.PixelGroup_Glyph()
    for (xOutside, yOutside) in pixelCoordsOutside_glyph:
        pixelGroup_outside_the_char.add_pixel_active(xOutside, yOutside, (1,1,1))

    print(f"pixels outside the character: {len(pixelCoordsOutside_glyph)} elems")
    pixelGroup_outside_the_char.matrix_representation_refresh()
    pixelGroup_outside_the_char.matrix_representation_display_in_terminal()

    print(pixelCoordsOutside_glyph)





    # raise ValueError(42)
    return 42  # fake number,
