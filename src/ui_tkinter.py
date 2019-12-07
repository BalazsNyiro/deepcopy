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
    # store passed Prg as a global variable, too, because Tkinter buttons need a state
    # I collect the msg NOT in the if because if one of them is missing, it causes Error
    for ErrTxtKey in ErrorsLocal:
        Prg["Errors"].append(util.ui_msg(Prg, ErrTxtKey))

    if Prg["Errors"]: return

    global PrgGlobal
    PrgGlobal = Prg
    Prg["Tkinter"] = {"images_loaded": {}}

    print("Tkinter ui main interface")
    MainWidth = 1200
    MainHeight = 800

    Window = window_new(Prg, "window.main.title")
    Window.geometry('{}x{}'.format(MainWidth, MainHeight))
    Prg["Tkinter"]["Window"] = Window

    SourceWidth = 300
    OnePageWidth = 600
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
    B = Tkinter.Button(FrameSourcePages, text="Hello", command=files_thumbnails_load_button)
    B.pack()


    Tkinter.Label(FrameTextRecognised, text="Text Recognised").grid(row=0, column=2)

    # top_frame = Frame(root, bg='cyan', width = 450, height=50, pady=3).grid(row=0, columnspan=3)
    # FrameSourcePages.grid(row=0, column=0, sticky='e')

    Window.mainloop()

# FIXME: dynamic image inserting doesn't work correctly
# https://python-forum.io/Thread-Tkinter-How-do-I-change-an-image-dynamically
# ??
def files_thumbnails_load_button():
    Prg = PrgGlobal
    files_thumbnails_load(Prg, Prg["Tkinter"]["FrameSourcePages"], Prg["Tkinter"]["Window"])
    print("button")
def files_thumbnails_load(Prg, Parent, Window):
    for FileSelected in files_selector(Prg):
        ImgId = img_generate_id_for_loaded_list(Prg, "thumbnalis")
        Img = image_file_load_to_tk(Prg, FileSelected)
        Img.ImgId = ImgId # all image knows his own id, if you want to remove them, delete them from loaded image list
        print("img type: ", type(Img))

        Prg["Tkinter"]["images_loaded"][ImgId] = Img # save reference of Img, otherwise garbace collector remove it

        if Img:
            Panel = Tkinter.Label(Parent, image=Img)
            Panel.pack()
            Window.update_idletasks()

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

