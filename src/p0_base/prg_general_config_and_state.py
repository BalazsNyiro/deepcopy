#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2025 Balazs Nyiro
# All rights reserved.

# This source code (all file in this repo)
# is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Please read the complete LICENSE file
# in the root directory of this source tree.

import platform, json, os, importlib, gzip, datetime
import typing


class Prg:
    """Prg represent a general, program wide state where the global configurations and generally used
    data structures are stored.

    This can be problematic for testing purposes, because probably a lot of information will be collected here,
    and how can you know what is important for a function?



    To know what is stored here and why, the data inserting and reading is centralized and the history is saved to know the source of an info

    """


    # history saving is important to see the source of changes in Prg,
    # for testing reasons. Changes in Prg has to be followed and checked.
    historySaveSkipForTheseKeywords: set[str] = set()
    # logging, callstack, or other special elements where the history would kill the performance

    logFile = f"log_deepcopy_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt"

    def __init__(self):
        self.initErrors = []
        self.initWarnings = []

        self.data = dict()
        self.history: dict[str, list[dict[str, str]]] = dict()

        # In Python 3.9 and later, __file__ always stores an absolute path,
        # the root is 3 levels above this file.
        self.data["deepcopy_dir_root"] = os.path.dirname(   # root level
            os.path.dirname(                                # src
                os.path.dirname(                            # p0_base
                    os.path.abspath(__file__))))


        ################################################
        Major, Minor = [int(Num) for Num in platform.python_version().split(".")[0:2]]

        msgVersionMin = "3.12.3"
        if Major < 3:
            self.initErrors.append(f"Too low version: Please use deepcopy with minimum Python {msgVersionMin}")

        if Major >= 3 and Minor < 12:
            self.initWarnings.append(f"Tested with Python {msgVersionMin}, maybe it works with older versions.")

        self.set("python_interpreter_version_major", Major, "prg_init")
        self.set("python_interpreter_version_minor", Minor, "prg_init")

        ################################################



        ################################################
        osName = platform.system()
        self.set("operation_system", osName, "prg_init")
        if osName != "Linux" and osName != "Windows":
            self.initWarnings.append(f"Not supported Os detected: {osName}")
            if osName == "Darwin":
                self.initWarnings.append("Theoretically DeepCopy can run on Mac, but the author needs a Mac to test the program.")




    ######### save Prg history changes to follow
    def set(self, keyword: str, val: typing.Any, whoUpdated: str, whyUpdated: str="setValueFirstTime"):
        """set wanted keyword and history"""

        self.data[keyword] = val
        self.history.setdefault(keyword, list())

        recordWhatHappened = {"valueUpdated": str(val), "whoUpdated": whoUpdated, "whyUpdated": whyUpdated}
        self.history[keyword].append(recordWhatHappened)




    def get_history(self, keyword: str) -> tuple[list[dict[str, str]], list[str]]:
        errors: list[str] = []
        historyOfKeyword: list[dict[str, str]] = []
        if keyword not in self.history:
            errors.append(f"wanted keyword ({keyword}) is unknown in history")
        else:
            historyOfKeyword = self.history[keyword]

        return historyOfKeyword, errors

    def get(self, keyword: str):
        """read wanted keyword from data
        don't use default value if the val is not defined.
        Decision: every value has to be defined, and not set automatically.
        """

        errors = []
        value = ""

        if keyword in self.data:
            value = self.data[keyword]
        else:
            errors.append(f"unknown keyword in Prg.data: {keyword}")

        return value, errors