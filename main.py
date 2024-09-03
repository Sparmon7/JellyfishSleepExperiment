#imports
import cv2
import numpy as np
import datetime
import matplotlib.pyplot as plt
import math
import sys
import csv
import os



#mask the difference of the 2 images to leave only the moving parts
def get_mask(frame1, frame2):
    frame_diff = cv2.subtract(frame2, frame1)
    frame_diff = cv2.medianBlur(frame_diff, 3)
    mask = cv2.adaptiveThreshold(frame_diff, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 11, 4)
    mask = cv2.medianBlur(mask, 3)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.array((29,29), dtype=np.uint8))
    _, mask = cv2.threshold(mask,127,255,cv2.THRESH_BINARY)
    return mask

#process the video
def extractFrames(video):
    currentFrame = 0 #iterator
    last = []  #stores grayscaled last frame
    numNotMoving= 0 #how many frames the jellyfish has been stable for
    frames = [] #stores last 15 frames
    movers = [] #stores list of previous movements for saving pulses
    movementCenters = [] #stores center of movement for saving pulses
    found = False #if jellyfish has moved yet
    numSaved = 0 #storing number of pulses saved. goes up to 10
    
    while True:
        #reading frame by frame
        ret, cur = video.read()
        if not ret:
            break
        frames.append(cur.copy())
        frames = frames[-15:].copy()
        cur = cv2.cvtColor(cur, cv2.COLOR_RGB2GRAY)
        
        if currentFrame!=0:
            mask = get_mask(cur, last)
            
            if np.sum(mask) > 30*255:#if sufficient moving consistent with a contraction
                if numNotMoving > 3:#if stationary for a while
                    places = list(zip(*np.where(mask == 255)))
                    xs = [i[0] for i in places]
                    ys = [i[1] for i in places]
                    
                    if np.std(xs) + np.std(ys) < 50: #checking that movement is localized
                        medX =np.median(xs)
                        medY = np.median(ys)
                        
                        #finding closest point to median that moved
                        minDist = 10000
                        center = -1
                        for i in places:
                            dist = np.sqrt((i[0]-medX)**2 + (i[1]-medY)**2)
                            if dist<minDist:
                                minDist = dist
                                center = i
                                
                        jellyCenter, jellyRadius = findJellyCircle(frames[-1])

                        dvert = jellyCenter[0] - center[0]
                        dhor = center[1] - jellyCenter[1]
                        
                        #ensuring movement came from jellyfish
                        if  jellyRadius**2 - 10000 <dhor **2 + dvert**2 < jellyRadius**2  + 10000:
                            
                            #finding angle of movement origin
                            angle = -1
                            if dvert == 0 and dhor < 0:
                                angle = 270.0
                            elif dvert == 0 and dhor > 0:
                                angle = 90.0
                            elif dvert <= 0 :
                                angle = 180 + math.atan(dhor/dvert)*180/math.pi
                            else:
                                angle = math.atan(dhor/dvert)*180/math.pi % 360
                            
                            #finidng orientation of jellyfish using dye marks
                            new = onlyJelly(frames[-1], jellyCenter, jellyRadius -10) 
                            theta = calculateAngle(new, jellyCenter, jellyRadius)
                            
                            delta = datetime.timedelta(seconds = vid.get(cv2.CAP_PROP_POS_MSEC)/1000)
                            
                            #writing data
                            write([currentFrame, totalFrame + currentFrame, str(round(angle,2)), str(round(theta,2)), str(round((angle - theta) %360 , 2)), jellyCenter[0], jellyCenter[1], jellyRadius, vidnum, totalTime + delta])
                            movers.append(currentFrame)
                            movementCenters.append(center)
                            found=True

                            numNotMoving = 0
                        else:
                            numNotMoving+=1
                    else:
                        numNotMoving+=1             
            else:
                numNotMoving+=1
            
            
    
            #saving pulse
            if found and numSaved < 10:
                if currentFrame == movers[-1] + 10:
                    try: #so doesn't save if directory already exists
                        os.mkdir(f"output/{filename}/pulse{numSaved+1}")
                        center = movementCenters[-1]
                        for j in range(1,16):
                            i=frames[j-1].copy()
                            for x in range(center[0]-3, center[0]+4):
                                for y in range(center[1]-3, center[1]+4):
                                    i[x, y]= [0,0,255]
                            cv2.imwrite(f"output/{filename}/pulse{numSaved+1}/frame{j}.jpg", i)   
                        numSaved+=1
                    except:
                        pass
             
        #iterate
        currentFrame+=1
        last = cur.copy()
    return currentFrame

#find the jellyfish center and radius
def findJellyCircle(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.medianBlur(img,71)
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
    param1=50,param2=30,minRadius=40,maxRadius=100)
    circles = np.uint16(np.around(circles))
    jellyCenter=[circles[0][0][1], circles[0][0][0]]
    radius = circles[0][0][2] + 5 #since may be uneven flap and want to include entire jellyfish
    return jellyCenter, radius
   
#write the data
def write(data):
    with open(f"output/{filename}/Results.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data) 

#remove everything else from the image other than the jellyfish
def onlyJelly(im, center, radius):
    mask = np.zeros_like(im)
    mask = cv2.circle(mask, (center[1], center[0]), radius, (255,255,255), -1)
    result = cv2.bitwise_and(im, mask)
    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    return result

#calculate angle
def calculateAngle(img, center, radius):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img = clahe.apply(img)
    _, img = cv2.threshold(img, 60, 255, cv2.THRESH_BINARY)
    img = cv2.medianBlur(img, 5)
    mask = np.zeros_like(img)
    mask = cv2.circle(mask, (center[1], center[0]), radius-10, 255, -1)
    img = cv2.bitwise_xor(img, mask)
    
    #finding all white spots indicating dye marks
    places = list(zip(*np.where(img == 255)))
    xs = [i[0] for i in places]
    ys = [i[1] for i in places]
    x = np.median(xs) 
    y= np.median(ys) 
    
    #finding angle of dye mark
    dvert = center[0]-x
    dhor = y-center[1]
    if dvert == 0 and dhor < 0:
        return 270.0
    elif dvert == 0 and dhor > 0:
        return 90.0
    elif dvert <= 0 :
        return 180 + math.atan(dhor/dvert)*180/math.pi
    else:
        return math.atan(dhor/dvert)*180/math.pi % 360



#starting program
print(datetime.datetime.now())  
filename, filetype = sys.argv[1].split(".")
filename = filename[:-2]

#writing output
totalTime = datetime.datetime.strptime(filename.split("_")[0] + filename.split("_")[1], "%Y%m%d%H%M")
os.mkdir(f"output/{filename}")
write(["Local Frame", "Total Frame", "Angle of Pulse", "Angle of Dye Mark", "Rotated Angle Pulse", "X", "Y", "Radius", "Video", "Timestamp"])

vidnum = 1
totalFrame = 0
exists = True
while exists: #iterating through all videos
    vid = None
    if vidnum<10:
        vid = cv2.VideoCapture("data/" + filename + "0" + str(vidnum) + "."+ filetype)
    else:
        vid = cv2.VideoCapture("data/" + filename + str(vidnum) + "."+ filetype)
        
    if vid.get(cv2.CAP_PROP_FRAME_COUNT) == 0: #no more videos
        break
    print(f"Starting video {vidnum}")                 
    frames = extractFrames(vid)
    
    totalFrame+=frames
    timeElapsed= vid.get(cv2.CAP_PROP_FRAME_COUNT)/vid.get(cv2.CAP_PROP_FPS)
    delta = datetime.timedelta(seconds = timeElapsed)
    totalTime+=delta
    vidnum+=1




    