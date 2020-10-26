from flask import Flask, render_template, url_for, request, redirect
import numpy as np
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def normalize(max, min, val):
    return(val-min)/(max-min)

def sigmoid(input):
    denominator = (np.exp(-1*input)) + 1
    return 1/denominator

def predict(features, weights, bias):
    array = np.dot(weights, features)
    predictions = sigmoid(array + bias)
    return predictions
def turnIntoString (val):
    plainText = val.find('a').get_text().lower().split()
    formattedName = plainText[1] + plainText[0]
    return formattedName

def binarySearch(start, end, value, sortedList):

    if(start <= end):  
        middle = (end+start)//2
        middleVal = turnIntoString(sortedList[middle])
        if value == middleVal:
            return middle
        if middleVal < value :
            return binarySearch(middle+1, end, value, sortedList)
        if middleVal > value:
            return binarySearch(start, middle-1,value, sortedList)
    else:
        return -1


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/player', methods = ['POST'])
def testName():
    player = request.form['name']
    PlayerListHeader = "https://www.basketball-reference.com/players/"
    PlayerPageHeader = "https://www.basketball-reference.com/"
    weightList = [3.1161244403970856, 1.251908745531215, 2.313347979881822, 1.3330372371624548, 1.887172013386962, 0.9510200528299977]
    bias = -4.885694714153023
    maxVals = [27.2, 9.3, 13.2, 2.8, 2.5, .68]
    minVals = [0,0,0,0,0,.35]
    playerStats = []

    nameList = player.lower().split()
    lastName = nameList[1]
    combinedName = lastName + nameList[0]  
    namesPage = requests.get(PlayerListHeader + lastName[0] + "/")
    website = BeautifulSoup(namesPage.content, "html.parser")
    table =  website.find("table")
    rows = table.find_all("tr")
    pos = binarySearch(0, len(rows), combinedName, rows)

    if pos != -1:
        correctRow = rows[pos]
        link = correctRow.find("a")
        playerWebpageRequest = requests.get(PlayerPageHeader + link["href"])
        playerWebpage = BeautifulSoup(playerWebpageRequest.content, "html.parser")
        playerTable = playerWebpage.find("table")
        row2  =  playerTable.findAll('tr')[2]

        if "Did Not Play" in row2.get_text() or int(row2.findAll(["th", "td"])[5].get_text()) <= 25:
            row2  =  playerTable.findAll('tr')[1]
        else:
            
            points = float(row2.findAll(["th","td"])[29].get_text())
            assists = float(row2.findAll(["th","td"])[24].get_text())
            rebounds = float(row2.findAll(["th","td"])[23].get_text())
            blocks = float(row2.findAll(["th","td"])[26].get_text())
            steals = float(row2.findAll(["th","td"])[25].get_text())
            trueShooting = float(row2.findAll(["th","td"])[9].get_text()) + (.44 * float(row2.findAll(["th","td"])[19].get_text()))
            trueShooting = points/ (2* trueShooting)
            playerStats.extend([points, assists, rebounds, blocks, steals, trueShooting])
            #values are hardcoded pls change
    else:
        return render_template("notFound.html")



    normalizedStats = [normalize(maxVals[i],minVals[i], playerStats[i]) for i in range(len(maxVals))]
    probability = predict(normalizedStats, weightList, bias)
    probabilityStatement = "very unlikely"
    if probability >= .7:
        probabilityStatement = "extremely likely"
    elif probability >= .45:
        yesOrNo = "yes, he will become an all star"
        probabilityStatement = "likely"
    elif probability >= .4:
        probabilityStatement = "somewhat likely/possible"
    elif probability >= .25:
        probabilityStatement = "unlikely"
    probability *= 100
    int(probability)
    
    return render_template("newPage.html", n = player, p = probability, pS = probabilityStatement)

if(__name__ == "__main__"):
    app.run(debug=True)
