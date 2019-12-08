#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, importlib, tempfile

Prg = {"Os": "",
       "Errors": [],
       "Warnings": [],
       "UiLanguage": "eng",
       "UiMessages": "",
       "UiInterface": "ui_tkinter",

       "DirPrgParent":  os.path.dirname( os.path.realpath(__file__) ),
       "DirsDeleteAfterRun": [],
       "FilesDeleteAfterRun": [],
       "PathDefaultFileSelectDir": os.path.abspath(__file__),
       "PathPrgExec" : os.path.realpath(__file__),
       }
with tempfile.TemporaryDirectory() as TmpDirName:
       Prg["PathTempDir"] = TmpDirName
       Prg["DirsDeleteAfterRun"].append(TmpDirName)
       print("Tempdir:", TmpDirName)

sys.path.append(os.path.join(Prg["DirPrgParent"], "src"))
import util, test_all

util.ui_msg_init(Prg)
util.installed_environment_detect(Prg)
util.os_detect(Prg)

test_all.run_all_tests(Prg)
UiInterface = importlib.import_module(Prg["UiInterface"])
UiInterface.window_main(Prg)

util.warning_display(Prg)
util.error_display(Prg)
