#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: function unit test environment,

import os, sys
Prg = {"Os": "",
       "Errors": [],
       "Warnings": [],
       "PrgPathExec" : os.path.realpath(__file__),
       "PrgDirParent":  os.path.dirname( os.path.realpath(__file__) ),
       "UiLanguage": "eng",
       "UiMessages": "",
       "FilesDeleteLater": []
       }
sys.path.append(os.path.join(Prg["PrgDirParent"], "src"))
import util, test_all

test_all.run_all_tests(Prg)

util.ui_msg_init(Prg)
util.os_detect(Prg)
util.warning_display(Prg)
util.error_display(Prg)
