from tkinter import * 
import cv2 
import Compiled

def loadImage(data):
    #Retreives path from textbox widget
    path = data.pathEntry.get() 
    data.gifPath = path + ".gif" 
    data.pngPath = path + ".png"
    data.loadImage = PhotoImage(file=data.gifPath)
    data.firstLoad = True 
    data.loadResized = False

def readNotes(data):
    data.firstRead = True 
    if not(data.firstRun):  
        image = cv2.imread(data.pngPath, cv2.IMREAD_COLOR)
        data.notesList = Compiled.staffConversion(image, Compiled.staffLocate(image), 64)
        print("Notes: ", data.notesList)

def playNotes(data):
    if not(data.firstRun):         
        Compiled.playNotes(data.notesList, data.playSpeed, data.pathVar)

def resizeLoadedImage(data): 
    #Dynamically resizes the image using .subsample() function
    scaleX = 1
    scaleY = 1
    while data.loadImage.width() > data.width: 
        data.loadImage = data.loadImage.subsample(scaleX,1)
        scaleX+=1 
    while data.loadImage.height() > (data.height - data.height//6):
        data.loadImage = data.loadImage.subsample(1,scaleY)
        scaleY+=1

def changeAccidental(data):
    #Updates instrument:
    instrument = data.instrumentDropdownContents.get()
    if instrument == "Piano": data.pathVar = "Wav"
    elif instrument == "Trumpet": data.pathVar = "Wav1"

    #Updates the piece speed: 
    speed = data.speedDropdownContents.get()
    if speed == "30 bpm": data.playSpeed = .5
    elif speed == "60 bpm": data.playSpeed = 1.0
    elif speed == "90 bpm": data.playSpeed = 1.5
    elif speed == "120 bpm": data.playSpeed = 2
    elif speed == "150 bpm": data.playSpeed = 2.5

    #Updates the accidental display: 
    def stringAccidentals(data): 
        returnString  = ""
        for accidental in data.currentSharps: 
            if len(returnString)==0: returnString = accidental
            else: returnString = returnString + ", " + accidental
        return returnString

    # Calling widget text variable:
    note = data.noteDropdownContents.get() 
    if note == "-": 
        data.currentSharps.clear()
        data.clearingLabel = Label(data.rightBar, text= "                           ")
        data.clearingLabel.grid(row=1, column=1)
        return None

    data.loopList = dict()

    # Stores accidental note in a dictionary of normal notes: dict[old note] = new note
    if note == "C♯": 
        if "Cs" in data.currentSharps: 
            data.loopList["Cs"] = "C"
            data.currentSharps.remove('Cs')
        else: 
            data.loopList["C"] = "Cs"
            data.currentSharps.add('Cs')
    elif note == "E♭": 
        if "Eb" in data.currentSharps: 
            data.loopList["Eb"] = "E"
            data.currentSharps.remove('Eb')
        else: 
            data.loopList["E"] = "Eb"
            data.currentSharps.add('Eb')
    elif note == "F♯": 
        if "Fs" in data.currentSharps: 
            data.loopList["Fs"] = "F"
            data.currentSharps.remove('Fs')
        else: 
            data.loopList["F"] = "Fs"
            data.currentSharps.add('Fs')
    elif note == "G♯": 
        if "Gs" in data.currentSharps: 
            data.loopList["Gs"] = "G"
            data.currentSharps.remove('Gs')
        else: 
            data.loopList["G"] = "Gs"
            data.currentSharps.add('Gs')
    elif note == "B♭": 
        if "Bb" in data.currentSharps: 
            data.loopList["Bb"] = "B"
            data.currentSharps.remove('Bb')
        else: 
            data.loopList["B"] = "Bb"
            data.currentSharps.add('Bb')
    elif note == "C2♯": 
        if "C2s" in data.currentSharps: 
            data.loopList["C2s"] = "C2"
            data.currentSharps.remove('C2s')
        else: 
            data.loopList["C2"] = "C2s"
            data.currentSharps.add('C2s')
    elif note == "E2♭": 
        if "E2b" in data.currentSharps: 
            data.loopList["E2b"] = "E2"
            data.currentSharps.remove('E2b')
        else: 
            data.loopList["E2"] = "E2b"
            data.currentSharps.add('E2b')
    elif note == "F2♯": 
        if "F2s" in data.currentSharps: 
            data.loopList["F2s"] = "F2"
            data.currentSharps.remove('F2s')
        else: 
            data.loopList["F2"] = "F2s"
            data.currentSharps.add('F2s')

    #Loops through current notes, checks for necessary updates 
    for i in range(len(data.notesList)): 
        for key in data.loopList: 
            if key == data.notesList[i][0]:
                data.notesList[i] = (data.loopList[key], data.notesList[i][1], data.notesList[i][2])

    data.clearingLabel = Label(data.rightBar, text= "                           ")
    data.clearingLabel.grid(row=1, column=1)
    data.notesListLabel = Label(data.rightBar, text = str(stringAccidentals(data)), fg="DarkGoldenrod1")
    data.notesListLabel.grid(row=1, column=1)
    print("\nUpdated: ", data.notesList)

def init(data, root):
    data.pngPath = ""
    data.gifPath = ""
    data.firstRun = True 
    data.firstLoad = False 
    data.firstRead = False 
    data.loadImage = None 
    data.loadResized = False 
    data.mode = "loadScreen"
    data.time = 0
    data.Qnote = PhotoImage(file='Qnote.gif')
    data.smallQnote = data.Qnote.subsample(3,3)
    data.Qstripes = PhotoImage(file='Stripes.gif').subsample(2,3)
    data.startOffset = 600
    data.currentSharps = set()
    data.playSpeed = 1.0
    data.pathVar = "Wav"


    # Note: Using .grid() and .pack() interchangeably will result in the program crashing
    # I had to edit the start code to make sure it was compatible with the .grid function

    #Window
    data.frame = Frame(root)
    data.frame.grid()

    #TopLeft Toolbar, row = 0, col = 0
    data.topBar = Frame(data.frame)
    data.topBar.grid(row=0, column=0)
    data.pyLabel = Label(data.topBar, text = "~ PyMusic      ", fg = "purple")
    data.pyLabel.grid(row=0, column=0)
    data.quitButton = Button(data.topBar, text = "Quit PyMusic", command = data.frame.quit)
    data.quitButton.grid(row=0, column=1)
    data.topBlankLabel = Label(data.topBar, text = "                       ") 
    data.topBlankLabel.grid(row=0, column=2)
    
    data.imgLabel = Label(data.topBar, text = "     Enter an image path:")
    data.pathEntry = Entry(data.topBar, background="white")
    data.goButton = Button(data.topBar, text = "Go", bg = "navy", command = lambda: loadImage(data))
    data.extLabel = Label(data.topBar, text = "*Use no file extension!*")

    data.blankLabel = Label(data.topBar, text="")
    data.readLabel = Label(data.topBar, text="Load the music feature:")
    data.playLabel = Label(data.topBar, text = "                              Play:")
    data.readButton = Button(data.topBar, text = "Read in the Notes", command = lambda: readNotes(data))
    data.playButton = Button(data.topBar, text = "Play!", command = lambda: playNotes(data))

    #Middle gap between toolbars, row = 0, col = 1
    data.gapBar = Frame(data.frame)
    data.gapBar.grid(row=0, column=1)

    #TopRight Toolbar, row = 0, col = 2
    data.rightBar = Frame(data.frame)
    data.rightBar.grid(row=0, column=2)
    data.settingsLabel = Label(data.rightBar, text = "Edit your settings here:", fg = "black")
    
    #Dropdown menu
    data.notesListLabel = Label(data.rightBar, text = "")
    data.noteDropdownContents = StringVar(data.rightBar)
    data.noteDropdownContents.set("♯Accidentals♭")
    data.noteDropdown = OptionMenu(data.rightBar, data.noteDropdownContents, "-", "C♯", "E♭", "F♯","G♯","B♭","C2♯","E2♭","F2♯") 
    data.speedDropdownContents = StringVar(data.rightBar)
    data.speedDropdownContents.set("60 bpm")
    data.speedDropdown = OptionMenu(data.rightBar, data.speedDropdownContents, "30 bpm", "60 bpm", "90 bpm", "120 bpm", "150 bpm")
    data.instrumentDropdownContents = StringVar(data.rightBar)
    data.instrumentDropdownContents.set("Piano")
    data.instrumentDropdown = OptionMenu(data.rightBar, data.instrumentDropdownContents, "Piano", "Trumpet")
    data.goDropdown = Button(data.rightBar, text="Update!", command = lambda: changeAccidental(data))
    data.accidentalSet = set()

####################################
# Dispatcher: 
####################################

def mousePressed(event, data):
    if data.mode == "loadScreen": startMP(event, data)
    elif data.mode == "main": mainMP(event, data)

def keyPressed(event, data):
    if data.mode == "loadScreen": pass
    elif data.mode == "main": mainKP(event, data)

def timerFired(data):
    if data.mode == "loadScreen": startTF(data)
    elif data.mode == "main": mainTF(data)    

def redrawAll(canvas, data):
    if data.mode == "loadScreen": startRA(canvas, data)
    elif data.mode == "main": mainRA(canvas, data)

# Load Screen:
####################################

def startMP(event, data):
    if 0 <= event.x <= data.width and 0 <= event.y <= data.height: data.mode="main"

def startTF(data):
    if data.startOffset != 0: data.startOffset -= 30

def startRA(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "white") #powder blue
    canvas.create_text(data.width//2, data.height//2, text = "~PyMusic", 
                        fill="darkBlue",
                        font="Avenir 60",
                        anchor = S) 
    canvas.create_text(data.width//2, data.height//2, text = "Click anywhere to immerse yourself", 
                        fill="black",
                        font="Avenir 28",
                        anchor = W) 
    canvas.create_image(data.width//3, data.height//2, image=data.Qnote)
    canvas.create_image(data.width*113//160+data.startOffset, data.height*7//13, image=data.Qstripes)

# Main Screen:
####################################

def mainMP(event, data):
    pass
def mainKP(event, data):
    pass
def mainTF(data): 
    pass

def mainRA(canvas, data): 
    canvas.create_image(data.width//10, data.height//10, image=data.smallQnote)
    canvas.create_text(data.width//8.5, data.height//7.5, text="~PyMusic", 
                        fill="purple",
                        font="avenir 25 bold italic",
                        anchor = W) 
    canvas.create_rectangle(data.width//12, data.height//6, data.width*11//12, data.height//6, fill = "black", outline="navy", width=3)
    #All initialized widgets are added to the root window
    if data.firstRun:
        data.firstRun = False 

        data.blankLabel.grid(row=1, column=0) 
        data.imgLabel.grid(row=2, column=0)
        data.pathEntry.grid(row=2, column=1)
        data.goButton.grid(row=3, column=1)
        data.extLabel.grid(row=3, column=0)

        #Setting and storing widget contents
        data.entryContents = StringVar()
        data.entryContents.set("Samples/Happy Birthday")
        data.pathEntry["textvariable"] = data.entryContents

    elif data.loadImage != None: 
        if not(data.loadResized): 
            resizeLoadedImage(data) 
            data.loadResized = True 
        canvas.create_text(data.width//2, data.height//7, text="Your Music:", 
                        fill="black",
                        font="Avenir 25") 
        canvas.create_image(data.width//2, data.height//6 + (data.height-data.height//6)//2, image=data.loadImage)
        if data.firstLoad: 
            data.firstLoad = False
            data.readLabel.grid(row=4, column=0)
            data.playLabel.grid(row=5, column=0)
            data.readButton.grid(row=4, column=1)
            data.playButton.grid(row=5, column=1)
        elif data.firstRead: 
            data.firstRead = False
            data.settingsLabel.grid(row=0, column=0)
            data.noteDropdown.grid(row=1, column=0)
            data.speedDropdown.grid(row=2, column=0)
            data.instrumentDropdown.grid(row=3, column=0)
            data.goDropdown.grid(row=4, column=0)
        
            '''
            #Altrnate way to bind (not functional programming):
                pathEntry.bind('<Key-Return>', print(data.contents))
            '''

####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data, root)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.grid()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app

    root.mainloop()  # blocks until window is closed
    print("Esketit!")

run(1100, 700)





'''
root = Tk()

topFrame = Frame(root)
topFrame.grid()
#topFrame.pack()


label = Label(root, text = "Name:", bg = "red")
label.grid(row=0, sticky=E)
#label.pack(fill = X)

#Button = Button(root, text = "runFunc", command = runFunc)
#Button.bind("<Button-1>", runFunc )

#button1 = Button(topFrame, text = "Button!", fg = "green", bg = "white")
#button1.pack(side=LEFT, fill = X) #Goes as far left as possible in the frame
#button1.grid(row=1, column=0)

#entry1 = Entry(root)
#entry1.pack()

#c = Checkbutton(root, text = "Keep me logged in")
#c.grid(columnspan = 2)
root.mainloop() 

######

if note == "C♯" accidental = "C"
elif note == "E♭": accidental = "E"
elif note == "F♯": accidental = "F"
elif note == "G♯": accidental = "G"
elif note == "B♭": accidental = "B"
elif note == "C2♯": accidental = "C2"
elif note == "E2♭": accidental = "E2"
elif note == "F2♯": accidental = "F2"
'''
