import svg, util
def neighbours_to_svg(Prg, NeighBours):
    SvgObj = svg.new_object()
    for CoordSpiralCenter, CoordsConnected in NeighBours.items():
        for CoordConnected in CoordsConnected:
            svg.line(SvgObj, CoordSpiralCenter, CoordConnected)

    # the dot has to cover the lines
    for CoordSpiralCenter, CoordsConnected in NeighBours.items():
        svg.dot(SvgObj, CoordSpiralCenter, R=len(CoordsConnected))

    SvgSrc = svg.pack(SvgObj)
    # print(SvgSrc)
    util.file_write(Prg, Fname="svg_neighbours.html", Content=SvgSrc)
