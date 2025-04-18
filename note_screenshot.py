# PIL 7.1.0 or higher
from PIL import ImageGrab

# Take a screenshot of the entire screen
screenshot = ImageGrab.grab()

# Save the screenshot to a file
screenshot.save('screenshot.png')



"""If you encounter issues, you might want to consider using pyscreenshot as a replacement for the Pillow ImageGrab module on Linux. pyscreenshot is a Python screenshot library that works on Linux, macOS, and Windows. It can be installed via pip and used as follows:

import pyscreenshot as ImageGrab

# Take a screenshot of the entire screen
screenshot = ImageGrab.grab()

# Save the screenshot to a file
screenshot.save('screenshot.png')"""




