# -*- coding: utf-8 -*-

import platform, sys, json, os, importlib, gzip


def installed_environment_detect(Prg):
    Major, Minor = [int(Num) for Num in platform.python_version().split(".")[0:2]]

    if Major < 3:
        Prg["Errors"].append("Please use deepcopy with minimum Python 3.7!")

    if Major == 3 and Minor < 7:
        Prg["Warnings"].append("Tested with Python 3.7. Maybe it works with older versions.")

# def module_import_

# Real situation: PIL is available but ImageTk is not.
# so module_available is not totally enough to successful import.
def module_available(Prg, ModuleName, Msg):
    if not importlib.util.find_spec(ModuleName):
        Prg["Errors"].append(Msg)
        return False
    return True

def os_detect(Prg):
    Os = Prg["Os"] = platform.system() 
    print(ui_msg(Prg, "os_detect.detected").format(Os))
    if Os != "Linux" and Os != "Windows":
        Prg["Errors"].append("Not supported Os detected: {:s}".format(Os))
        if Os == "Darwin": 
            Prg["Warnings"].append("Theoretically DeepCopy can run on Mac if the necessary external commands are available, TODO in the future")

def ui_msg_init(Prg):
    Txt = file_read_all( os.path.join(Prg["DirPrgParent"], "resources", "ui_messages.json"))
    Prg["UiMessages"] = json.loads(Txt)

# MsgPath example: os_detect.detected
# if we process an error message and later the program can be broken,
# we print the message immediately
def ui_msg(Prg, MsgPath, PrintInTerminal=False):

    # it can handle one path or list of paths
    if isinstance(MsgPath, list):
        Texts = []
        for Path in MsgPath:
            Texts.append(ui_msg(Prg, Path))
        return Texts

    Container = Prg["UiMessages"]
    for Key in MsgPath.split("."):
        if Key in Container:
            Container = Container[Key]
        else:
            Msg = "Ui message key is unknown: " + Prg["UiLanguage"] + " - " + MsgPath
            Prg["Errors"].append(Msg)
            if PrintInTerminal: print(Msg)
            return Msg

    # check: eng msg always has to be defined
    if "eng" not in Container:
        Msg = "Ui message, default eng translation is missing: " + MsgPath
        Prg["Errors"].append(Msg)
        if PrintInTerminal: print(Msg)
        return Msg

    # here we get one lang block, for example: {"eng": "menu", "hun":"menü"}
    if Prg["UiLanguage"] in Container:
        return Container[Prg["UiLanguage"]]
    else:
        if "eng" in Container:
            Prg["Warnings"].append("Ui message is unknown: " + Prg["UiLanguage"] + " - " + MsgPath)
            return Container["eng"]


def warning_display(Prg):
    list_display(Prg["Warnings"], "Warnings:")
def error_display(Prg):
    list_display(Prg["Errors"], "Errors:")
    if Prg["Errors"]:
        print("\nBecause of these errors DeepCopy exists:")
        sys.exit(1)
def list_display(List, Title):
    if not List:
        return
    print("== {:s} ==".format(Title))
    for L in List:
        print(L)
##################################

def file_read_all(Fname="", Mode="r"): # if you want read binary, write "rb"
    Content = ""
    if file_test(Fname, MsgErr="File doesn't exists: '" + Fname + "'"):
        with open(Fname, Mode) as f:
            Content = f.read()
    return Content

def file_read_lines(Prg, Fname="", ErrMsgNoFile="", ErrExit=False, Strip=False):
    if Prg["Errors"]:
        print("file_read_lines, Return because errors")
        return

    if isinstance(Fname, list):
        Files = Fname
        Out = []
        for File in Files:
            Out.extend(file_read_lines(File, ErrMsgNoFile=ErrMsgNoFile, ErrExit=ErrExit, Strip=Strip)) 
        return Out

    if file_test(Fname):
        with open(Fname, 'r') as F:
            if Strip:
                return [L.strip() for L in F.readlines()]
            else:
                return F.readlines()

    elif ErrMsgNoFile:
        Prg["Errors"].append(ErrMsgNoFile)
        print(ErrMsgNoFile)
        if ErrExit:
            sys.exit(1)
    return []

def file_test(Fn="", MsgErr="", ErrExit=False, PrintHardExit=False, MsgOk=""):
    Ret=True
    if not os.path.isfile(Fn):
        Ret=False
        if len(MsgErr):
            print(MsgErr + " " + Fn) 
        if ErrExit:
            if PrintHardExit:
                print("\nFile test, hard exit:", Fn) # TODO: use lang output
            sys.exit(1)
    else:
        if MsgOk:
            print(MsgOk)

    return Ret


def file_append(Prg, Fname="", Content="",
                Mode="a"):  # you can append in binary mode, too
    file_write(Prg, Fname=Fname, Content=Content, Mode=Mode)


def file_write(Prg, Fname="", Content="", Mode="w", Gzipped=False, CompressLevel=9):
    if not Fname:
        Prg["Errors"].append("file_write error: not fname")
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
        Prg["Errors"].append("file_write error: " + Fname)
        return False

def dir_create_if_necessary(Prg, Path):
    if not os.path.isdir(Path):
        os.mkdir(Path)

def img_load_into_prg_structure(Prg, FileSelectedPath,
                                ImgId,
                                PixelsPreview = None,
                                PixelsPreviewImg = None,
                                ImageTkPhotoImageThumbnail = None,
                                ):

    Pixels, PixelDataSize, ImgWidth, ImgHeight = img_load_pixels(Prg, FileSelectedPath)  # RGB has 3 integers, RGBA has 4, Grayscale has 1 integer
    if Prg["Errors"]: return

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


def img_load_pixels(Prg, ImgPath, Timer=False):
    try:
        from PIL import Image
    except ImportError:
        Prg["Errors"].append("install.missing.module_pillow")
        return

    ImgOriginal = Image.open(ImgPath)
    ImgWidth, ImgHeight = ImgOriginal.size

    # detect once that it's RGB or RGBA (3 or 4 elements in the tuple)
    PixelSample = ImgOriginal.getpixel((0, 0))
    PixelDataSize = len(PixelSample)
    print("Pixel Data size: ", PixelDataSize)

    Pixels = ImgOriginal.load()

    return Pixels, PixelDataSize, ImgWidth, ImgHeight

def img_generate_id_for_loaded_list(Prg, PreFix="", PostFix=""):
    NumOfLoadedPics = len(Prg["ImagesLoaded"].keys())
    if PreFix: PreFix += "_"
    if PostFix: PostFix = "_" + PostFix
    return "{:s}{:d}{:s}".format(PreFix, NumOfLoadedPics + 1, PostFix)

