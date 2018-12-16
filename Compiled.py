import cv2
import numpy as np
import datetime
import Notes
import copy
from threading import Thread

################################################################
#This section for testing purposes


hbd = cv2.imread("Samples/Happy Birthday.png", cv2.IMREAD_COLOR)
timeSignatureOffset = 64

################################################################
whitePixel = '[255 255 255]'
blackPixel = '[0 0 0]'
timeSignatureOffset = 64 #Arbitrary number I came up with 

#Helper function
def isStaffLine(startRow, startCol, array):
    length = 0
    for col in range(startCol, len(array[startRow])):
        if str(array[startRow][col]) == whitePixel: 
            length = col 
            break
    return (length/len(array[0])) >= (.7)

#Returns list of staff line locations in the image
def staffLocate(image): 
    array = np.array(image) 
    staffCount = 5
    lineRange = 7
    staffFound = False 
    staffList = [] #List of (x, y) of the staff lines 
    
    #Algo for finding staff lines: 
    for col in range(len(array[0])):
        if staffFound: break
        for row in range(len(array)):
            if (str(array[row][col]) != whitePixel) and (isStaffLine(row, col, array)): 
                #Check if pixel stems all the way to the right, takes up more than 70% of the screen 
                if len(staffList) == 0:
                    staffFound = True  
                    staffList.append((col, row))
                else: 
                    if abs(staffList[-1][1] - row) > 2:
                        staffList.append((col, row))
    #Account for the indented first line 
    if len(staffList) > 5:
        staffDistance = staffList[5][1] - staffList[4][1]
        subImg = image[ :(staffList[0][1]-staffDistance//2) , : ] 
        cv2.imshow("", subImg)
        returnList = staffLocate(subImg)
        returnList.extend(staffList)
        return returnList
    else:
        return staffList

################################################################

#Recursively checks for eights notes using floodFill template 
def floodEighthCheck(x, y, image, epsilon):
    try:
        checkedPixelSet = set()
        checkedPixelSet = flood(x, y, image, checkedPixelSet)

        leftMostPixel = x 
        rightMostPixel = x

        for checkedTuple in checkedPixelSet: 
            if checkedTuple[0] < leftMostPixel: leftMostPixel = checkedTuple[0]
            elif checkedTuple[0] > rightMostPixel: rightMostPixel = checkedTuple[0]

        #Test for eighth note connection: 
        if x-leftMostPixel > 2*epsilon or rightMostPixel-x > 2*epsilon: 
            return .5
        return None 
    except: return None 

def flood(x, y, image, checkedPixelSet=None): 
    #Checking for bounds 
    #                    image.shape = height, width, channels 
    if ((y < 0) or (y >= image.shape[0]) or (x < 0) or (x >= image.shape[1])): return 
    pixelColor = str(image[y, x]) 
    #Checking if the move is legal
    if pixelColor == whitePixel: return
    elif (x,y) in checkedPixelSet: return 

    #Saves non-white note locations
    checkedPixelSet.add((x,y))

    #Recursively add all other pixels 
    flood(x-1, y, image, checkedPixelSet)
    flood(x+1, y, image, checkedPixelSet)
    flood(x, y-1, image, checkedPixelSet)
    flood(x, y+1, image, checkedPixelSet)

    return checkedPixelSet



#Returns the relevant note value
def noteValue(image, i, biggerImage, biggerOffset): 
    x, y, epsilon = i[0], i[1], i[2]
    eightNoteTest = floodEighthCheck(x, y+biggerOffset, biggerImage, epsilon)
    if eightNoteTest != None: 
        return eightNoteTest

    #Image with no staff lines passed in
    #openCV uses img[row, col] or [vertical-y, horiz-x]
    blackFound = False 
    whiteFound = False 
    darkColorThreshold = 100
    lightColorThreshold = 60
    #Loops horizontally over note 
    for col in range(i[0]-i[2]-1, i[0]+i[2]+2):
        imagePixel = str(image[i[1], col])
        #Parses pixel to make sure values are above a certain threshold
        rgbListWhite = [rgbVal for rgbVal in imagePixel[1:len(imagePixel)-1].split(" ") if int(float(rgbVal)) >= darkColorThreshold]
        rgbListDark = [rgbVal for rgbVal in imagePixel[1:len(imagePixel)-1].split(" ") if int(rgbVal) <= lightColorThreshold]
        if not(blackFound) and len(rgbListDark)==3:
            blackFound = True   
        elif blackFound and not(whiteFound) and len(rgbListWhite)==3: 
            whiteFound = True 
        if whiteFound and len(rgbListDark)==3: 
            return 2
    return 1

#Determines note values and returns an ordered list of notes
def staffConversion(image, staffList, timeSignatureOffset = 0):
    if len(staffList)>5:
        returnList = []
        startIndex = 0
        endIndex = 5
        for i in range(len(staffList)//5):
            returnList.extend(staffC(image, staffList[startIndex:endIndex], timeSignatureOffset if endIndex==5 else 35))
            startIndex+=5
            endIndex+=5
        return returnList
    else: return(staffC(image, staffList, timeSignatureOffset))


def staffC(image, staffList, timeSignatureOffset = 0):
    lineWidth = staffList[1][1] - staffList[0][1]
    preImg = image
    tempStaff = preImg[ staffList[0][1]-lineWidth:staffList[-1][1]+lineWidth, staffList[0][0]: ] 
    biggerStaff = preImg[ staffList[0][1]-4*lineWidth:staffList[-1][1]+4*lineWidth, staffList[0][0]: ] 
    #Contains tuple of [(Note, Duration, Special Parameter)]
    preReturnList = [] 
    returnList = []

    #Eliminating staff line pixels for easier note recognition
    for row in range(lineWidth, len(tempStaff), 1):  
        for col in range(len(tempStaff[0])):
            try: 
                if str(tempStaff[row-1, col]) == whitePixel and str(tempStaff[row+2, col]) == whitePixel: 
                    tempStaff[row, col] = [255,255,255]
                    tempStaff[row+1, col] = [255,255,255]
            except: pass

    grayStaff = cv2.cvtColor(tempStaff, cv2.COLOR_BGR2GRAY)

    #Use the Hough Circles intrinsic to find circles within the image 
    #In this case, the circles are the notes! 
    #And store this in a numpy array:
    circles = cv2.HoughCircles(grayStaff, cv2.HOUGH_GRADIENT, 1, 2.5*lineWidth,
              param1=30,
              param2=7,
              minRadius=(lineWidth-4),
              maxRadius=(lineWidth-1))
    circles = np.uint16(np.around(circles))

    #Use a set to make sure no notes are vertically stacked 
    xSet = set()

    #Since we're looking at a subimage of a larger image, use an offset for staff line locations: 
    imageOffset = (0 - staffList[0][1] + lineWidth) 
    halfStepOffset = lineWidth//2

    for i in circles[0,:]:
        if i[0] not in xSet and i[0]>timeSignatureOffset: 
            xSet.add(i[0])
            noteVal = noteValue(tempStaff, i, biggerStaff, 3*lineWidth)
            if 0 < i[1] < staffList[0][1] + imageOffset: 
                preReturnList.append(("G2", noteVal, i[0]))
                continue
            elif staffList[0][1] + imageOffset - halfStepOffset < i[1] < staffList[0][1] + imageOffset + halfStepOffset: 
                preReturnList.append(("F2", noteVal, i[0]))
                continue
            elif staffList[0][1] + imageOffset < i[1] < staffList[1][1] + imageOffset: 
                preReturnList.append(("E2", noteVal, i[0]))
                continue
            elif staffList[1][1] + imageOffset - halfStepOffset < i[1] < staffList[1][1] + imageOffset + halfStepOffset:
                preReturnList.append(("D2", noteVal, i[0]))
                continue
            elif staffList[1][1] + imageOffset < i[1] < staffList[2][1] + imageOffset: 
                preReturnList.append(("C2", noteVal, i[0]))
                continue
            elif staffList[2][1] + imageOffset - halfStepOffset < i[1] < staffList[2][1] + imageOffset + halfStepOffset:
                preReturnList.append(("B", noteVal, i[0]))
                continue
            elif staffList[2][1] + imageOffset < i[1] < staffList[3][1] + imageOffset: 
                preReturnList.append(("A", noteVal, i[0]))
                continue
            elif staffList[3][1] + imageOffset - halfStepOffset < i[1] < staffList[3][1] + imageOffset + halfStepOffset:
                preReturnList.append(("G", noteVal, i[0]))
                continue
            elif staffList[3][1] + imageOffset < i[1] < staffList[4][1] + imageOffset: 
                preReturnList.append(("F", noteVal, i[0]))
                continue
            elif staffList[4][1] + imageOffset - halfStepOffset < i[1] < staffList[4][1] + imageOffset + halfStepOffset:
                preReturnList.append(("E", noteVal, i[0]))
                continue
            elif staffList[4][1] + imageOffset < i[1] < len(grayStaff): 
                preReturnList.append(("D", noteVal, i[0]))
                continue
            else: 
                preReturnList.append(("UNKNOWN", noteVal, i[0]))
                continue
        else: pass

    #Make sure the list is ordered 
    #Credit for this awesome line of code goes to "cheeken" from stackoverflow: 
    #https://stackoverflow.com/questions/10695139/sort-a-list-of-tuples-by-2nd-item-integer-value
    returnList = sorted(preReturnList, key=lambda x: x[2])
    return returnList

################################################################

#Intakes a list of tuples of the [("Note", time value, and special char)]
def playNotes(inList, playSpeed, pathVar): 
    popList = copy.copy(inList)
    oldTime = datetime.datetime.utcnow()  
    previousDuration = popList[0][1]

    #Threading is used to ignore the extra whitespace at the end of .wav files
    #AND to make sure the piece plays in time
    while len(popList) > 0: 
        newTime = datetime.datetime.utcnow() 
        #Performs every note 'duration' 
        if (newTime - oldTime).total_seconds() >= previousDuration/playSpeed: 
            note = popList[0][0]
            duration = popList[0][1]
            if note == "C": 
                t = Thread(target = Notes.playC, args=(pathVar,))
                t.start() #Starting threading immediately every time allows for chords
            elif note == "Cs": 
                t = Thread(target = Notes.playCs, args=(pathVar,))
                t.start()
            elif note == "D": 
                t = Thread(target = Notes.playD, args=(pathVar,))
                t.start()
            elif note == "Eb": 
                t = Thread(target = Notes.playEb, args=(pathVar,))
                t.start()
            elif note == "E": 
                t = Thread(target = Notes.playE, args=(pathVar,))
                t.start()
            elif note == "F": 
                t = Thread(target = Notes.playF, args=(pathVar,))
                t.start()
            elif note == "Fs": 
                t = Thread(target = Notes.playFs, args=(pathVar,))
                t.start()
            elif note == "G": 
                t = Thread(target = Notes.playG, args=(pathVar,))
                t.start()
            elif note == "Gs": 
                t = Thread(target = Notes.playGs, args=(pathVar,))
                t.start()
            elif note == "A": 
                t = Thread(target = Notes.playA, args=(pathVar,))
                t.start()
            elif note == "Bb": 
                t = Thread(target = Notes.playBb, args=(pathVar,))
                t.start()
            elif note == "B": 
                t = Thread(target = Notes.playB, args=(pathVar,))
                t.start()
            elif note == "C2": 
                t = Thread(target = Notes.playC2, args=(pathVar,))
                t.start()
            elif note == "C2s": 
                t = Thread(target = Notes.playCs2, args=(pathVar,))
                t.start()
            elif note == "D2": 
                t = Thread(target = Notes.playD2, args=(pathVar,))
                t.start()
            elif note == "E2b": 
                t = Thread(target = Notes.playEb2, args=(pathVar,))
                t.start()
            elif note == "E2": 
                t = Thread(target = Notes.playE2, args=(pathVar,))
                t.start()
            elif note == "F2": 
                t = Thread(target = Notes.playF2, args=(pathVar,))
                t.start()
            elif note == "F2s": 
                t = Thread(target = Notes.playFs2, args=(pathVar,))
                t.start()
            elif note == "G2": 
                t = Thread(target = Notes.playG2, args=(pathVar,))
                t.start()
            oldTime = datetime.datetime.utcnow() 
            previousDuration = popList[0][1]
            popList.pop(0)

###############

# Twinkle twinkle little star: 
#playNotes([('C', 1, 74), ('C', 1, 74), ('G', 1, 74),('G', 1, 74),('A', 1, 102), ('A', 1, 146), ('G', 2, 188)])

#print(staffLocate(image))
'''
[(107, 164), (107, 170), (107, 176), (107, 182), (107, 188), 
(64, 260), (64, 266), (64, 272), (64, 278), (64, 284), 
(64, 356), (64, 362), (64, 368), (64, 374), (64, 380), 
(64, 452), (64, 458), (64, 464), (64, 470), (64, 476)]
'''
#print(staffConversion(hbd, staffLocate(hbd), timeSignatureOffset))


