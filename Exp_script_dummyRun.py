"""
Conditions:
a) spatial frequency: -high and -low
a) grouping of G-elements and Target: -grouped and -ungrouped
a) target strength: -low and -high
    target strength refers to the range of the emotional strength (in terms of %)
that will be visible at the screen. 10-20 refers to 20% and 40% intensity range,
and 30-40 refers to 60% and 80% emotional intensity range.
    grouped will have 18 trials. 6 for each identity. In every trial identity will be
different at each faces (4 identities in total, will be used). Therefore, ungrouped
trials (which has 3 levels: AAA, FFF, AFH) will each have 6 trials, totalling 18 trials
again to match the grouped trials. 
    spatial frequency will be manipulated with 2 levels: low and high. 
Therefore, each observer will do 36x2 = 72 trials in one block. And they do 2 blocks
one for HPF and one for LPF. 
    If permitted, normal gray scale images can be added as an additional experiment. 
    I expect to see better facial expression identification performance when the target matches
with the G-elements (grouping elements), especially when the target strength is low. No apriori
hypothesis regarding the differences in performance in seeing HPF vs LPF images. 

Observers will see 4 faces and all will have different identity. 
Future: 
1- Somehow I need to manipulate the emotion of the faces individually withing a loop.
    a- need to extend the stim duration too. Right now it ties to frames, thus 50 frames. 
    But I can get them back to normal with longer times?
"""
from __future__ import division
from calendar import c  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui, monitors
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys
from random import choice, randrange, shuffle
from psychopy.tools.coordinatetools import pol2cart, cart2pol
import time
from psychopy.tools.filetools import fromFile, toFile
import psychopy.gui
import csv
import math
import re
import random
from pathlib import Path 
from string import ascii_letters, digits
import pylink
import platform
import random
import time
import sys
from psychopy.tools.monitorunittools import pix2deg, deg2pix
import pathlib

### FOR RAs:  ##############################

condID = 3 # 1 2 or 3
edf_fname = 'TEST'

#############################################

#display and experiment options
currentPath = "/Users/gorkem.er/Desktop/W23/"#os.getcwd()#"/Users/gorkem.er/Documents/GitHub/A22_exp"
print(currentPath)
print(os.getcwd())
globalClock = core.Clock()
refRate = 60 # 1 second
second = refRate
#stimDur = refRate * 12 # 12 seconds
stimDur = 150 # 1 round equals 4 seconds motion, inverting after 2 second
posX = 8
posY = 0
durInitialBlank = 24 * second
cond = "BB" # assigning default

#cond = "\BB" # \LPF \BB
dummy_mode = True
responses = []
keyList = []
freezeSide = []
response = None
FI = "B"

# Show only critical log message in the PsychoPy console
from psychopy import logging
logging.console.setLevel(logging.CRITICAL)

# Set this variable to True if you use the built-in retina screen as your
# primary display device on macOS. If have an external monitor, set this
# variable True if you choose to "Optimize for Built-in Retina Display"
# in the Displays preference settings.
use_retina = False
# Set this variable to True to run the script in "Dummy Mode"

# Set this variable to True to run the task in full screen mode
# It is easier to debug the script in non-fullscreen mode
full_screen = False
# Set up EDF data file name and local data folder
#
# The EDF data filename should not exceed 8 alphanumeric characters
# use ONLY number 0-9, letters, & _ (underscore) in the filename
# edf_fname = 'TEST'

# Prompt user to specify an EDF data filename
# before we open a fullscreen window
dlg_title = 'Enter EDF File Name'
dlg_prompt = 'Please enter a file name with 8 or fewer characters\n' + \
             '[letters, numbers, and underscore].'

# loop until we get a valid filename
while True:
    dlg = gui.Dlg(dlg_title)
    dlg.addText(dlg_prompt)
    dlg.addField('File Name:', edf_fname)
    dlg.addField('Condition ID:', condID)
    # show dialog and wait for OK or Cancel
    ok_data = dlg.show()
    if dlg.OK:  # if ok_data is not None
        print('EDF data filename: {}'.format(ok_data[0]))
    else:
        print('user cancelled')
        core.quit()
        sys.exit()

    # get the string entered by the experimenter
    tmp_str = dlg.data[0]
    # strip trailing characters, ignore the ".edf" extension
    edf_fname = tmp_str.rstrip().split('.')[0]
    # check if the filename is valid (length <= 8 & no special char)
    allowed_char = ascii_letters + digits + '_'
    if not all([c in allowed_char for c in edf_fname]):
        print('ERROR: Invalid EDF filename')
    elif len(edf_fname) > 8:
        print('ERROR: EDF filename should not exceed 8 characters')
    else:
        break

# assigning conditions based on the condID
if condID == 1:
    cond = "/HPF"
elif condID == 2:
    cond = "/LPF"
else:
    cond = "/BB"
    
if cond == "/HPF" or cond == "/BB":
    bgColor = (0.3,0.3,0.3)
    fgColor = (-1, -1, -1)
else: # elif cond == "\LPF":
    bgColor = "black"
    fgColor = (1, 1, 1)

# Set up a folder to store the EDF data files and the associated resources
# e.g., files defining the interest areas used in each trial
results_folder = 'W23'
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

# We download EDF data file from the EyeLink Host PC to the local hard
# drive at the end of each testing session, here we rename the EDF to
# include session start date/time
time_str = time.strftime("_%Y_%m_%d_%H_%M", time.localtime())
session_identifier = edf_fname + time_str

# create a folder for the current testing session in the "results" folder
session_folder = os.path.join(results_folder, session_identifier)
if not os.path.exists(session_folder):
    os.makedirs(session_folder)
# Step 1: Connect to the EyeLink Host PC
#
# The Host IP address, by default, is "100.1.1.1".
# the "el_tracker" objected created here can be accessed through the Pylink
# Set the Host PC address to "None" (without quotes) to run the script
# in "Dummy Mode"

# Step 2: Open an EDF data file on the Host PC
edf_file = edf_fname + ".EDF"


# Add a header text to the EDF file to identify the current experiment name
# This is OPTIONAL. If your text starts with "RECORDED BY " it will be
# available in DataViewer's Inspector window by clicking
# the EDF session node in the top panel and looking for the "Recorded By:"
# field in the bottom panel of the Inspector.
# preamble_text = 'RECORDED BY %s' % os.path.basename(__file__)

# Optional tracking parameters
# Sample rate, 250, 500, 1000, or 2000, check your tracker specification

# Open a window, be sure to specify monitor parameters
#mon = monitors.Monitor('myMonitor', width=53.0, distance=90.0)
mon = monitors.Monitor('testMonitor')#'eyeTrackerRoom_mon'
#mon.setSizePix=(1920,1080)
#for mon in monitors.getAllMonitors(mon).getSizePix():
#    print(mon, monitors.Monitor(mon).getSizePix())
#print(monitor.getAllMonitors())
win = visual.Window(fullscr=False,
                    monitor= mon,
                    size=[1920/1.7, 1080/1.3],
                    units='pix',
                    winType='pyglet',
                    color = bgColor)
                    
#win = visual.Window(fullscr=full_screen,
#                    monitor='eyeTrackerRoom_mon',
#                    winType='pyglet',
#                    units='pix')

print(win.size)

print(mon.getWidth())
print(mon.getSizePix())
# get the native screen resolution used by PsychoPy
scn_width, scn_height = win.size
# resolution fix for Mac retina displays


# Beeps to play during calibration, validation and drift correction
# parameters: target, good, error
#     target -- sound to play when target moves
#     good -- sound to play on successful operation
#     error -- sound to play on failure or interruption
# Each parameter could be ''--default sound, 'off'--no sound, or a wav file

def clear_screen(win):
    """ clear up the PsychoPy window"""
    win.flip()



def terminate_task():
    """ Terminate the task gracefully and retrieve the EDF data file

    file_to_retrieve: The EDF on the Host that we would like to download
    win: the current window used by the experimental script
    """


    if el_tracker.isConnected():
        # Terminate the current trial first if the task terminated prematurely
        error = el_tracker.isRecording()
        if error == pylink.TRIAL_OK:
            abort_trial()

        # Put tracker in Offline mode
        el_tracker.setOfflineMode()

        # Clear the Host PC screen and wait for 500 ms
        el_tracker.sendCommand('clear_screen 0')
        pylink.msecDelay(500)

        # Close the edf data file on the Host
        el_tracker.closeDataFile()

        # Show a file transfer message on the screen
        msg = 'EDF data is transferring from EyeLink Host PC...'
        show_msg(win, msg, wait_for_keypress=False)

        # Download the EDF data file from the Host PC to a local data folder
        # parameters: source_file_on_the_host, destination_file_on_local_drive
        local_edf = os.path.join(session_folder, session_identifier + '.EDF')
        try:
            el_tracker.receiveDataFile(edf_file, local_edf)
        except RuntimeError as error:
            print('ERROR:', error)

        # Close the link to the tracker.
        el_tracker.close()

    # close the PsychoPy window
    win.close()

    # quit PsychoPy
    core.quit()
    sys.exit()

def abort_trial():
    """Ends recording """

    el_tracker = pylink.getEYELINK()

    # Stop recording
    if el_tracker.isRecording():
        # add 100 ms to catch final trial events
        pylink.pumpDelay(100)
        el_tracker.stopRecording()

    # clear the screen
    clear_screen(win)
    # Send a message to clear the Data Viewer screen
    bgcolor_RGB = (116, 116, 116)
    el_tracker.sendMessage('!V CLEAR %d %d %d' % bgcolor_RGB)

    # send a message to mark trial end
    el_tracker.sendMessage('TRIAL_RESULT %d' % pylink.TRIAL_ERROR)

#win = visual.Window([1200, 800], units = 'deg', monitor = 'eyeTrackRoom_mon', colorSpace= 'rgb', color = bgColor, fullscr=False) 
#win.setRecordFrameIntervals(True) #(0.3,0.3,0.3)

#myRatingScale = visual.RatingScale(win, choices=['angry', 'neutral', 'happy'])
myRatingScale = visual.RatingScale(win, low=-8, high=8, precision=1, skipKeys=None,
        marker='circle',
        labels=["Very Angry", "Very Happy"])
# image handling
import glob # a module that allows you to access filenames from a folder

def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))

identity_dir = currentPath #"C:\Users\Public\Documents\EyeLink\SampleExperiments\Python\examples\Psychopy_examples\A22"
#"/Users/gorkem.er/Documents/GitHub/A22_exp"+"/"+cond
print("currentPath:", currentPath)
identity_dir = identity_dir + cond
filenames_identities = []

print(identity_dir)

file_pattern = re.compile(r'.*?(\d+).*?')
def get_order(file):
    match = file_pattern.match(Path(file).name)
    if not match:
        return math.inf
    return int(match.groups()[0])

for identities in listdir_nohidden(identity_dir):
    filenames = glob.glob(os.path.join(identities, '*.jpg')) #images
    sorted_files = sorted(filenames, key=get_order)
    #print(sorted_files)
    filenames_identities.append(sorted_files)

images = [] # need to start with an empty list

#stimuli initializing
fixation = visual.GratingStim(win, size=5, pos=[0,0], sf=0,color = 'red')

print(len(filenames_identities))
# create an image stimulus from each file, and store in the list:
for identity in filenames_identities:
    for file in identity:
        images.append(visual.ImageStim(win=win, image=file))


# segmenting based on identity
print(type(images))
iden_A = images[0:150]
iden_B = images[150:300]
iden_C = images[300:450]
iden_D = images[450:600]

# further segmenting based on emotion, F -> H -> A
print(type(images))
iden_A_F = iden_A[0:50]
iden_A_H = iden_A[50:100]
iden_A_A = iden_A[100:150]
iden_B_F = iden_B[0:50]
iden_B_H = iden_B[50:100]
iden_B_A = iden_B[100:150]
iden_C_F = iden_C[0:50]
iden_C_H = iden_C[50:100]
iden_C_A = iden_C[100:150]
iden_D_F = iden_D[0:50]
iden_D_H = iden_D[50:100]
iden_D_A = iden_D[100:150]

print("iden_A_F:",iden_A_F)
# calculating circle 45 degrees cartesian points (x0 + r cos theta, y0 + r sin theta)
displacement = 5
x0 = 0
y0 = 0
theta = 45
r = 6
#pi/4
# going counter clockwise
corners1 = [x0 + r*cos(pi/4), y0 + r *sin(pi/4)]
corners2 = [x0 + r*cos(3*pi/4), y0 + r *sin(3*pi/4)]
corners3 = [x0 + r*cos(5*pi/4), y0 + r *sin(5*pi/4)]
corners4 = [x0 + r*cos(7*pi/4), y0 + r *sin(7*pi/4)]

group_1 = [ round(deg2pix(x0 + r*cos(340*pi/180),mon),2), round(deg2pix(y0 + r *sin(340*pi/180),mon),2)] #[x0 + (r+1)*cos(pi/4), y0 + (r+1) *sin(pi/4)]
group_2 = [ round(deg2pix(x0 + r*cos(35*pi/180),mon),2), round(deg2pix(y0 + r *sin(35*pi/180),mon),2)] #[x0 + (r-r/2)*cos(pi/4), y0 + (r-3) *sin(pi/4)]
group_3 = [ round(deg2pix(x0 + r*cos(90*pi/180),mon),2), round(deg2pix(y0 + r *sin(90*pi/180),mon),2)] #[x0 + (r+2) *cos(pi/8), y0 + r *sin(pi/8)]
group_4 = [ round(deg2pix(x0 + r*cos(195*pi/180),mon),2), round(deg2pix(y0 + r *sin(195*pi/180),mon),2)]

#angry_people = [iden_A_A, iden_B_A, iden_C_A, iden_D_A]
#happy_people = [iden_A_H, iden_B_H, iden_C_H, iden_D_H]
fearful_people = [iden_A_F, iden_B_F, iden_C_F, iden_D_F]
target_emot_list = []

lowComd = range(5,25)
highCond = range(30,50)

# ilk index [0] target
trial_params = [
    # EMOTIONAL INCONGRUENT trial
    # 20
    [ [iden_D_H, iden_A_A, iden_B_A, iden_C_A], True, lowComd, "HAAA", True],
    [ [iden_A_H, iden_B_A, iden_C_A, iden_D_A], True, lowComd, "HAAA", False],
    [ [iden_B_H, iden_C_A, iden_D_A, iden_A_A], True, highCond, "HAAA", True],
    [ [iden_C_H, iden_D_A, iden_A_A, iden_B_A], True, highCond, "HAAA", False],
    [ [iden_D_H, iden_A_A, iden_B_A, iden_C_A], False, lowComd, "HAAA", True],
    [ [iden_A_H, iden_B_A, iden_C_A, iden_D_A], False, lowComd, "HAAA", False],
    [ [iden_B_H, iden_C_A, iden_D_A, iden_A_A], False, highCond, "HAAA", True],
    [ [iden_C_H, iden_D_A, iden_A_A, iden_B_A], False, highCond, "HAAA", False],
    #[ [iden_D_H, iden_A_A, iden_B_F, iden_C_H], True, lowComd, "HAAA", True], #
    #[ [iden_A_H, iden_B_A, iden_C_F, iden_D_H], True, lowComd, "HAAA", False], #
    #[ [iden_B_H, iden_C_A, iden_D_F, iden_A_H], True, highCond,"HAAA", True], #
    #[ [iden_C_H, iden_D_A, iden_A_F, iden_B_H], True, highCond,"HAAA", False], #
    #[ [iden_A_H, iden_D_A, iden_B_F, iden_C_H], True, lowComd, "HAAA", True], #
    #[ [iden_D_H, iden_B_A, iden_C_F, iden_A_H], True, lowComd, "HAAA", False], #
    #[ [iden_B_H, iden_C_A, iden_D_F, iden_A_H], True, highCond,"HAAA", True], #
    #[ [iden_C_H, iden_D_A, iden_A_F, iden_B_H], True, highCond,"HAAA", False], #
    [ [iden_B_H, iden_A_A, iden_D_A, iden_C_A], True, lowComd, "HAAA", True],
    [ [iden_A_H, iden_B_A, iden_C_A, iden_D_A], True, lowComd, "HAAA", False],
    [ [iden_D_H, iden_C_A, iden_B_A, iden_A_A], True, highCond, "HAAA", True],
    [ [iden_C_H, iden_D_A, iden_A_A, iden_B_A], True, highCond, "HAAA", False],
    # 20 
    [ [iden_D_H, iden_A_F, iden_B_F, iden_C_F], True, lowComd, "HFFF", True],
    [ [iden_A_H, iden_B_F, iden_C_F, iden_D_F], True, lowComd, "HFFF", False],
    [ [iden_B_H, iden_C_F, iden_D_F, iden_A_F], True, highCond, "HFFF", True],
    [ [iden_C_H, iden_D_F, iden_A_F, iden_B_F], True, highCond, "HFFF", False],
    [ [iden_D_H, iden_A_F, iden_B_F, iden_C_F], False, lowComd, "HFFF", True],
    [ [iden_A_H, iden_B_F, iden_C_F, iden_D_F], False, lowComd, "HFFF", False],
    [ [iden_B_H, iden_C_F, iden_D_F, iden_A_F], False, highCond, "HFFF", True],
    [ [iden_C_H, iden_D_F, iden_A_F, iden_B_F], False, highCond, "HFFF", False],
    #[ [iden_D_H, iden_A_A, iden_B_F, iden_C_H], False, lowComd, "HFFF", True], # 
    #[ [iden_A_H, iden_B_A, iden_C_F, iden_D_H], False, lowComd, "HFFF", False], #
    #[ [iden_B_H, iden_C_A, iden_D_F, iden_A_H], False, highCond, "HFFF", True], #
    #[ [iden_C_H, iden_D_A, iden_A_F, iden_B_H], False, highCond, "HFFF", False], #
    #[ [iden_B_H, iden_A_A, iden_D_F, iden_C_H], False, lowComd, "HFFF", True], #
    #[ [iden_A_H, iden_B_A, iden_C_F, iden_D_H], False, lowComd, "HFFF", False], #
    #[ [iden_D_H, iden_C_A, iden_B_F, iden_A_H], False, highCond, "HFFF", True], # 
    #[ [iden_C_H, iden_D_A, iden_A_F, iden_B_H], False, highCond, "HFFF", False], #
    [ [iden_D_H, iden_A_F, iden_B_F, iden_C_F], True, lowComd, "HFFF", True],
    [ [iden_C_H, iden_B_F, iden_A_F, iden_D_F], True, lowComd, "HFFF", False],
    [ [iden_B_H, iden_C_F, iden_D_F, iden_A_F], True, highCond, "HFFF", True],
    [ [iden_A_H, iden_D_F, iden_C_F, iden_B_F], True, highCond, "HFFF", False],
    # 20
    [ [iden_D_H, iden_A_H, iden_B_H, iden_C_H], True, lowComd, "HHHH", True],
    [ [iden_A_H, iden_B_H, iden_C_H, iden_D_H], True, lowComd, "HHHH", False],
    [ [iden_B_H, iden_C_H, iden_D_H, iden_A_H], True, highCond, "HHHH", True],
    [ [iden_C_H, iden_D_H, iden_A_H, iden_B_H], True, highCond, "HHHH", False],
    [ [iden_D_H, iden_A_H, iden_B_H, iden_C_H], False, lowComd, "HHHH", True],
    [ [iden_A_H, iden_B_H, iden_C_H, iden_D_H], False, lowComd, "HHHH", False],
    [ [iden_B_H, iden_C_H, iden_D_H, iden_A_H], False, highCond, "HHHH", True],
    [ [iden_C_H, iden_D_H, iden_A_H, iden_B_H], False, highCond, "HHHH", False],
    [ [iden_D_H, iden_A_H, iden_B_H, iden_C_H], True, lowComd, "HHHH", True],
    [ [iden_A_H, iden_B_H, iden_C_H, iden_D_H], True, lowComd, "HHHH", False],
    [ [iden_B_H, iden_C_H, iden_D_H, iden_A_H], True, highCond, "HHHH", True],
    [ [iden_C_H, iden_D_H, iden_A_H, iden_B_H], True, highCond, "HHHH", False],
    [ [iden_D_H, iden_A_H, iden_B_H, iden_C_H], True, lowComd, "HHHH", True],
    [ [iden_C_H, iden_B_H, iden_A_H, iden_D_H], True, lowComd, "HHHH", False],
    [ [iden_B_H, iden_C_H, iden_D_H, iden_A_H], True, highCond, "HHHH", True],
    [ [iden_A_H, iden_D_H, iden_C_H, iden_B_H], True, highCond, "HHHH", False],
    [ [iden_A_H, iden_D_H, iden_B_H, iden_C_H], True, lowComd, "HHHH", True],
    [ [iden_D_H, iden_B_H, iden_C_H, iden_A_H], True, lowComd, "HHHH", False],
    [ [iden_B_H, iden_C_H, iden_D_H, iden_A_H], True, highCond, "HHHH", True],
    [ [iden_C_H, iden_D_H, iden_A_H, iden_B_H], True, highCond, "HHHH", False],
    # happy - angry border
    # EMOTIONAL INCONGRUENT TRIALS
    # 20
    [ [iden_D_A, iden_A_H, iden_B_H, iden_C_H], True, lowComd, "AHHH", True],
    [ [iden_A_A, iden_B_H, iden_C_H, iden_D_H], True, lowComd, "AHHH", False],
    [ [iden_B_A, iden_C_H, iden_D_H, iden_A_H], True, highCond, "AHHH", True],
    [ [iden_C_A, iden_D_H, iden_A_H, iden_B_H], True, highCond, "AHHH", False],
    [ [iden_D_A, iden_A_H, iden_B_H, iden_C_H], False, lowComd, "AHHH", True],
    [ [iden_A_A, iden_B_H, iden_C_H, iden_D_H], False, lowComd, "AHHH", False],
    [ [iden_B_A, iden_C_H, iden_D_H, iden_A_H], False, highCond, "AHHH", True],
    [ [iden_C_A, iden_D_H, iden_A_H, iden_B_H], False, highCond, "AHHH", False],
    #[ [iden_D_A, iden_A_A, iden_B_F, iden_C_H], True, lowComd, "AHHH", True], #
    #[ [iden_A_A, iden_B_A, iden_C_F, iden_D_H], True, lowComd, "AHHH", False], #
    #[ [iden_B_A, iden_C_A, iden_D_F, iden_A_H], True, highCond, "AHHH", True], #
    #[ [iden_C_A, iden_D_A, iden_A_F, iden_B_H], True, highCond, "AHHH", False], #
    #[ [iden_D_A, iden_A_A, iden_B_F, iden_C_H], True, lowComd, "AHHH", True], #
    #[ [iden_A_A, iden_B_A, iden_C_F, iden_D_H], True, lowComd, "AHHH", False], #
    #[ [iden_B_A, iden_C_A, iden_D_F, iden_A_H], True, highCond, "AHHH", True], #
    #[ [iden_C_A, iden_D_A, iden_A_F, iden_B_H], True, highCond, "AHHH", False], #
    [ [iden_B_A, iden_A_H, iden_D_H, iden_C_H], True, lowComd, "AHHH", True],
    [ [iden_A_A, iden_B_H, iden_C_H, iden_D_H], True, lowComd, "AHHH", False],
    [ [iden_D_A, iden_C_H, iden_B_H, iden_A_H], True, highCond, "AHHH", True],
    [ [iden_C_A, iden_D_H, iden_A_H, iden_B_H], True, highCond, "AHHH", False],
    # 20
    [ [iden_D_A, iden_A_F, iden_B_F, iden_C_F], True, lowComd, "AFFF", True],
    [ [iden_A_A, iden_B_F, iden_C_F, iden_D_F], True, lowComd, "AFFF", False],
    [ [iden_B_A, iden_C_F, iden_D_F, iden_A_F], True, highCond, "AFFF", True],
    [ [iden_C_A, iden_D_F, iden_A_F, iden_B_F], True, highCond, "AFFF", False],
    [ [iden_D_A, iden_A_F, iden_B_F, iden_C_F], False, lowComd, "AFFF", True],
    [ [iden_A_A, iden_B_F, iden_C_F, iden_D_F], False, lowComd, "AFFF", False],
    [ [iden_B_A, iden_C_F, iden_D_F, iden_A_F], False, highCond, "AFFF", True],
    [ [iden_C_A, iden_D_F, iden_A_F, iden_B_F], False, highCond, "AFFF", False],
    #[ [iden_D_A, iden_A_A, iden_B_F, iden_C_H], False, lowComd, "AFFF", True], #
    #[ [iden_A_A, iden_B_A, iden_C_F, iden_D_H], False, lowComd, "AFFF", False], #
    #[ [iden_B_A, iden_C_A, iden_D_F, iden_A_H], False, highCond, "AFFF", True], #
    #[ [iden_C_A, iden_D_A, iden_A_F, iden_B_H], False, highCond, "AFFF", False], #
    #[ [iden_C_A, iden_A_A, iden_B_F, iden_D_H], False, lowComd, "AFFF", True], #
    #[ [iden_A_A, iden_B_A, iden_C_F, iden_D_H], False, lowComd, "AFFF", False], #
    #[ [iden_B_A, iden_C_A, iden_D_F, iden_A_H], False, highCond, "AFFF", True], #
    #[ [iden_D_A, iden_C_A, iden_A_F, iden_B_H], False, highCond, "AFFF", False], #
    [ [iden_C_A, iden_A_F, iden_B_F, iden_D_F], True, lowComd, "AFFF", True],
    [ [iden_A_A, iden_B_F, iden_C_F, iden_D_F], True, lowComd, "AFFF", False],
    [ [iden_B_A, iden_C_F, iden_D_F, iden_A_F], True, highCond, "AFFF", True],
    [ [iden_D_A, iden_C_F, iden_A_F, iden_B_F], True, highCond, "AFFF", False],
    # 20
    [ [iden_D_A, iden_A_A, iden_B_A, iden_C_A], True, lowComd, "AAAA", True],
    [ [iden_A_A, iden_B_A, iden_C_A, iden_D_A], True, lowComd, "AAAA", False],
    [ [iden_B_A, iden_C_A, iden_D_A, iden_A_A], True, highCond, "AAAA", True],
    [ [iden_C_A, iden_D_A, iden_A_A, iden_B_A], True, highCond, "AAAA", False],
    [ [iden_D_A, iden_A_A, iden_B_A, iden_C_A], False, lowComd, "AAAA", True],
    [ [iden_A_A, iden_B_A, iden_C_A, iden_D_A], False, lowComd, "AAAA", False],
    [ [iden_B_A, iden_C_A, iden_D_A, iden_A_A], False, highCond, "AAAA", True],
    [ [iden_C_A, iden_D_A, iden_A_A, iden_B_A], False, highCond, "AAAA", False],
    [ [iden_D_A, iden_A_A, iden_B_A, iden_C_A], True, lowComd, "AAAA", True],
    [ [iden_A_A, iden_B_A, iden_C_A, iden_D_A], True, lowComd, "AAAA", False],
    [ [iden_B_A, iden_C_A, iden_D_A, iden_A_A], True, highCond, "AAAA", True],
    [ [iden_C_A, iden_D_A, iden_A_A, iden_B_A], True, highCond, "AAAA", False],
    [ [iden_D_A, iden_A_A, iden_B_A, iden_C_A], True, lowComd, "AAAA", True],
    [ [iden_B_A, iden_A_A, iden_C_A, iden_D_A], True, lowComd, "AAAA", False],
    [ [iden_A_A, iden_C_A, iden_D_A, iden_B_A], True, highCond, "AAAA", True],
    [ [iden_C_A, iden_D_A, iden_A_A, iden_B_A], True, highCond, "AAAA", False],
    [ [iden_D_A, iden_A_A, iden_B_A, iden_C_A], True, lowComd, "AAAA", True],
    [ [iden_B_A, iden_A_A, iden_C_A, iden_D_A], True, lowComd, "AAAA", False],
    [ [iden_A_A, iden_C_A, iden_D_A, iden_B_A], True, highCond, "AAAA", True],
    [ [iden_C_A, iden_D_A, iden_A_A, iden_B_A], True, highCond, "AAAA", False],
]

print("trialN" , len(trial_params))

def run_trial(trial_pars, trial_index):
    """ Helper function specifying the events that will occur in a single trial

    trial_pars - a list containing trial parameters, e.g.,
                ['mask', 'img_1.jpg']
    trial_index - record the order of trial presentation in the task
    """
        # unpacking the trial parameters
    stimSet, targetSolo, targetVisibleWinSet, stimOrg, soloBottom = trial_pars
    print("stimSet:", stimSet)
    #myRatingScale.noResponse = True
    #myRatingScale.markerStart = random.randint(1,10)
    t0 = time.time()

    #assigning stim stuff on each trial
    stim1 = stimSet[0]
    print("stim1:", stim1)
    stim2 = stimSet[1]
    print("stim2:", stim2)
    stim3 = stimSet[2]
    print("stim3:", stim3)
    stim4 = stimSet[3]
    print("stim4:", stim4)

    if soloBottom:
        sign = 1
    else:
        sign = -1
    
    possibleLocations =  [group_2, group_3, group_4]
    random.shuffle(possibleLocations)
    if targetSolo:
        targetLoc = np.array([group_1]) * sign  + random.randint(-20,20)
    else:
        targetLoc = possibleLocations.pop()
        targetLoc = np.array([targetLoc]) * sign + random.randint(-20,20) 
        possibleLocations.append(group_1)
    random.shuffle(possibleLocations)
    # here I save the locations info before I apply the jittering
    #
    possibleLocations = np.array(possibleLocations) * sign
    possibleLocations[0] = possibleLocations[0] + random.randint(-20,20)
    possibleLocations[1] = possibleLocations[1] + random.randint(-20,20)
    possibleLocations[2] = possibleLocations[2] + random.randint(-20,20)
    
    print(targetVisibleWinSet)
    print("possibleLocations:", possibleLocations)

    up = bool(random.getrandbits(1))

    
    # OPTIONAL: draw landmarks and texts on the Host screen
    # In addition to backdrop image, You may draw simples on the Host PC to use
    # as landmarks. For illustration purpose, here we draw some texts and a box
    # For a list of supported draw commands, see the "COMMANDS.INI" file on the
    # Host PC (under /elcl/exe)
    left = int(scn_width/2.0) - 60
    top = int(scn_height/2.0) - 60
    right = int(scn_width/2.0) + 60
    bottom = int(scn_height/2.0) + 60

    # show the image, and log a message to mark the onset of the image
    clear_screen(win)
    win.flip()
    
    # Send a message to clear the Data Viewer screen, get it ready for
    # drawing the pictures during visualization
    bgcolor_RGB = (116, 116, 116)

    # show the image for 5-secs or until the SPACEBAR is pressed
    # move the window to follow the gaze
    event.clearEvents()  # clear cached PsychoPy events
    
    fixation.draw()
    win.flip()
    core.wait(1) #1 second wait-time after a response
    #posPix = posToPix(gabor)
        
    frame_num = 0  # keep track of the frames displayed
    
    for frames in range(0, 50): # 4 seconds at each round
        print("targetLoc:", stim1)
        stim1[frames].pos = targetLoc[0]
        if frames in targetVisibleWinSet and up:
            stim1[frames].draw()
        frame_num += 1
        flip_time = core.getTime()
        if frame_num == 1:
            # send a message to mark movement onset
            # pursuit start time
            movement_start = flip_time
        stim2[frames].pos = possibleLocations[0]
        stim2[frames].draw()

        stim3[frames].pos = possibleLocations[1]
        stim3[frames].draw()

        stim4[frames].pos = possibleLocations[2]
        stim4[frames].draw()
        
        fixation.draw()
        win.flip()
        #### FRAME LOOP ####
    for frames in reversed(range(0, 50)): # 4 seconds at each round

        stim1[frames].pos = targetLoc[0]
        if frames in targetVisibleWinSet and not up:
            stim1[frames].draw()
        stim2[frames].pos = possibleLocations[0]
        stim2[frames].draw()
        stim3[frames].pos = possibleLocations[1]
        stim3[frames].draw()
        stim4[frames].pos = possibleLocations[2]
        stim4[frames].draw()
        fixation.draw()
        win.flip()

    #registering responses
    fixation.draw()
    win.flip()
    
    ''' keyboard press handling while loop'''
    #rt_clock.reset() # reset the time after the stimulus was shown
    myRatingScale.noResponse = False
    while myRatingScale.noResponse:  # show & update until a response has been made
        #myItem.draw()
        myRatingScale.draw()
        win.flip()
        if event.getKeys(keyList=['escape', 'q']): # listen for a escape or q press, it will run after the above left-right press is progressed.

            terminate_task()
            return pylink.ABORT_EXPT
            win.close()
            core.quit()
            
    rating = myRatingScale.getRating()  # SAVE AND LOG


    
    fixation.draw()
    win.flip() #need to flip back again to show a gray screen
    # mart 16 23, toplanti icin core.wait ekliyorum
    core.wait(1.5)
    # clear the screen
    clear_screen(win)

# skip this step if running the script in Dummy Mode

        
#runExperimentLoop()
# randomize the trial list
random.shuffle(trial_params)
#random.shuffle(test_list)

# construct a list of 4 trials
#test_list = gorki[:]*1

trial_params2 = [
    # EMOTIONAL INCONGRUENT trial
    [ [iden_D_H, iden_A_A, iden_B_A, iden_C_A], True, lowComd, "HAAA", True]
    ]

trial_index = 1
for trial_pars in trial_params: #for trial_pars in test_list:
    myRatingScale = visual.RatingScale(win, low=-8, high=8, precision=1,
        marker='circle',
        labels=["Very Angry", "Very Happy"], showValue = True, acceptSize = 1, size = 0.8, scale = None, mouseOnly = False)
    myRatingScale.markerStart = random.randint(1,10)
    run_trial(trial_pars, trial_index)
    trial_index += 1

# Create (but not yet display) some text:
#msg1 = visual.TextBox2(win, 
#    text=u"What expression was shown the most (including both blocks)", 
#    font="Open Sans", letterHeight=0.1,
#    pos=(0, 0.2)) 
#    
#msg2 = visual.TextStim(win, "The experiment has ended! Last question: When thinking about both of the blocks, what expression was shown the most? Please press 'A' key (on keyboard) for 'Angry', 'H' for 'Happy' and 'N' for 'Not sure'. Thank you!", color = 'red',height=25)
#
#
#msg2.draw()
#
#win.flip()

keys = event.waitKeys()
for key in keys:
    print(key)


# Step 7: disconnect, download the EDF file, then terminate the task
terminate_task()

win.close()
core.quit()
