import svg, util
def neighbours_to_svg(Prg, NeighBours, Spirals, Fname="svg_neighbours.html"):
    SvgObj = svg.new_object()
    for CoordSpiralCenter, CoordsConnected in NeighBours.items():
        for CoordConnected in CoordsConnected:
            # print(Fname, "Debug:", CoordSpiralCenter, CoordConnected)
            svg.line(SvgObj, CoordSpiralCenter, CoordConnected, StrokeWidth=len(Spirals[CoordSpiralCenter]))

    # the dot has to cover the lines
    for CoordSpiralCenter, CoordsConnected in NeighBours.items():
        svg.dot(SvgObj, CoordSpiralCenter, R=len(Spirals[CoordSpiralCenter]))
        svg.text(SvgObj, CoordSpiralCenter, str(CoordSpiralCenter), Color="green", ShiftXAbs=-20)

    SvgSrc = svg.pack(SvgObj)
    # print(SvgSrc)
    util.file_write(Prg, Fname=Fname, Content=SvgSrc)
