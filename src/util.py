#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform, sys, json, os


# import language.py


def os_detect(Prg):
    Os = Prg["Os"] = platform.system() 
    print(ui_msg(Prg, "os_detect.detected").format(Os))
    if Os != "Linux" and Os != "Windows":
        Prg["Errors"].append("Not supported Os detected: {:s}".format(Os))
        if Os == "Darwin": 
            Prg["Warnings"].append("Theoretically DeepCopy can run on Mac if the necessary external commands are available, TODO in the future")
    
def ui_msg_init(Prg):
    Txt = file_read_all( os.path.join(Prg["PrgDirParent"], "resources", "ui_messages.json"))
    Prg["UiMessages"] = json.loads(Txt)
    print(Prg)

# MsgPath example: os_detect.detected
def ui_msg(Prg, MsgPath):
    Container = Prg["UiMessages"]
    for Key in MsgPath.split("."):
        if Key in Container:
            Container = Container[Key]
        else:
            Msg = "Ui message key is unknown: " + Prg["UiLanguage"] + " - " + MsgPath
            Prg["Errors"].append(Msg)
            return Msg

    # check: eng msg always has to be defined
    if "eng" not in Container:
        Msg = "Ui message, default eng translation is missing: " + MsgPath
        Prg["Errors"].append(Msg)
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
    if Prg["Errors"]: return

    if isinstance(Fname, list):
        Files = Fname
        Out = []
        for File in Files:
            Out.extend(file_read_lines(File, ErrMsgNoFile=ErrMsgNoFile, ErrExit=ErrExit, Strip=Strip)) 
        return Out

    if file_test(Fname):
        with open(Fname, 'r') as F:
            if Strip:
                return [L.strip() for L in f.readlines()]
            else:
                return f.readlines()

    elif ErrMsgNoFile:
        Prg["Errors"].append(ErrMsgNoFile)
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

