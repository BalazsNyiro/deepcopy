# -*- coding: utf-8 -*-
import util

def window_main(Prg):
    # I collect the msg NOT in the if because if one of them is missing, it's
    # an immediatelly test

    MsgTk = util.ui_msg(Prg, "install.missing.module_tkinter")
    MsgPil = util.ui_msg(Prg, "install.missing.module_pillow")
    MsgImageTk = util.ui_msg(Prg, "install.missing.package_ImageTk")

    if util.module_available(Prg, "tkinter", MsgTk):
        import tkinter as Tkinter

    if util.module_available(Prg, "PIL", MsgPil):
        from PIL import Image
        try: # if PIL is available, you have to check ImageTk too in PIL
            from PIL import ImageTk
        except:
            Prg["Errors"].append(MsgImageTk)

    if Prg["Errors"]: return

    print("ui main interface")
    Window = Tkinter.Tk()
    Window.title(util.ui_msg(Prg, "window.main.title"))

    Load = Image.open("resources/deepcopy_logo_64.png")
    Img = ImageTk.PhotoImage(Load)
    Panel = Tkinter.Label(Window, image=Img)
    Panel.pack(side="bottom", fill="both", expand="yes")

    Window.mainloop()
