import json
import random
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageOps
ImageDraw.ImageDraw.font = ImageFont.truetype("times.ttf", 11.4)

#loading lists
interjections = json.load(open("interjections.json"))
adverbs = json.load(open("adverbs.json"))
verbs = json.load(open("verbs.json"))
adjectives = json.load(open("adjectives.json"))
pronouns = json.load(open("pronouns.json"))
contractions = json.load(open("contractions.json"))

#50% chance a word will start uppercase
def randomCase(text):
    if random.randrange(4) > 0:
        return text.capitalize()
    else:
        return text

#picks a random word from a list and gives it random case
def pick(list):
    return randomCase(random.choice(list))

#generates and prints random bro ball phrase
def generatePhrase():
    formula = random.randrange(10)
    match formula:
        case 0:
            return f"{pick(interjections)} Bro"
        case 1:
            return f"{pick(adverbs)} Bro"
        case 2:
            return f"{pick(verbs)} Bro"
        case 3:
            return f"{randomCase('i')}'m {pick(adjectives)} Bro"
        case 4:
            return f"{pick(contractions)} {randomCase('being')} {pick(adjectives)} Bro"
        case 5:
            return f"{pick(verbs)} {pick(pronouns)} Bro"
        case 6:
            return f"{pick(adverbs)} {pick(verbs)} {pick(pronouns)} Bro"
        case 7:
            return f"{pick(verbs)} {pick(adverbs)} Bro"
        case 8:
            return f"{pick(verbs)} {pick(pronouns)} {pick(adverbs)} Bro"
        case 9:
            return f"{pick(contractions)} {pick(adjectives)} Bro"
        case _:
            print("uh oh bro")

def randomColor():
    color = (random.choice(range(256)), random.choice(range(256)), random.choice(range(256)))
    return color

#generates bro ball image from phrase
def generateImage(phrase):
    print(phrase)
    style = random.randrange(2)+1
    base = f"bbBase{style}.jpg"
    bubble = f"sb{style}.png"
    with Image.open(base).convert("RGBA") as ball, Image.open(bubble) as speechBubble:
        #creates new image as base for text
        txt = Image.new("RGBA", ball.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(txt)
        #manages where to place text depending on length
        textCoord = (55, 17)
        if d.textlength(phrase) > 110:
            textCoord = (45, 17)
            words = phrase.split()
            print(phrase.split())
            newPhrase = ""
            for entry in words:
                temp = newPhrase + f" {entry}"
                if (d.textbbox((45,17), temp)[2] - d.textbbox((45,17), temp)[0]) > 85:
                    newPhrase += "\n"
                newPhrase += f" {entry}"
            phrase = newPhrase
        elif d.textlength(phrase) > 70:
            textCoord = (39, 33)
        #places text on new image and combines it onto the bb image
        d.text(textCoord, phrase, fill=(0, 0, 0, 255))
        bluredText = txt.filter(ImageFilter.GaussianBlur(.5/style))
        coloredBall = ImageOps.colorize(ball.convert("L"), randomColor(), "white")
        withBubble = Image.alpha_composite(coloredBall.convert("RGBA"), speechBubble)
        combine = Image.alpha_composite(withBubble, bluredText)
        out = combine.resize((1280, 1200))
        out.show()

generateImage(generatePhrase())