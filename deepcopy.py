#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, importlib, tempfile

DirPrgParent = os.path.dirname(os.path.realpath(__file__))
Prg = {"Os": "",
       "Errors": [],
       "Warnings": [],
       "UiLanguage": "eng",
       "UiMessages": "",
       "UiInterface": "ui_tkinter",
       "UiThumbnailSize": (256, 256),
       "UiTextSelectPreviewSize": (1024, 768),
       "DirPrgParent":  DirPrgParent,
       "DirsDeleteAfterRun": [],
       "FilesDeleteAfterRun": [],
       "PathDefaultFileSelectDir": os.path.abspath(__file__),
       "PathPrgExec" : os.path.realpath(__file__),
       "PathTempDir": os.path.join(DirPrgParent, "tmp"),
       "Color": {"TextSelectFrame": (255, 0, 0)},

       "ImagesLoaded": {},
       "ImageIdSelected": ""

       }

sys.path.append(os.path.join(Prg["DirPrgParent"], "src"))
import util, test_all

util.dir_create_if_necessary(Prg, Prg["PathTempDir"])

util.ui_msg_init(Prg)
util.installed_environment_detect(Prg)
util.os_detect(Prg)

TestOnly = False
print(sys.argv)
if "testonly" in sys.argv:
       TestOnly = True
       sys.argv = sys.argv[:1] # the testing environment gives a warning when I use a prg param so I hide it, temporary solution
test_all.run_all_tests(Prg)
if TestOnly:
       sys.exit(0)


UiInterface = importlib.import_module(Prg["UiInterface"])
UiInterface.window_main(Prg)

util.warning_display(Prg)
util.error_display(Prg)

# TODO: clean temporary dir after execute
