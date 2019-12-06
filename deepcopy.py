#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, importlib

Prg = {"Os": "",
       "Errors": [],
       "Warnings": [],
       "PrgPathExec" : os.path.realpath(__file__),
       "PrgDirParent":  os.path.dirname( os.path.realpath(__file__) ),
       "UiLanguage": "eng",
       "UiMessages": "",
       "UiInterface": "ui_tkinter",
       "FilesDeleteLater": [],
       "PathDefaultFileSelectDir": os.path.abspath(__file__)
       }
sys.path.append(os.path.join(Prg["PrgDirParent"], "src"))
import util, test_all

util.installed_environment_detect(Prg)
test_all.run_all_tests(Prg)

util.ui_msg_init(Prg)
util.os_detect(Prg)

UiInterface = importlib.import_module(Prg["UiInterface"])
UiInterface.window_main(Prg)

util.warning_display(Prg)
util.error_display(Prg)
