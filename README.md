# Jellyfish Sleep Experiment
## Experiment
This experiment, run by Mike Abrams and The Harland Lab at UC Berkeley, researches how the jellyfish nervous systems change between wake and sleep, particularly in response to sleep deprivation. The jellyfish nervous system consists of different neuron clusters called rhopalia. I was tasked with creating the algorithm to process hours of video data to determine both when the jellyfish contracts as well as which rhopalia initiates the contraction (since they are spread out along the circumference of the jellyfish). 
## The Program
### Output
The program uses the OpenCV library to process an ordered series of jellyfish videos and create a csv with data about each contraction, the angle on the jellyfish that initiates the contraction, the center and radius of the jellyfish, and the timestamp. Additionally, this program stores the first 10 contractions with a blue dot indicating where the contraction initiates as a sanity check for the code.
### How to run
Create an empty folder titled 'output' for the program to write the data. Additionally, fill the input folder with the videos to be analyzed. This program assumes that the videos are titled like `20210901_1300_SalmaHayek_Baseline_cam2vidnum01.mp4 ` with the datetime first and the numbered video last.

Run the following two lines in the command line:

` pip install -r requirements.txt`

`python main.py [firstVideoFileName] `


