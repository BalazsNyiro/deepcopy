def obj_new():
    return {    "Width": 0,
                "Height": 0,
                "Src": [],
                "Margin": 10,
                "Scale": 60
            }

def obj_set_width_height(SvgObj, Coord):
    X, Y = Coord
    X = X + SvgObj["Margin"] # right and bottom margin
    Y = Y + SvgObj["Margin"]
    if X > SvgObj["Width"]: SvgObj["Width"] = X
    if Y > SvgObj["Height"]: SvgObj["Height"] = Y

def pack(SvgObj):
    Width = SvgObj["Width"]
    Height = SvgObj["Height"]
    Src = "\n".join(SvgObj["Src"])

    return """<!DOCTYPE html><html>
              <body>
              <svg width="{:d}" height="{:d}">{:s}</svg>
              </body>
              </html>""".format(Width, Height, Src)

def text(SvgObj, Coord, Text, Color="black", ShiftXAbs=0):
    X, Y = Coord
    X = SvgObj["Margin"] + X * SvgObj["Scale"]
    Y = SvgObj["Margin"] + Y * SvgObj["Scale"]

    X = X + ShiftXAbs # Absolute shift, without scaling

    obj_set_width_height(SvgObj, (X, Y))

    SvgObj["Src"].append("""<text x="{:d}" y="{:d}" fill="rgb({:s})">{:s}</text>""".format(X, Y, Colors[Color], Text))

def line(SvgObj, CoordFrom, CoordTo, Color="red", StrokeWidth=2, HalfLine=False):

    XFrom, YFrom = CoordFrom
    XTo, YTo = CoordTo
    # SCALING and Left + Top Margin
    XFrom = SvgObj["Margin"] + XFrom * SvgObj["Scale"]
    YFrom = SvgObj["Margin"] + YFrom * SvgObj["Scale"]

    XTo = SvgObj["Margin"] + XTo * SvgObj["Scale"]
    YTo = SvgObj["Margin"] + YTo * SvgObj["Scale"]

    if HalfLine:
        XTo = int((XFrom + XTo)/2)
        YTo = int((YFrom + YTo)/2)

    obj_set_width_height(SvgObj, (XFrom, YFrom))
    obj_set_width_height(SvgObj, (XTo, YTo))

    SvgObj["Src"].append("""<line x1="{:d}" y1="{:d}" x2="{:d}" y2="{:d}" style="stroke:rgb({:s});stroke-width:{:d}" />""".format(XFrom, YFrom, XTo, YTo, Colors[Color], StrokeWidth))

def dot(SvgObj, Coord, FillColor="black", StrokeColor="red", StrokeWidth=2, R=2):

    X, Y = Coord
    X = SvgObj["Margin"] + X * SvgObj["Scale"]
    Y = SvgObj["Margin"] + Y * SvgObj["Scale"]
    R = R * 2 #SvgObj["Scale"]//20 # I don't want real scale in R
    # StrokeWidth = StrokeWidth * SvgObj["Scale"]
    obj_set_width_height(SvgObj, (X+R+StrokeWidth//2, Y+R+StrokeWidth//2))

    SvgObj["Src"].append("""<circle cx="{:d}" cy="{:d}" r="{:d}" stroke="{:s}" stroke-width="{:d}" fill="{:s}" />""".format(X,Y,R,Colors[StrokeColor], StrokeWidth,Colors[FillColor]))

Colors = {  "red": "255,0,0",
            "green": "0,255,0",
            "blue": "0,0,255",
            "white": "255,255,255",
            "black": "0,0,0"
            }
