# -*- coding: utf-8 -*-
import importlib
def window_main(Prg):

    if not importlib.util.find_spec("tkinter"):
        Prg["Errors"].append("Please install tkinter module! Ubuntu: sudo apt install python3-tk")

    if not importlib.util.find_spec("PIL"):
        Prg["Errors"].append("Please install Pillow module for image handling: http://python-pillow.github.io/")

    if Prg["Errors"]: return

    print("ui main interface")
