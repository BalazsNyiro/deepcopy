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



import os, sys

sys.path.append("src/p0_base")
import prg_general_config_and_state
prg = prg_general_config_and_state.Prg()  # check python version


print("This script checks the available modules, to see if deepcopy can work or not")

try:
    print("pillow (PIL) is important to read images and create screenshots")
    from PIL import Image
    print(f"PIL import was successful")

except:
    print("""
          Python image library (PIL) is important to load images, deepcopy cannot run without this.
          PIL import was unsuccessful - please install pillow: 'pip install pillow'
          """)

print(f"multiprocessing is useful to speed up image recognition - deepcopy can work without this, but will be slow.")
print(f"module 'multiprocessing' is working on Linux/Win only, module 'multiprocess' works on Mac")

try:
    print(f"multiprocessing on Linux/Win... (https://stackoverflow.com/questions/61270799/python-multiprocessing-with-macos)")
    import multiprocessing
    print(f"multiprocessing import was successful")

except:
    print(f"Module multiprocessing is Not available")
    print(f"try to use multiprocess, typically in MacOs... (https://stackoverflow.com/questions/61270799/python-multiprocessing-with-macos)")
    print(f"multiprocess homepage: https://pypi.org/project/multiprocess/")

    try:
        import multiprocess
    except:
        print(f"Module multiprocess is Not available")

        print("Theoretically deepcopy can work without multiprocessing/multiprocess but radically slower")
        print("Practically we will see this part - if you have problems, install multiprocess: 'pip install multiprocess'")

