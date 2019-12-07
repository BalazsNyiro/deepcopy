# -*- coding: utf-8 -*-
import util, os, time
PrgGlobal = None
ErrorsLocal = []

try:
    import tkinter as Tkinter
    import tkinter.filedialog as FileDialog
except ImportError: ErrorsLocal.append("install.missing.module_tkinter")

try:    from PIL import Image
except ImportError: ErrorsLocal.append("install.missing.module_pillow")

try:    from PIL import ImageTk
except ImportError: ErrorsLocal.append("install.missing.package_ImageTk")

def window_main(Prg):
    for ErrTxtKey in ErrorsLocal:
        Prg["Errors"].append(util.ui_msg(Prg, ErrTxtKey))

    if Prg["Errors"]: return

    # store passed Prg as a global variable, too, because Tkinter buttons need a state
    # I collect the msg NOT in the if because if one of them is missing, it causes Error
    global PrgGlobal
    PrgGlobal = Prg

    Prg["Tkinter"] = {"images_loaded": {}}

    MainWidth = 1200
    MainHeight = 800
    SourceWidth = 300
    OnePageWidth = 600

    Window = window_new(Prg, "window.main.title")
    Window.geometry('{}x{}'.format(MainWidth, MainHeight))
    Prg["Tkinter"]["Window"] = Window

    TextRecognisedWidth = MainWidth - SourceWidth - OnePageWidth

    FrameSourcePages = frame_new(Prg, Window, SourceWidth, MainHeight, bg="yellow")
    FrameSourcePages.grid(row=0, column=0, rowspan=3)

    FrameOnePage = frame_new(Prg, Window, OnePageWidth, MainHeight)
    FrameOnePage.grid(row=0, column=1, rowspan=3)

    FrameTextRecognised = frame_new(Prg, Window, TextRecognisedWidth, MainHeight, bg="green")
    FrameTextRecognised.grid(row=0, column=2, rowspan=3)

    Tkinter.Label(FrameOnePage, text="Frame One Page").grid(row=0, column=1)
    Tkinter.Label(FrameOnePage, text="2222").grid(row=1, column=1)

    Prg["Tkinter"]["FrameSourcePages"] = FrameSourcePages
    Tkinter.Button(FrameSourcePages, text=util.ui_msg(Prg, "file_operation.file_load_into_thumbnail_list"), command=files_thumbnails_load_button_cmd).pack()

    Tkinter.Label(FrameTextRecognised, text="Text Recognised").grid(row=0, column=2)

    Window.mainloop()

def files_thumbnails_load_button_cmd(): # it is called from Ui so we use global state to store objects.
    Prg = PrgGlobal
    Parent = Prg["Tkinter"]["FrameSourcePages"]

    for FileSelected in files_selector(Prg):
        ImgId = img_generate_id_for_loaded_list(Prg, "thumbnalis")

        # FIXME: FileSelected is the original file.
        # HERE WE HAVE TO CREATE A THUMBNAIL into TMP dir and load that one
        # AND SAVE INTO Thumbnail's original_source attribute the original path

        Img = image_file_load_to_tk(Prg, FileSelected)
        if Img:
            Img.ImgId = ImgId # all image knows his own id, if you want to remove them, delete them from loaded image list
            Prg["Tkinter"]["images_loaded"][ImgId] = Img # save reference of Img, otherwise garbace collector remove it
            Panel = Tkinter.Label(Parent, image=Img)
            Panel.pack()

def files_selector(Prg):
    Dir = Prg["PathDefaultFileSelectDir"]
    print(Dir)
    return FileDialog.askopenfilenames(initialdir=Prg["PathDefaultFileSelectDir"], title="Select file",
                                       filetypes=( ("png files", "*.png"), ("jpeg files", "*.jpg"),("all files", "*.*")))

def img_generate_id_for_loaded_list(Prg, IdPlusText):
    NumOfLoadedPics = len(Prg["Tkinter"]["images_loaded"].keys())
    return "{:d}_{:s}".format(NumOfLoadedPics + 1, IdPlusText)

def frame_new(Prg, Parent, Width, Height, bg=""):
    return Tkinter.Frame(Parent, bg=bg, width=Width, height=Height,pady=3)

def window_new(Prg, TitleKey=""):
    Window = Tkinter.Tk()
    if TitleKey:
        Window.title(util.ui_msg(Prg, TitleKey))
    return Window

def image_file_load_to_tk(Prg, Path):
    if not os.path.isfile(Path):
        Msg = util.ui_msg(Prg, "file_operation.file_missing", PrintInTerminal=True)
        Prg["Warning"].append(Msg)
        return False

    Load = Image.open(Path)
    return ImageTk.PhotoImage(Load)

