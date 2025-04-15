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
        print(f"matrix representation 1: {pixelGroup_glyph.matrix_representation}")

        stats_of_pixelGroups_glyphs[pixelGroup_glyph.groupId] = {
            "glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph":
                glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph(pixelGroup_glyph.matrix_representation)}




    return stats_of_pixelGroups_glyphs


def glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph(pixelGroup_glyph_matrix_representation: list[list[img_0_pixels.PixelGroup_Glyph]] ) -> int: #  list[ list[(int, int) ] ]:
    """count the closed inactive segments inside of a glyph.

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

    # return list( list(1, 2))
    print(f"matrix representation 2: {pixelGroup_glyph_matrix_representation}")
    print(f" create a general 'drop' function with gravity_directions_at_start and gravity_directions_after_first_collision params ")

    return 42  # fake number,
