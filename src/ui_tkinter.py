# -*- coding: utf-8 -*-
import util, os

ErrorsLocal = []

try:    import tkinter as Tkinter
except ImportError: ErrorsLocal.append("install.missing.module_tkinter")

try:    from PIL import Image
except ImportError: ErrorsLocal.append("install.missing.module_pillow")

try:    from PIL import ImageTk
except ImportError: ErrorsLocal.append("install.missing.package_ImageTk")

def window_main(Prg):
    # I collect the msg NOT in the if because if one of them is missing, it causes Error
    for ErrTxtKey in ErrorsLocal:
        Prg["Errors"].append(util.ui_msg(Prg, ErrTxtKey))

    if Prg["Errors"]: return

    print("Tkinter ui main interface")
    Window = window_new(Prg, "window.main.title")

    FrameSourcePages = Tkinter.Frame(Window)
    FrameOnePage = Tkinter.Frame(Window)
    FrameTextRecognised = Tkinter.Frame(Window)

    Img = image_file_load_to_tk(Prg, "resources/deepcopy_logo_64.png")
    if Img:
        Panel = Tkinter.Label(FrameSourcePages, image=Img)
        Panel.pack(side="bottom", fill="both", expand="yes")
        Tkinter.Label(FrameOnePage, text="Frame One Page").pack()
        Tkinter.Label(FrameTextRecognised, text="Text Recognised").pack()

    FrameSourcePages.pack()
    FrameOnePage.pack()
    FrameTextRecognised.pack()
    Window.mainloop()

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

