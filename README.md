# video2pdfGUI

# Warning
At the moment, this fork is still under development.
The script in its base functionalities is working, though the UI is 
not optimized and suffers freezes. It does the tasks, however.
Just leave it working in background, and wait until it finish.
Currently working on Windows 10, for other OS, it needs to be tested.

# Description
This is a fork of the original project 'video2pdfslided', by kaushik jeyaraman.
This fork purpose is to add a GUI and a ready to use Python environment, to make the program usable by non programmers.
The core script purpose is to extract pics from a video, and merge them into a single pdf file.
All the credits for the core logic goes to former creator, kaushik jeyaraman

# Setup
As of today, Python3 must be installed on target machines.
Install all required packages with:

pip install -r requirements.txt


# Steps to run the code
python guivideo2pdf.py

it will capture screenshots of unique frames and save it output folder...once screenshots are captured the program asks the user to manually verify the screenshots and delete any duplicate images.
Once this is done, hit 'MERGE' button and the program creates a pdf out of the screenshots.

# Example
There are two sample video avilable in "./input", you can test the code using these input by running
<li>python video2pdfslides.py "./input/Test Video 1.mp4" (4 unique slide)
<li>python video2pdfslides.py "./input/Test Video 2.mp4" (19 unique slide)


# More
The default parameters works for a typical video presentation. But if the video presentation has lots of animations, the default parametrs won't give a good results, you may notice duplicate/missing slides. Don't worry, you can make it work for any video presentation, even the ones with animations, you just need to fine tune and figure out the right set of parametrs, The 3 most important parameters that I would recommend to get play around is "MIN_PERCENT", "MAX_PERCENT", "FGBG_HISTORY". The description of these variables can be found in code comments.



# Developer contact info
kaushik jeyaraman: kaushikjjj@gmail.com
