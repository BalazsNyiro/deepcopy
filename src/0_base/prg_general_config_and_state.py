#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform, json, os, importlib, gzip


class Prg:
    """Prg represent a general, program wide state where the global configurations and generally used
    data structures are stored.

    This can be problematic for testing purposes, because probably a lot of information will be collected here,
    and how can you know what is important for a function?



    To know what is stored here and why, the data inserting and reading is centralized and the history is saved to know the source of an info

    """


    # history saving is important to see the source of changes in Prg,
    # for testing reasons. Changes in Prg has to be followed and checked.
    historySaveSkipForTheseKeywords = set()
    # logging, callstack, or other special elements where the history would kill the performance



    def __init__(self):
        self.initErrors = []
        self.initWarnings = []

        self.data = dict()
        self.history = dict()

        # In Python 3.9 and later, __file__ always stores an absolute path,
        # the root is 3 levels above this file.
        self.data["deepcopy_dir_root"] = os.path.dirname(   # root level
            os.path.dirname(                                # src
                os.path.dirname(                            # 0_base
                    os.path.abspath(__file__))))


        ################################################
        Major, Minor = [int(Num) for Num in platform.python_version().split(".")[0:2]]

        msgVersionMin = "3.12.3!"
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
            self.initWarnings.append("Not supported Os detected: {:s}".format(osName), "util:os_detect")
            if osName == "Darwin":
                self.initWarnings.append("Theoretically DeepCopy can run on Mac, but the author needs a Mac to test the program.")




    ######### save Prg history changes to follow
    def set(self, keyword: str, val: any, whoUpdated: str, whyUpdated: str="setValueFirstTime"):
        """set wanted keyword and history"""

        self.data[keyword] = val
        self.history.setdefault(keyword, list())

        recordWhatHappened = {"valueUpdated": val, "whoUpdated": whoUpdated, "whyUpdated": whyUpdated}
        self.history[keyword].append(recordWhatHappened)




    def get_history(self, keyword: str):
        errors = []
        history = []
        if keyword not in self.history:
            errors.append(f"wanted keyword ({keyword}) is unknown in history")
        else:
            history = self.history.get(keyword)

        return history, errors

    def get(self, keyword: str):
        """read wanted keyword from data
        don't use default value if the val is not defined.
        Decision: every value has to be defined, and not set automatically.
        """

        errors = []
        value = ""

        if keyword in self.data:
            value = self.data.get(keyword)
        else:
            errors.append(f"unknown keyword in Prg.data: {keyword}")

        return value, errors