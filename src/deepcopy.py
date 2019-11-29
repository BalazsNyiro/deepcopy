#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import util

Prg = { "Os": None,
        "Errors": [],
        "Warnings": [],
        "Language": "Eng"
}

util.os_detect(Prg)


util.warning_display(Prg)
util.error_display(Prg)
