# deepcopy
Python based OCR program with deep text structure analysing and style detecting

# Goal - read from screenshots
Read simple human texts (basic English/French/latin alphabet with numbers, and dot, questionmark, exclamation mark)

Nice to have: 
- translate words under mouse cursor (local dictionary builder, work with more dictionary)


Contact/Author: Balazs Nyiro, balazs.nyiro.ca@gmail.com

# How can you help
 - I need a Macintosh to test Deepcopy, so if you have an unused and can give that to me, that would be a help.

# INSTALL support
deepcopy_installed_correctly.py -> check available modules and print install hints.

# INSTALL
 - important python3 modules
   - python3-pil  
     - apt install python3-pil    (install with apt package manager)
     - pip install pillow         (install with pip)
   - multiprocessing (works on Linux/win)
   - multiprocess   (only Mac)    (pip install multiprocess)  pip install multiprocess
 
# INSTALL for development

Tools:
   - mypy         (pip install mypy)
   - coverage     (pip install coverage)

To validate with mypy: validate_mypy.sh
To validate coverage:  validate_coverage.sh

