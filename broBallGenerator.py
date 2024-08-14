#!/usr/bin/env python3
import json
import random
import string
from tkinter import *
from tkinter import ttk, filedialog, colorchooser
from ttkthemes import ThemedTk
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageOps, ImageTk
import os, sys
from io import BytesIO
import copykitten

#for to compile exe
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)

ImageDraw.ImageDraw.font = ImageFont.truetype(resource_path("times.ttf"), 11.3)
#loading lists
interjections = json.load(open(resource_path("interjections.json")))
adverbs = json.load(open(resource_path("adverbs.json")))
verbs = json.load(open(resource_path("verbs.json")))
adjectives = json.load(open(resource_path("adjectives.json")))
pronouns = json.load(open(resource_path("pronouns.json")))
contractions = json.load(open(resource_path("contractions.json")))

# global chosenColor
# chosenColor = 0

#picks a random word from a list (this is for easy to read/ didnt want to update things)
def pick(list):
    return (random.choice(list))
    
#applies a pattern for uppercase letters
def caseStyle(sentence):
    match random.randrange(3):
        case 0:
            #first word uppercase
            return sentence.capitalize()
        case 1:
            #all words uppercase
            return string.capwords(sentence)
        case 2:
            #no words uppercase
            return sentence

#generates and prints random bro ball phrase
def generatePhrase():
    formula = random.choices(list(range(10)), weights=(60, 20, 30, 15, 8, 10, 2, 5, 3, 10), k = 1)[0]
    match formula:
        case 0:
            return f"{caseStyle(pick(interjections))} Bro"
        case 1:
            return f"{caseStyle(pick(adverbs))} Bro"
        case 2:
            return f"{caseStyle(pick(verbs))} Bro"
        case 3:
            return caseStyle(contractions[0] + " " + pick(adjectives)) + " Bro"
        case 4:
            return caseStyle(pick(contractions) + " being " + pick(adjectives) + " Bro")
        case 5:
            return caseStyle(pick(verbs) + " " + pick(pronouns) + " Bro")
        case 6:
            return caseStyle(pick(adverbs) + " " +pick(verbs) + " " + pick(pronouns) + " Bro")
        case 7:
            return caseStyle(pick(verbs) + " " + pick(adverbs) + " Bro")
        case 8:
            return caseStyle(pick(verbs) + " " + pick(pronouns) + " " + pick(adverbs) + " Bro")
        case 9:
            return caseStyle(pick(contractions) + " " + pick(adjectives) + " Bro")
        case _:
            print("uh oh bro")

#random rgb color but 50% chance it limits the higher values
def getColor():
    global chosenColor
    #print(chosenColor)
    if chosenColor == 0:
    # Random
        if random.randrange(2) == 1:
            newColor = random.randrange(200), random.randrange(200), random.randrange(200)
        else:
            newColor = random.randrange(256), random.randrange(256), random.randrange(256)
    else:
        newColor = chosenColor[0]

    print(newColor)
    return newColor

#generates bro ball image from phrase
def generateImage(phrase, usePhraseForSeed = True):
    print(phrase)
    style = random.randrange(2)+1
    base = resource_path("bbBase" + str(style) + ".jpg")
    bubble = resource_path("sb" + str(style) + ".png")
    with Image.open(base).convert("RGBA") as ball, Image.open(bubble) as speechBubble:
        randomAnchor = "la"
        txt = Image.new("RGBA", ball.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(txt)
        #manages where to place text depending on length
        textCoord = (55, 17)
        if d.textlength(phrase) > 110:
            textCoord = (45, 17)
            words = phrase.split()
            newPhrase = ""
            for entry in words:
                temp = newPhrase + f" {entry}"
                if (d.textbbox((45,17), temp)[2] - d.textbbox((45,17), temp)[0]) > 85:
                    newPhrase += "\n"
                newPhrase += f" {entry}"
            phrase = newPhrase
        elif d.textlength(phrase) > 76:
            textCoord = (39, 33)
        elif random.randrange(2) == 1:
            textCoord = (131, 17)
            randomAnchor = "ra"
        #sets seed for random color based on phrase
        if usePhraseForSeed:
            random.seed(phrase.lower())
        #putting it together
        d.text(textCoord, phrase, fill=(0, 0, 0, 255), anchor = randomAnchor)
        bluredText = txt.filter(ImageFilter.GaussianBlur(.5/style))

        global color
        color = getColor()
        coloredBall = ImageOps.colorize(ball.convert("L"), color, "white")
        withBubble = Image.alpha_composite(coloredBall.convert("RGBA"), speechBubble)
        out = Image.alpha_composite(withBubble, bluredText)

        #reset seed for next time
        random.seed()
        return out

#the rest of this is tkinter bs
root = ThemedTk(theme="keramik")

root.geometry("240x270")
root.resizable(False, False)
root.configure(background="gray80")
root.title("BBGen")
img = PhotoImage(file='bbIcon.png')
root.tk.call('wm', 'iconphoto', root._w, img)
#root.iconbitmap(resource_path("bbIcon.ico"))

ballPil = Image.open(resource_path("helloBro.jpg"))
ballImage = ImageTk.PhotoImage(ballPil)
currentPhrase = ''

imageHolder = Frame(root, bd = 5, relief = 'ridge', )
imageHolder.pack(pady = 5)

canvas = Canvas(imageHolder, width = 160, height = 150, borderwidth = 0, highlightthickness = 0)
canvas.pack()
item = canvas.create_image((0,0), image = ballImage, anchor = 'nw')

def updateImage(overridePhrase = "", usePhraseForSeed = True):
    global ballPil
    global ballImage
    global currentPhrase
    global color
    inputText = textArea.get("1.0",'end-1c')
    if inputText == "":
        currentPhrase = generatePhrase()
    else:
        currentPhrase = caseStyle(inputText) + " Bro"

    if overridePhrase != "":
        currentPhrase = overridePhrase

    root.title(currentPhrase)
    ballPil = generateImage(currentPhrase, usePhraseForSeed)
    ballImage = ImageTk.PhotoImage(ballPil)
    canvas.itemconfig(item, image = ballImage)
    saveButton.config(state = NORMAL)
    copyButton.config(state = NORMAL)

    #img = PhotoImage(file="bbIconGray.png")
    imgPath = resource_path("bbIconGray.png")
    img = Image.open(imgPath)

    r, g, b, a = img.split()
    gray = img.convert("L")

    #print(color)
    colorizedIcon = ImageOps.colorize(gray, color, "white" )
    colorizedIcon.putalpha(a)
    root.tk.call('wm', 'iconphoto', root._w, ImageTk.PhotoImage(colorizedIcon))

def saveImage():
    filePath = filedialog.asksaveasfile(mode='w', defaultextension=".jpg", filetypes=[("JPEG Image", "*.jpg")], initialfile = currentPhrase.lower().replace(" ", "-") + ".jpg")
    if filePath:
        ballPil.convert("RGB").save(filePath)

def copyImage():
    global ballPil
    copykitten.copy_image(ballPil.tobytes(), ballPil.width, ballPil.height)

def setColor():
    global chosenColor
    global currentPhrase

    chosenColor = colorchooser.askcolor(title = "Color me Bro")
    #print(chosenColor)

    updateImage(currentPhrase)
    chosenColor = 0 #this makes it work how i want


    return

def unsetColor():
    global chosenColor
    global currentPhrase

    random.seed(random.random())
    chosenColor = 0

    updateImage(currentPhrase, False)
    return

textArea = Text(root, height = 1, width = 25)
textArea.pack(pady = 0)
buttonFrame = Frame(root, bg = "gray80")
buttonFrame.pack(pady = 5)
ttk.Button(buttonFrame,text='Meet New Bro', takefocus = False, command = updateImage).pack(side='left', padx = (0, 5))

copyButton = ttk.Button(buttonFrame,text='Copy Bro', takefocus = False, command = copyImage, state = DISABLED)
copyButton.pack(side='right', padx = (5, 0))

buttonFrameBottomRow = Frame(root, bg = "gray80")
buttonFrameBottomRow.pack(pady = 2)

setColorButton = ttk.Button(buttonFrameBottomRow,text='Color Bro', takefocus = False, command = setColor)
setColorButton.pack(side='left', padx = (0, 5))

saveButton = ttk.Button(buttonFrameBottomRow,text='Keep Bro', takefocus = False, command = saveImage, state = DISABLED)
saveButton.pack(side='right', padx = (5, 0))

#unsetColorButton = ttk.Button(buttonFrameBottomRow,text='Randomly Color Bro', takefocus = False, command = unsetColor)
#unsetColorButton.pack(side='right', padx = (5,0))

chosenColor = 0
color = 0

root.mainloop()
