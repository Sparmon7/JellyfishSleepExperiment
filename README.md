# Jellyfish Sleep Experiment
## Experiment
This experiment, run by Mike Abrams and The Harland Lab at UC Berkeley, researches how the jellyfish nervous systems change between wake and sleep, particularly in response to sleep deprivation. The jellyfish nervous system consists of different neuron clusters called rhopalia. I was tasked with creating the algorithm to process hours of video data to determine both when the jellyfish contracts as well as which rhopalia initiates the contraction (since they are spread out along the circumference of the jellyfish). 
## The Program
### How it works
The program uses the OpenCV library to process an ordered series of 120 fps jellyfish videos. The program records each pulse by determining the difference between consecutive frames and a series of OpenCV image operations. The action is only considered a pulse if there is sufficient and localized movement on the jellyfish after having been stable for a minimum of 3 frames. The jellyfish is identified by using the HoughCircle operation. 
After a pulse has been identified, the program identifies the dark dye marks on the jellyfish using OpenCV image operations to track how much it has rotated.
To see an example, look at `video.mp4`, which is a jellyfish contraction slowed down 50x. The red dot indicates the rhopalia that first initiates the contraction, and the green lines indicate the 0 degree line and the angle of the dye marks.
An earlier version of a program with a similar intent took longer than the length of each video to run on the Berkeley supercluster, but this version takes roughly 1/3 the time of a video on a traditional laptop, enabling the researchers to process results much more efficiently.
### Output
The program outputs a csv file in the output folder containing data for each pulse including the frame (video frame and global frame), angle of pulse, angle of dye mark, adjusted angle of pulse relative to dye mark, center of jellyfish, radius of jellyfish, video number, and timestamp of when it occurred (using the video name and the elapsed time in the video). Additionally, this program stores the first 10 contractions with a red dot indicating where the contraction initiates as a sanity check for the code.
### How to run
Create an empty folder titled 'output' for the program to write the data. Additionally, fill a folder titled 'data'  with the videos to be analyzed. This program assumes that the videos are titled like `20210901_1300_SalmaHayek_Baseline_cam2vidnum01.mp4 ` with the date and time first and the numbered video last. This program will process all videos with that title in sequential order.

Run the following two lines in the command line:

`pip install -r requirements.txt`

`python main.py [firstVideoFileName] `


