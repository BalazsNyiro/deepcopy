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
import img_10_pixels
import img_13_pixel_select
from img_10_pixels import PixelGroup_Glyph


def statistics_collect_about_pixelgroups(pixelGroups_glyphs_all: dict[int, img_10_pixels.PixelGroup_Glyph]) -> dict[int, dict[str, int|list[PixelGroup_Glyph]]]:
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
    stats_of_pixelGroups_glyphs: dict[int, dict[str, int|list[PixelGroup_Glyph] ]] = dict()
    # list[list[(int, int)]] |       # list of (list of pixels)
    # int |
    # dict[int, int]

    for pixelGroup_id, pixelGroup_glyph in pixelGroups_glyphs_all.items():

        if not pixelGroup_glyph.pixels: continue
        # theoretically this is not possible, practically it's a validation

        pixelGroup_glyph.matrix_representation_refresh((1, 1, 1, 1))
        pixelGroup_glyph.matrix_representation_display_in_terminal(refreshTheMatrix=False)

        stats_of_pixelGroups_glyphs[pixelGroup_glyph.groupId] = dict()

        groupsInactive, errorsClosedInactive = glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph__emptyBorderHasToBePreparedAroundMatrix( pixelGroup_glyph, checkEmptyBorderAroundMatrixRepresentation=False)
        if not errorsClosedInactive:
            stats_of_pixelGroups_glyphs[pixelGroup_glyph.groupId]["glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph"] = groupsInactive

    return stats_of_pixelGroups_glyphs


def glyph_stat_collect_enclosed_inactive_unavailable_segments_in_glyph__emptyBorderHasToBePreparedAroundMatrix(
        pixelGroup_glyph: img_10_pixels.PixelGroup_Glyph,
        checkEmptyBorderAroundMatrixRepresentation: bool = True
) -> tuple[list[img_10_pixels.PixelGroup_Glyph], list[str]]:
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


    """
    ABC_Eng_Upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ABC_Eng_Lower = "abcdefghijklmnopqrstuvwxyz"
    numbers:  1234567890
    
    TODO: 
     - detect closed pixel groups
     - in all directions detect the average thickness of pixels around the group
     - the pixelgroup and surrounding circle can be safely selected
     - the extra elems, 'd': the top-right upper line can be isolated, as a OUTSIDE-CIRCLE elem
     - method 2:
       - around the group, always select one layer of active pixels, until in all directions you reach the end,
       - so only the inactive group and the surrounding circle will be selected.
       
       circles and relations:
       qp dp db
       
       circles:
       abdegopq6890"
       ABDOPQR"
   
   
    =======================================================
    
    where there is no closed group in convex-hull, there are lignes:
    (next to open groups: XXX pattern:)
    
          .****.
          *....* 
          *****. 
          *XXXX 
          .****.
    
     
    ======================================================= 
    
    """

    errorsInStatClosedInactive: list[str] = []

    ######################## This validation can be turned off IF the caller has a declared border creation in matrix representation ##########
    # def matrix_representation_has_emptyborder_around_glyph()
    if checkEmptyBorderAroundMatrixRepresentation:
        if not img_10_pixels.pixelGroup_matrix_representation_has_emptyborder_around_glyph(
            pixelGroup_glyph.matrix_representation, raiseExceptionIfNoBorder=False):
            errorsInStatClosedInactive.append(f"no empty border around glyph: \n{img_10_pixels.pixelGroup_matrix_representation_convert_to_str__forHumanReadingInTerminal(pixelGroup_glyph.matrix_representation)}\n\n")
    ######################## This validation can be turned off IF the caller has a declared border creation in matrix representation ##########



    ############ VISUALISE THE COLLECTED PIXELGROUP: ################################################
    # at this point we know that the matrix has an empty border, so the outside pixels can be collected
    pixelCoordsOutside_Glyph_collector = img_13_pixel_select.coords_drop_collect_pixelgroups_from_starting_point(
        pixelGroup_glyph.matrix_representation, allowedDirections={1, 3, 5, 7}, wantedRepresentedPixelGroupNames={img_10_pixels.pixelsNameBackgroundInactive})
    # print(f"0 - pixels outside the character: {len(pixelCoordsOutside_Glyph_collector.pixels)} elems")
    # pixelCoordsOutside_Glyph_collector.matrix_representation_refresh()
    # pixelCoordsOutside_Glyph_collector.matrix_representation_display_in_terminal()


    ################## InsidePixelDetect ####################################
    (xAbsLeft, yAbsTop, xAbsRight, yAbsBottom), errorsInMatrix = pixelGroup_glyph.matrix_representation_xAbsLeft_yAbsTop_xAbsRight_yAbsBottom()
    if errorsInMatrix:
        errorsInStatClosedInactive.extend(errorsInMatrix)

    insideGroups = []

    if not errorsInStatClosedInactive:

        # create an empty pixel collector
        insidePixelCollector = img_10_pixels.PixelGroup_Glyph()

        # add all coords in the total area of the glyph:
        insidePixelCollector.pixels_fill_coordinates(xStart=xAbsLeft, yStart=yAbsTop, xEnd=xAbsRight, yEnd=yAbsBottom)

        # remove external pixels, from the outside border to the direction of inside representation
        insidePixelCollector.pixels_remove(list(pixelCoordsOutside_Glyph_collector.pixels.keys()))

        # remove active pixels
        insidePixelCollector.pixels_remove(list(pixelGroup_glyph.pixels.keys()))

        # print(f"1 - pixels inside the character, isolated from outside pixels:")
        # insidePixelCollector.matrix_representation_display_in_terminal()


        # if the character was a 'T' for example, then insidePixelCollector.pixels is empty.
        # if the character has an internal group, in 'O' for example, then the
        # external border and the active O will be removed, but the internal
        # EMPTY pixels in the O char will be kept.

        # in other words: in pixels you can find the internal white groups now.

        while insidePixelCollector.has_pixels():
            if not insidePixelCollector.has_pixels(): break

            # input(f"{removeCounter} --> <ENTER>, inside pixel collector pixels: {insidePixelCollector.pixels.keys()}  representedNames: {insidePixelCollector.representedPixelGroupNames}")
            insidePixelCollector.matrix_representation_refresh()
            # print(f"matrix representation: {insidePixelCollector.matrix_representation}")

            activeRelativeMatrixCoords = img_10_pixels.pixelGroup_matrix_representation_collect_matrix_coords_with_represented_names(
                insidePixelCollector.matrix_representation, wantedRepresentedNames={img_10_pixels.pixelsNameForegroundActive}
            )
            oneCoordX, oneCoordY = activeRelativeMatrixCoords[0]

            emptyGroup = img_13_pixel_select.coords_drop_collect_pixelgroups_from_starting_point(
                insidePixelCollector.matrix_representation, allowedDirections={1, 3, 5, 7}, wantedRepresentedPixelGroupNames={img_10_pixels.pixelsNameForegroundActive},
                xStartInMatrix=oneCoordX, yStartInMatrix=oneCoordY
            )

            insidePixelCollector.pixels_remove(list(emptyGroup.pixels.keys()))

            if not emptyGroup.pixels:
                # print("no more pixels in empty Group")
                break

            insideGroups.append(emptyGroup)

    return insideGroups, errorsInStatClosedInactive
