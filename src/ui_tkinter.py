# -*- coding: utf-8 -*-
import util

# MsgTk = util.ui_msg(Prg, "install.missing.module_tkinter")
# MsgPil = util.ui_msg(Prg, "install.missing.module_pillow")
# MsgImageTk = util.ui_msg(Prg, "install.missing.module_imagetk")
# FIXME: how use here Prg variable???? to use language messages
if util.module_available(dict(), "tkinter", "install tkinter"): from tkinter import *
if util.module_available(dict(), "PIL", "install PIL"): from PIL import Image
if util.module_available(dict(), "PIL", "install PIL/ImageTk in synaptic"): from PIL import ImageTk

def window_main(Prg):
    # I collect the msg NOT in the if because if one of them is missing, it's
    # an immediatelly test


    if Prg["Errors"]: return

    print("ui main interface")
    Window = Tk()
    Window.title(util.ui_msg(Prg, "window.main.title"))

    Load = Image.open("resources/deepcopy_logo_64.png")
    Img = ImageTk.PhotoImage(Load)
    Panel = Label(Window, image=Img)
    Panel.pack(side="bottom", fill="both", expand="yes")

    Window.mainloop()
