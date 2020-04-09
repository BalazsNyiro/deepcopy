# -*- coding: utf-8 -*-

import platform, json, os, importlib, gzip

def installed_environment_detect():
    Major, Minor = [int(Num) for Num in platform.python_version().split(".")[0:2]]

    if Major < 3:
        warning_display("Please use deepcopy with minimum Python 3.7!", "util:env detect min py 3")

    if Major == 3 and Minor < 7:
        warning_display("Tested with Python 3.7. Maybe it works with older versions.", "util:env detect, min 3.7")

# def module_import_

# Real situation: PIL is available but ImageTk is not.
# so module_available is not totally enough to successful import.
# TESTED
def module_available(ModuleName, Msg):
    if not importlib.util.find_spec(ModuleName):
        warning_display(Msg, "util:module_available")
        return False
    return True

def os_detect(Prg):
    Os = Prg["Os"] = platform.system() 
    print(ui_msg(Prg, "os_detect.detected").format(Os))
    if Os != "Linux" and Os != "Windows":
        warning_display("Not supported Os detected: {:s}".format(Os), "util:os_detect")
        if Os == "Darwin": 
            warning_display("Theoretically DeepCopy can run on Mac if the necessary external commands are available, TODO in the future", "util:os darwin")

def ui_msg_init(Prg):
    Txt = file_read_all(Prg, os.path.join(Prg["DirPrgParent"], "resources", "ui_messages.json"))
    Prg["UiMessages"] = json.loads(Txt)

# MsgPath example: os_detect.detected
# if we process an error message and later the program can be broken,
# we print the message immediately
# TESTED
def ui_msg(Prg, MsgPath, TestCase=False):

    # it can handle one path or list of paths
    if isinstance(MsgPath, list):
        Texts = list()
        for Path in MsgPath:
            Texts.append(ui_msg(Prg, Path, TestCase=TestCase))
        return Texts

    Container = Prg["UiMessages"]
    for Key in MsgPath.split("."):
        if Key in Container:
            Container = Container[Key]
        else:
            Msg = "Ui message key is unknown in container: " + Prg["UiLanguage"] + " - " + MsgPath
            if not TestCase: # no messages from test execution
                warning_display(Msg, "util:ui_msg, key is unknown")
            return Msg

    # check: eng msg always has to be defined
    if "eng" not in Container:
        Msg = "Ui message, default eng translation is missing: " + MsgPath
        if not TestCase:
            warning_display(Msg, "util:ui_msg, eng missing")
        return Msg

    # here we get one lang block, for example: {"eng": "menu", "hun":"menü"}
    if Prg["UiLanguage"] in Container:
        return Container[Prg["UiLanguage"]]
    else:
        if "eng" in Container:
            if not TestCase:
                warning_display("Ui message is unknown: " + Prg["UiLanguage"] + " - " + MsgPath, "util:only_eng_in_container")
            return Container["eng"]


def warning_display(Msg, Caller="TODO FIX THE CALLER if you call it only with one Param"):
    print("Warning: ", Msg, " ("+Caller+")")

def error_display(Msg, Caller):
    MsgOut = "Error: " + str(Msg) +" ("+Caller+")"
    raise Exception(MsgOut)

def list_display(List, Title):
    if not List:
        return
    print("== {:s} ==".format(Title))
    for L in List:
        print(L)

# DOC: naive formatted dictionary display
def dict_display_simple_data(Dict, Title="",Prefix="  "):
    if Title:
        print(Title)

    KeyMaxLen = 0
    # find Max length in keys
    for Key in Dict:
        KeyLen = len(str(Key))
        if KeyLen > KeyMaxLen:
            KeyMaxLen = KeyLen

    for Key, Values in Dict.items():
        LengthInfo = " " + str(len(Values)) + " elem -> "
        print("{:s}{:>{Width}}{:>{WidthLenInfo}}{:s}".format(Prefix, str(Key), LengthInfo, str(Values), WidthLenInfo=12, Width=KeyMaxLen))
##################################

# TESTED
def file_read_all(Prg, Fname="", Mode="r"): # if you want read binary, write "rb"
    Content = ""
    if file_test(Prg, Fname, MsgErr="File doesn't exists: '" + Fname + "'"):
        with open(Fname, Mode) as f:
            Content = f.read()
    return Content

def file_read_lines(Prg, Fname="", ErrMsgNoFile="", ErrExit=False, Strip=False):
    if isinstance(Fname, list):
        Files = Fname
        Out = list()
        for File in Files:
            Out.extend(file_read_lines(Prg, File, ErrMsgNoFile=ErrMsgNoFile, ErrExit=ErrExit, Strip=Strip))
        return Out

    if file_test(Prg, Fname):
        with open(Fname, 'r') as F:
            if Strip:
                return [L.strip() for L in F.readlines()]
            else:
                return F.readlines()

    elif ErrMsgNoFile:
        if ErrExit:
            error_display(ErrMsgNoFile, "file_read_all, if ErrExit=True")
        else:
            warning_display(ErrMsgNoFile, "file_read_all, if ErrExit=False")
    return list()

# TESTED
def file_test(Prg, Fn="", MsgErr="", ErrExit=False, MsgOk=""):
    Ret=True
    if not os.path.isfile(Fn):
        Ret=False
        if not MsgErr:
            MsgErr = ui_msg(Prg, "file_operation.file_missing").format(Fn)
        else:
            MsgErr += MsgErr + "(" + Fn + ")"

        if ErrExit:
            error_display(MsgErr, "util:file_test")
        else:
            warning_display(MsgErr, "util:file_test")
    else:
        if MsgOk:
            print(MsgOk)
    return Ret


def file_append(Prg, Fname="", Content="",
                Mode="a"):  # you can append in binary mode, too
    file_write(Prg, Fname=Fname, Content=Content, Mode=Mode)


def file_write(Prg, Fname="", Content="", Mode="w", Gzipped=False, CompressLevel=9):
    if not Fname:
        warning_display("file_write error: not fname", "util:file_write, not Fname")
        return
    print("writing:", Fname)
    # if we received a list of string, convert it to string:
    if isinstance(Content, list):
        Content = '\n'.join(Content)

    if Gzipped:
        if not "b" in Mode:
            Mode = Mode + "b"
        OutputBytes = bytes(Content, 'utf-8')
        Content = gzip.compress(OutputBytes, CompressLevel)

    try:
        f = open(Fname, Mode)
        f.write(Content)
        f.close()
        return True
    except:
        warning_display("file_write error: " + Fname, "util:file_write, except")
        return False

def dir_create_if_necessary(Path):
    if not os.path.isdir(Path):
        os.mkdir(Path)

# Tested
def img_load_into_prg_structure__get_imgid(Prg, FilePathElems):
    FilePathImg = os.path.join(*FilePathElems)
    ImgId = img_generate_id_for_loaded_list(Prg, PreFix="thumbnail", PostFix=FilePathImg)
    img_load_into_prg_structure(Prg, FilePathImg, ImgId)
    Img = Prg["ImagesLoaded"][ImgId]
    return Img, ImgId

# Tested
def img_load_into_prg_structure(Prg, FileSelectedPath,
                                ImgId,
                                PixelsPreview = None,
                                PixelsPreviewImg = None,
                                ImageTkPhotoImageThumbnail = None,
                                ):
    file_test(Prg, FileSelectedPath, ErrExit=True)

    Pixels, PixelDataSize, ImgWidth, ImgHeight = img_load_pixels(Prg, FileSelectedPath)  # RGB has 3 integers, RGBA has 4, Grayscale has 1 integer

    #  example  "TextSelectCoords" : [    one bubble can contain any coordinate pairs
    #                                     [ [5,10], [256, 10], [256, 612], [5, 612] ]
    #                                ]
    TextSelectPreviewPixelsWidth = 0
    TextSelectPreviewPixelsHeight = 0
    if PixelsPreviewImg:
        TextSelectPreviewPixelsWidth = PixelsPreviewImg.size[0]
        TextSelectPreviewPixelsHeight = PixelsPreviewImg.size[1]

    Prg["ImagesLoaded"][ImgId] = {
        "Reference2avoidGarbageCollector": ImageTkPhotoImageThumbnail,
        # TODO: use empty TextSelectCoords by default
        "TextSelectCoords": [  [[10, 10], [10, 50], [50, 50], [50, 10]]   ],  # here can be lists, with coordinate pairs,
        "TextSelectPreviewPixels": PixelsPreview,
        "TextSelectPreviewPixelsWidth": TextSelectPreviewPixelsWidth,
        "TextSelectPreviewPixelsHeight": TextSelectPreviewPixelsHeight,
        "FilePathOriginal": FileSelectedPath,
        "Pixels": Pixels,
        "PixelDataSize": PixelDataSize,
        "Width": ImgWidth,
        "Height": ImgHeight
    }

# indirect tested only:
# util.img_load_into_prg_structure__get_imgid(Prg, FilePathElems)
#  -> img_load_into_prg_structure(Prg, FilePathImg, ImgId)
#    -> img_load_pixels()
def img_load_pixels(Prg, ImgPath, Timer=False):
    try:
        from PIL import Image
    except ImportError:
        error_display(ui_msg("install.missing.module_pillow"), "util:mg_load_pixels, PIL import")

    ImgOriginal = Image.open(ImgPath)
    ImgWidth, ImgHeight = ImgOriginal.size

    # detect once that it's RGB or RGBA (3 or 4 elements in the tuple)
    PixelSampleColorValue = ImgOriginal.getpixel((0, 0))
    # if it's a grayscale img, it't a simple int, not a tuple
    if isinstance(PixelSampleColorValue, int):
        PixelDataSize = 1
    else:
        PixelDataSize = len(PixelSampleColorValue) # RGB value has 3 elems, RGBA has 4
    print("Pixel Data size: ", PixelDataSize)

    Pixels = ImgOriginal.load()

    return Pixels, PixelDataSize, ImgWidth, ImgHeight

# TESTED
def img_generate_id_for_loaded_list(Prg, PreFix="", PostFix=""):
    NumOfLoadedPics = len(Prg["ImagesLoaded"].keys())
    if PreFix: PreFix += "_"
    if PostFix: PostFix = "_" + PostFix
    return "{:s}{:d}{:s}".format(PreFix, NumOfLoadedPics + 1, PostFix)

# TESTED
def img_is_rgb(Img):
    Size = Img.get("PixelDataSize", -1)
    if Size == 3:
        return True
    return False

# TESTED
def img_is_grayscale(Img):
    Size = Img.get("PixelDataSize", -1)
    if Size == 1:
        return True
    return False

# TESTED, neighbour coord order:
#   CDE
#   B F
#   AHG
def coords_neighbour_points(Coord):
    X, Y = Coord
    return [
        (X - 1, Y + 1),
        (X - 1, Y    ),
        (X - 1, Y - 1),
        (X,     Y - 1),
        (X + 1, Y - 1),
        (X + 1, Y    ),
        (X + 1, Y + 1),
        (X,     Y + 1),
    ]

# it's a very often used func.
# I want to avoid extract values so I didn't receive
# coords as a tuple.
# TESTED
def coords_connect_fromA_toB_with_points(Ax, Ay, Bx, By):

    DeltaX = Bx - Ax
    DeltaY = By - Ay

    StepY = 1
    if Ay > By:
        StepY = -1

    StepX = 1
    if Ax > Bx:
        StepX = -1

    Points = list()
    # print("\n>>>", Ax, Ay, ",  ", Bx, By)

    RangeX = range(Ax, Bx + StepX, StepX)
    RangeY = range(Ay, By + StepY, StepY)

    # simple case: only X is moving
    if DeltaY == 0:
        Y = Ay
        for X in RangeX:
            Points.append((X,Y))

    # simple case: only Y is moving
    elif DeltaX == 0:
        X = Ax
        for Y in RangeY:
            Points.append((X,Y))

    else: # X and Y is moving, not horizontal/vertical steps

        # if we move nearly vertically,
        # for example: connect_coords(2, 1, 1, 4)
        # then in vertical axis there are much more fine Y steps 1,2,3,4
        # then in horizontal axis where we can use these two X steps: 2,1
        # So the choosen step order depends on the absolute value of deltas

        if abs(DeltaX) >= abs(DeltaY):
            Y = Ay
            YchangePerUnit = float(DeltaY) / abs(DeltaX)

            Step = 0
            for X in RangeX:
                PointCalculated = (X, int(round(Y+YchangePerUnit*Step) ) )
                Points.append(PointCalculated)
                Step += 1

        else: ##### abs(DeltaX) < abs(DeltaY) #####
            X = Ax
            XchangePerUnit = float(DeltaX) / abs(DeltaY)

            Step = 0
            for Y in RangeY:
                PointCalculated = (  int(round(X+XchangePerUnit*Step)), Y )
                Points.append(PointCalculated)
                Step += 1

    return Points

# find the middle of two coordinates
def coord_middle(CoordA, CoordB):
    XA, YA = CoordA
    XB, YB = CoordB
    return(int((XA+XB)/2), int((YA+YB)/2))

# TESTED
def txt_multiline_insert_prefix(TextWithNewlines, Prefix=">> "):
    Formatted = list()
    for Line in TextWithNewlines.split("\n"):
        Formatted.append(Prefix + Line)
    return "\n".join(Formatted)


