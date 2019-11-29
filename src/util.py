#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform, sys

# import language.py


def os_detect(Prg):
    Os = Prg["Os"] = platform.system() 
    print("Detected os:", Os)
    if Os != "Linux" and Os != "Windows":
        Prg["Errors"].append("Not supported Os detected: {:s}".format(Os))
        if Os == "Darwin": 
            Prg["Warnings"].append("Theoretically DeepCopy can run on Mac if the necessary external commands are available, TODO in the future")
    


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

