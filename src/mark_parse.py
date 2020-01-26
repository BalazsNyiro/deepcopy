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
    Area = mark_util.mark_to_area(Prg, Mark)

    #                   on right side you can find the closed empty areas:
    #     ....OOOOOOO...       signed with '.' chars,                         FFFFOOOOOOOFFF
    #     ..OOOOOOOOOO..       F means: fired/reached from outside            FFOOOOOOOOOOFF
    #     .OOOOOOOOOOOO.                                                      FOOOOOOOOOOOOF
    #     .OOOOO..OOOOO.                                                      FOOOOO..OOOOOF
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

    CharFire = "F"
    area.fire_from_side(Area, "Top",    [Fg], Directions="All", CharFire=CharFire)
    area.fire_from_side(Area, "Bottom", [Fg], Directions="All", CharFire=CharFire)
    area.fire_from_side(Area, "Left",   [Fg], Directions="All", CharFire=CharFire)
    area.fire_from_side(Area, "Right",  [Fg], Directions="All", CharFire=CharFire)

    # AreaStr = area.to_string(Area)
    # mark_info_insert(Prg, MarkStats, MarkId, [("mark_area_open", "\n" + AreaStr )])
    NumOfClosedEmptyPixels = area.pattern_count(Area, [Bg])

    MarkNumOfPixels = len(Mark.keys())
    MarkAreaClosedEmptyRatio = NumOfClosedEmptyPixels[Bg] / MarkNumOfPixels
    mark_info_insert(Prg, MarkStats, MarkId, [("mark_area_closed_empty_ratio", str(MarkAreaClosedEmptyRatio )  )])


    # TODO: num of closed area (above some %)
    # TODO: ratio of open area
    BlockVolume, BlockSizes = area.count_separated_blocks(Area, Bg, [Fg, CharFire])
    mark_info_insert(Prg, MarkStats, MarkId, [("separated_blocks_volume", str(BlockVolume)  )])
    mark_info_insert(Prg, MarkStats, MarkId, [("separated_blocks_sizes", str(BlockSizes)  )])


def mark_area_convex(Prg, Marks, MarkId, MarkStats):
    Mark = Marks[MarkId]
    AreaConvex = mark_util.mark_area_convex(Prg, Mark)
    mark_info_insert(Prg, MarkStats, MarkId, [("mark_area_convex", "\n" + area.to_string(AreaConvex))])


def mark_hull_convex(Prg, Marks, MarkId, MarkStats):
    # TODO: implement it, based on convex_area
    pass

def mark_info_basic(Prg, Marks, MarkId, MarkStats):
    Xmin, Xmax, Ymin, Ymax, Width, Height = mark_util.mark_min_max_width_height(Prg, Marks[MarkId])

    mark_info_insert(Prg, MarkStats, MarkId, [
        ("width",  Width),
        ("height", Height),
        ("area_bounding_box", Width*Height),
        ("pixelnum", len(Marks[MarkId])),
        ("x_min", Xmin),
        ("x_max", Xmax),
        ("y_min", Ymin),
        ("y_max", Ymax),
    ])

    return "parser mark_width_height: " + str(Width) + ", " + str(Height)

def mark_info_insert(_Prg, MarkStats, MarkId, KeyVals):
    Mark = MarkStats[MarkId]
    for Key, Val in KeyVals:

        if Key in Mark:
            print("ERROR: owerwrite existing key: " + Key + "  oldval: " + Mark[Key] + "   new val:" + Val)
        Mark[Key] = Val

        if len(Key) > MarkStats["keywords_len_max"]:
            MarkStats["keywords_len_max"] = len(Key)


