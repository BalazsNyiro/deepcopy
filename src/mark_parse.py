# -*- coding: utf-8 -*-
import area
import mark_util

# Mark analyser algorithms, main logic
# OutputType can be: human | data

# in '8' or 'B' chars there are 2 closed areas,
# in 'b' or 'e' or in 'o' there are one closed.
#
def mark_area_select_closed_empty_area(Prg, Marks, MarkId, MarkStats):
    Fg = mark_util.MarkFg
    Bg = mark_util.MarkBg

    Mark = Marks[MarkId]
    AreaFired = mark_util.mark_to_area(Prg, Mark)

    #                   on right side you can find the closed empty areas:
    #     ....OOOOOOO...       signed with '.' chars,                         FFFFOOOOOOOFFF
    #     ..OOOOOOOOOO..       F means: fired/reached from outside            FFOOOOOOOOOOFF
    #     .OOOOOOOOOOOO.                                                      FOOOOOOOOOOOOF
    #     .OOOOO..OOOOO.        the closed block size = 14 in this case:      FOOOOO..OOOOOF
    #     OOOO......OOOO                                                      OOOO......OOOO
    #     OOOO......OOOO                                                      OOOO......OOOO
    #     OOOOOOOOOOOOOO   all direction is important here, because:          OOOOOOOOOOOOOO
    #     OOOOOOOOOOOOOO                                                      OOOOOOOOOOOOOO
    #     OOO...........  in case of letter e, if you fire from right         OOOFFFFFFFFFFF
    #     OOOO..........  the *** chars will be empty because Bottom Fire     OOOOFFFFFFFFFF
    #     OOOO..........  can't go down basically,                            OOOOFFFFFFFFFF
    #     .OOOOOO***OOO.  and it fills the area with F sign                   FOOOOOOFFFOOOF
    #     .OOOOOOOOOOOO.  and can't fill *** with F so in this situation      FOOOOOOOOOOOOF
    #     ..OOOOOOOOOOO.  when starts a fire, it can spread                   FFOOOOOOOOOOOF
    #     ....OOOOOOOO..  into any direction                                  FFFFOOOOOOOOFF

    CharFire = "F" # Directions: not all, because if there is only 1 pixel wide frame around
    Directions = ["Left", "Right", "Up", "Down"] # the closed area, the fire can enter into it

    area.fire_from_side(AreaFired, "Top",    [Fg], Directions=Directions, CharFire=CharFire)
    area.fire_from_side(AreaFired, "Bottom", [Fg], Directions=Directions, CharFire=CharFire)
    area.fire_from_side(AreaFired, "Left",   [Fg], Directions=Directions, CharFire=CharFire)
    area.fire_from_side(AreaFired, "Right",  [Fg], Directions=Directions, CharFire=CharFire)

    AreaFiredInConvex = area.mask_with_convex_shape(AreaFired, mark_util.mark_area_convex(Prg, Mark), Fg, Bg)

    AreaStr = area.to_string(AreaFiredInConvex)
    mark_info_insert(Prg, MarkStats, MarkId, [("mark_area_open_in_convex", "\n" + AreaStr )])

    NumOfClosedEmptyPixels = area.pattern_count(AreaFired, [Bg])

    MarkNumOfPixels = len(Mark.keys())
    MarkAreaClosedEmptyRatio = NumOfClosedEmptyPixels[Bg] / MarkNumOfPixels
    mark_info_insert(Prg, MarkStats, MarkId, [("mark_area_closed_empty_ratio", str(MarkAreaClosedEmptyRatio )  )])


    # TODO: num of closed area (above some %)
    # TODO: ratio of open area
    BlockVolume, BlockSizes = area.count_separated_blocks(AreaFired, Bg, [Fg, CharFire])
    mark_info_insert(Prg, MarkStats, MarkId, [("separated_blocks_volume", str(BlockVolume)  )])
    mark_info_insert(Prg, MarkStats, MarkId, [("separated_blocks_sizes", str(BlockSizes)  )])

    # TODO: measure OPEN empty area: the lower part of e is open,
    # with area convex you can count the size of open area

def mark_area_convex(Prg, Marks, MarkId, MarkStats):
    Mark = Marks[MarkId]
    AreaConvex = mark_util.mark_area_convex(Prg, Mark)
    mark_info_insert(Prg, MarkStats, MarkId, [("mark_area_convex", "\n" + area.to_string(AreaConvex))])


def mark_info_basic(Prg, Marks, MarkId, MarkStats):
    Mark = Marks[MarkId]

    mark_info_insert(Prg, MarkStats, MarkId, [
        ("Width",  Mark["Width"]),
        ("Height", Mark["Height"]),
        ("Area_bounding_box", Mark["BoundingBox"]),
        ("Pixelnum", len(Marks[MarkId])),
        ("Xmin", Mark["Xmin"]),
        ("Xmax", Mark["Xmax"]),
        ("Ymin", Mark["Ymin"]),
        ("Ymax", Mark["Ymax"]),
    ], "mark_info_basic")

    return "parser mark_width_height: " + str(Mark["Width"]) + ", " + str(Mark["Height"])

def mark_info_insert(_Prg, MarkStats, MarkId, KeyVals, Caller=""):
    MarkStat = MarkStats[MarkId]
    for Key, Val in KeyVals:

        if Key in MarkStat:
            print("ERROR("+Caller+"): owerwrite existing key: " + str(Key) + "  oldval: " + str(MarkStat[Key]) + "   new val:" + str(Val))
        MarkStat[Key] = Val

        if len(Key) > MarkStats["keywords_len_max"]:
            MarkStats["keywords_len_max"] = len(Key)


