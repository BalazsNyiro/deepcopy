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

    MainHeight = 600
    FrameSourcePages = Tkinter.Frame(Window, bg='cyan', width=350, height=MainHeight, pady=3).grid(row=0, columnspan=3)
    FrameOnePage = Tkinter.Frame(Window, bg='purple', width=800, height=MainHeight, pady=3).grid(row=0, columnspan=3)
    FrameTextRecognised = Tkinter.Frame(Window)

    Img = image_file_load_to_tk(Prg, "resources/deepcopy_logo_64.png")
    if Img:
        Panel = Tkinter.Label(FrameSourcePages, image=Img)
        Panel.grid(row=0)
        Tkinter.Label(FrameOnePage, text="Frame One Page").grid(row=0)
        Tkinter.Label(FrameTextRecognised, text="Text Recognised").pack()

    # top_frame = Frame(root, bg='cyan', width = 450, height=50, pady=3).grid(row=0, columnspan=3)
    # FrameSourcePages.grid(row=0, column=0, sticky='e')

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

