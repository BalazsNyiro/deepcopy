def new_object():
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

def line(SvgObj, Coord1, Coord2, Color="red", StrokeWidth=2):

    X1, Y1 = Coord1
    X2, Y2 = Coord2
    # SCALING and Left + Top Margin
    X1 = SvgObj["Margin"] + X1 * SvgObj["Scale"]
    Y1 = SvgObj["Margin"] + Y1 * SvgObj["Scale"]
    X2 = SvgObj["Margin"] + X2 * SvgObj["Scale"]
    Y2 = SvgObj["Margin"] + Y2 * SvgObj["Scale"]

    obj_set_width_height(SvgObj, (X1, Y1))
    obj_set_width_height(SvgObj, (X2, Y2))

    SvgObj["Src"].append("""<line x1="{:d}" y1="{:d}" x2="{:d}" y2="{:d}" style="stroke:rgb({:s});stroke-width:{:d}" />""".format(X1, Y1, X2, Y2, Colors[Color], StrokeWidth))

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
