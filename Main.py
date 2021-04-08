# MIT License

# Copyright (c) 2021 Matt Curtis

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

VERSION_INFO = "21.4.1" # Script version number [YEAR.MONTH.BUILDNUM]

"""
CURRENT KNOWN ISSUE(S):
- Audio normalizing causes a memory leak
- Song suggestions don't have a title
- Multiple instances of the webserver cannot run at the same time
"""

"""
UPCOMING FEATURE(S):
+ Console-based dashboard instead of huge log
+ First-Run detection with announcer telling you how to setup this software
+ Better-looking HTML with multiple pages and graphs
"""

# Import classes
from RadioHost import RadioHost # RadioHost itself, the main class
import os.path # Used for getting absolute path to file

# Determine main program directory
maindirectory = os.path.dirname(os.path.abspath(__file__)) # The absolute path to this file

if __name__ == '__main__':
    maininstance = RadioHost()

    # Check if program has started before. If not, run guided tutorial
    if os.path.exists(str(maindirectory) + "/Firstrun.txt"):
        # Start radio host
        maininstance.startradio("") # Specify string as argument here to set a custom location
    else:
        # Run guided tutorial
        # Equivalent of "touch" command to create a blank file
        with open(str(maindirectory) + "/Firstrun.txt", "a") as firstrun:
            firstrun.close()
        maininstance.starttutorial() # Run tutorial from main class