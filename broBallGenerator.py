import json
import random


#loading lists

interjections = json.load(open("interjections.json"))
adverbs = json.load(open("adverbs.json"))
verbs = json.load(open("verbs.json"))
adjectives = json.load(open("adjectives.json"))

print(random.choice(interjections) + " bro")

#def randomPhrase():
    