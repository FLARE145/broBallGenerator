import json
import random
from PIL import Image

#load image
broBallPrime = Image.open("helloBro.jpg")
area1 = (52, 18, 105, 32)
area2 = (102, 88, 155, 102)
square = broBallPrime.crop(area1)
broBallPrime.paste(square, area2)
broBallPrime.show()


#loading lists
interjections = json.load(open("interjections.json"))
adverbs = json.load(open("adverbs.json"))
verbs = json.load(open("verbs.json"))
adjectives = json.load(open("adjectives.json"))
pronouns = json.load(open("pronouns.json"))
contractions = json.load(open("contractions.json"))

#50% chance a word will start uppercase
def randomCase(text):
    if random.randrange(2) > 0:
        return text.capitalize()
    else:
        return text

#picks a random word from a list and gives it random case
def pick(list):
    return randomCase(random.choice(list))

#generates and prints random bro ball phrase
def randomPhrase():
    formula = random.randrange(10)
    match formula:
        case 0:
            print(f"{pick(interjections)} Bro")
        case 1:
            print(f"{pick(adverbs)} Bro")
        case 2:
            print(f"{pick(verbs)} Bro")
        case 3:
            print(f"{randomCase('i')}'m {pick(adjectives)} Bro")
        case 4:
            print(f"{pick(contractions)} {randomCase('being')} {pick(adjectives)} Bro")
        case 5:
            print(f"{pick(verbs)} {pick(pronouns)} Bro")
        case 6:
            print(f"{pick(adverbs)} {pick(verbs)} {pick(pronouns)} Bro")
        case 7:
            print(f"{pick(verbs)} {pick(adverbs)} Bro")
        case 8:
            print(f"{pick(verbs)} {pick(pronouns)} {pick(adverbs)} Bro")
        case 9:
            print(f"{pick(contractions)} {pick(adjectives)} Bro")
        case _:
            print("uh oh bro")

randomPhrase()