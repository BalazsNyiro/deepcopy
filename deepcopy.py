#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, importlib, argparse

DirPrgParent = os.path.dirname(os.path.realpath(__file__))
Prg = {"Os": "",
       "UiLanguage": "eng",
       "UiMessages": "",
       "UiInterface": "ui_tkinter",
       "UiThumbnailSize": (256, 256),
       "UiTextSelectPreviewSize": (1024, 768),
       "DirPrgParent":  DirPrgParent,
       "DirTmpPath": os.path.join(DirPrgParent, "tmp"),
       "DirsDeleteAfterRun": list(),
       "FilesDeleteAfterRun": list(),
       "DirDefaultFileSelectPath": os.path.abspath(__file__),
       "PathPrgExec" : os.path.realpath(__file__),
       "Color": {"TextSelectFrame": (255, 0, 0)},

       "ImagesLoaded": dict(),
       "ImageIdSelected": "",

       "TestResults": []
       }

sys.path.append(os.path.join(Prg["DirPrgParent"], "src"))
import util, util_test, test_mark_collect, test_mark_util, test_area, test_spiral, test_path

util.dir_create_if_necessary(Prg["DirTmpPath"])

util.ui_msg_init(Prg)
util.installed_environment_detect()
util.os_detect(Prg)

parser = argparse.ArgumentParser(prog="DeepCopy", description="Character recognition")
parser.add_argument("--testonly", help="execute only tests", action='store_true')
args = parser.parse_args()

SysArgvOrig = sys.argv
sys.argv = sys.argv[:1] # the testing environment gives a warning when I use a prg param so I hide it, temporary solution

# test_mark_collect.run_all_tests(Prg)
# test_mark_util.run_all_tests(Prg)
# test_area.run_all_tests(Prg)
# test_spiral.run_all_tests(Prg)
test_path.run_all_tests(Prg)
util_test.result_all(Prg)

if args.testonly:
       sys.exit(0)


UiInterface = importlib.import_module(Prg["UiInterface"])
UiInterface.window_main(Prg)

print("test only: ./deepcopy.py testonly")
# TODO: clean temporary dir after execute
