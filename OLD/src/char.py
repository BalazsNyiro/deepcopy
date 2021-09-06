import svg, util
def neighbours_to_svg(Prg, NeighBours, Spirals, Fname="svg_neighbours.html"):
    SvgObj = svg.obj_new()
    for CoordSpiralCenter, CoordsConnected in NeighBours.items():
        for CoordConnected in CoordsConnected:
            # print(Fname, "Debug:", CoordSpiralCenter, CoordConnected)
            SpiralLen = len(Spirals[CoordSpiralCenter])
            # Dash = str(SpiralLen) + "," + str(SpiralLen)
            svg.line(SvgObj, CoordSpiralCenter, CoordConnected, StrokeWidth=SpiralLen, HalfLine=True)

    # the dot has to cover the lines
    for CoordSpiralCenter, CoordsConnected in NeighBours.items():
        svg.dot(SvgObj, CoordSpiralCenter, R=len(Spirals[CoordSpiralCenter]))
        svg.text(SvgObj, CoordSpiralCenter, str(CoordSpiralCenter), Color="green", ShiftXAbs=-20)

    SvgSrc = svg.pack(SvgObj)
    # print(SvgSrc)
    util.file_write(Prg, Fname=Fname, Content=SvgSrc)

def path_in_char_to_svg(Prg, Paths, Spirals, Fname="svg_paths_in_char.html"):
    SvgObj = svg.obj_new()

    # the dot has to cover the lines
    print("")
    print("Paths:", Paths)
    for Path in Paths:
        SpiralPrev = None
        for Spiral in Path:
            if SpiralPrev:
                svg.line(SvgObj, Spiral, SpiralPrev, StrokeWidth=5)

            print("path in char, svg, Spiral: ", Spiral)
            svg.dot(SvgObj, Spiral, R=len(Spirals[Spiral]))
            svg.text(SvgObj, Spiral, str(Spiral), Color="green", ShiftXAbs=-20)
            SpiralPrev = Spiral

    SvgSrc = svg.pack(SvgObj)
    # print(SvgSrc)
    util.file_write(Prg, Fname=Fname, Content=SvgSrc)
