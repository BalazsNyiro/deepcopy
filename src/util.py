# -*- coding: utf-8 -*-

import platform, json, os, importlib, gzip

def installed_environment_detect():
    Major, Minor = [int(Num) for Num in platform.python_version().split(".")[0:2]]

    if Major < 3:
        warning_display("Please use deepcopy with minimum Python 3.7!", "util:env detect min py 3")

    if Major == 3 and Minor < 7:
        warning_display("Tested with Python 3.7. Maybe it works with older versions.", "util:env detect, min 3.7")


def os_detect(Prg):
    Os = Prg["Os"] = platform.system() 
    print(ui_msg(Prg, "os_detect.detected").format(Os))
    if Os != "Linux" and Os != "Windows":
        warning_display("Not supported Os detected: {:s}".format(Os), "util:os_detect")
        if Os == "Darwin": 
            warning_display("Theoretically DeepCopy can run on Mac if the necessary external commands are available, TODO in the future", "util:os darwin")




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


def img_is_rgb(Img):
    Size = Img.get("PixelDataSize", -1)
    if Size == 3:
        return True
    return False


def img_is_grayscale(Img):
    Size = Img.get("PixelDataSize", -1)
    if Size == 1:
        return True
    return False



