# video2pdfGUI

#Warning
At the moment, this fork is still under development.
There are no differences with the original projects.

# Description
This is a fork of the original project 'video2pdfslided', by kaushik jeyaraman.
This fork purpose is to add a GUi and a ready to use Python environment, to make the program usable by non programmers.
All the credits for the core logic goes to former creator, kaushik jeyaraman

# Setup
pip install -r requirements.txt


# Steps to run the code
python video2pdfslides.py <video_path>

it will capture screenshots of unique frames and save it output folder...once screenshots are captured the program is paused and the user is asked to manually verify the screenshots and delete any duplicate images. Once this is done the program continues and creates a pdf out of the screenshots.

# Example
There are two sample video avilable in "./input", you can test the code using these input by running
<li>python video2pdfslides.py "./input/Test Video 1.mp4" (4 unique slide)
<li>python video2pdfslides.py "./input/Test Video 2.mp4" (19 unique slide)


# More
The default parameters works for a typical video presentation. But if the video presentation has lots of animations, the default parametrs won't give a good results, you may notice duplicate/missing slides. Don't worry, you can make it work for any video presentation, even the ones with animations, you just need to fine tune and figure out the right set of parametrs, The 3 most important parameters that I would recommend to get play around is "MIN_PERCENT", "MAX_PERCENT", "FGBG_HISTORY". The description of these variables can be found in code comments.



# Developer contact info
kaushik jeyaraman: kaushikjjj@gmail.com
