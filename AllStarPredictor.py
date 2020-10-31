import csv
import numpy as np
from bs4 import BeautifulSoup
import requests


def normalize(max, min, val):
    return(val-min)/(max-min)

def sigmoid(input):
    denominator = (np.exp(-1*input)) + 1
    return 1/denominator


def predict(features, weights, bias):
    array = np.dot(weights, features)
    predictions = sigmoid(array + bias)
    return predictions


headerSufficies = ["a/", "b/", "c/", "d/", "e/", "f/", "g/", "h/", "i/", "j", "k/", "l/", "m/", "n/", "o/", "p/", "q/", "r/", "s/", "t/", "u/", "v/", "w/", "x/", "y/", "z/"]
PlayerListHeader = "https://www.basketball-reference.com/players/"
PlayerPageHeader = "https://www.basketball-reference.com/"
weightList = [3.1161244403970856, 1.251908745531215, 2.313347979881822, 1.3330372371624548, 1.887172013386962, 0.9510200528299977]
bias = -4.885694714153023
maxVals = [27.2, 9.3, 13.2, 2.8, 2.5, .68]
minVals = [0,0,0,0,0,.35]

print("Welcome to the Allstar Predictor. We will predict your player's all star future based on their sophomore year stats ")
player = input("What is the name of the player you want to predict?")

nameList = player.lower().split()
firstName = nameList[0]
lastName = nameList[1]
namesPage = requests.get(PlayerListHeader + lastName[0] + "/")
website = BeautifulSoup(namesPage.content, "html.parser")
table =  website.find("table").get_text()
print(table)
#do a binary search
"""
for i in statCategories:
    question = "How many " + i + " per game did " + name + " average during his sophomore season?   "
    stat = float(input(question))
    playerStats.append(stat)
#normalize and calc ts%
trueShooting = playerStats[0]/(playerStats[6] + (.44 * playerStats[5]))
trueShooting /= 2
playerStats[5] = trueShooting
playerStats.pop(6)
normalizedStats = [normalize(maxVals[i],minVals[i], playerStats[i]) for i in range(len(maxVals))]
probability = predict(normalizedStats, weightList, bias)
yesOrNo = "No"
probabilityStatement = "very unlikely"
if probability >= .7:
    yesOrNo = "yes"
    probabilityStatement = "extremely likely"
elif probability >= .45:
    yesOrNo = "yes"
    probabilityStatement = "likely"
elif probability >= .4:
    probabilityStatement = "somewhat likely/possible"
elif probability >= .25:
    probabilityStatement = "unlikely"
probability *= 100
int(probability)

print("Probability = ", str(probability), "\nit is ", probabilityStatement, " for " + name + " to be an all star")
print("Our yes or no answer: " , yesOrNo)
print("\n\n\n\n\n\nThanks to Basketball Reference for the stats")
"""































