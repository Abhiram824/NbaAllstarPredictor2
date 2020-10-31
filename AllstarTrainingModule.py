import csv
import numpy as np


def normalize(max, min, val):
    return(val-min)/(max-min)

def sigmoid(input):
    denominator = (np.exp(-1*input)) + 1
    return 1/denominator

def cost(weights, features, labels, bias):
    cost = 0
    predictedVals = predict(features, weights, bias)
    for i in range(len(labels)):
        cost+= ((labels[i]*np.log(predictedVals[i])) + (1-labels[i])*np.log(1 - predictedVals[i]))
    return (-cost)/len(labels)

def weightGradient(weights, features, labels, weightPos, bias):
    
    predictedVals = predict(features, weights, bias)
    
    gradient = 0
    for i in range(len(predictedVals)):
        gradient += features[weightPos][i] * (predictedVals[i] - labels[i])
    return gradient/len(predictedVals)

def Bgradient(weights, bias, features, labels):
    predictedVals = predict(features, weights, bias)
    gradientB = 0
    for i in range(len(labels)):
        gradientB += (predictedVals[i] - labels[i])
    return gradientB/len(labels)

def predict(features, weights, bias):
    array = np.dot(weights, features)
    predictions = [sigmoid(i + bias) for i in array]
    return predictions

def stats(labels, predictions):
    truePositives = 0
    trueNegatives = 0
    falsePositives = 0
    falseNegatives = 0
    for i in range(len(predictions)):
        if labels[i] == 1 and predictions[i] == 1:
            truePositives += 1

        if labels[i] == 0 and predictions[i] == 0:
            trueNegatives += 1

        if labels[i] == 0 and predictions[i] == 1:
            falsePositives += 1

        if labels[i] == 1 and predictions[i] == 0:
            falseNegatives += 1
    accuracy = (truePositives + trueNegatives)/ len(predictions)
    precision = truePositives/(truePositives + falsePositives)
    recall = truePositives/(truePositives + falseNegatives)
    return accuracy, recall, precision

def divide(ratio, dictionary, randomKey):
    limit = int (ratio * len(dictionary[randomKey]))
    trainingDataVals = []
    testDataVals = []
    for key in dictionary:
        keyList = list(dictionary[key])
        split1 = [keyList[i] for i in range(limit)]
        trainingDataVals.append(split1)
        split2 = [keyList[i] for i in range(limit, len(dictionary[randomKey]))]
        testDataVals.append(split2)
    return trainingDataVals, testDataVals


def gradient(weightList, learningRate, features, labels, bias): 
    for i in range(len(weightList)):
        weightList[i] -= weightGradient(weightList, features, labels,i, bias) * learningRate
    return weightList




maxVals = [27.2, 9.3, 13.2, 2.8, 2.5, .68]

with open("NBAdata.csv", "r") as file:
    fileReader = csv.reader(file)
    keys = ["Points", "Assists", "Rebounds", "Blocks", "Steals", "Percentage"]
    playerDictionary = {i: [] for i in keys}
    allStarList = []
    
    for row in fileReader:
        if row[0] == "Player Name":
            continue
        for i in range(1,len(row) - 1,1):
            if i == 6:
                normalVal = normalize(maxVals[i-1], .35, float(row[i]))
            else:
                normalVal = normalize(maxVals[i-1], 0, float(row[i]))
            playerDictionary[keys[i-1]].append(normalVal)
        allStarList.append(int(row[7]))
        


trainingData, testData = divide(.8, playerDictionary, "Points")


trainingLabels = [allStarList[i] for i in range(len(trainingData[0]))]
testLabels = [allStarList[i] for i in range(len(trainingData[0]), len(allStarList), 1)]


        




weightList = [0,0,0,0,0,0]
bias = 0


for i in range(5000):
    weightList = gradient(weightList, 0.07, trainingData,trainingLabels, bias)
    bias -= Bgradient(weightList,bias, trainingData, trainingLabels) * (0.07)
    if i% 200 == 0:
        print(cost(weightList,trainingData, trainingLabels, bias))

 



            



print(weightList, bias)
print(cost(weightList,trainingData, trainingLabels, bias))


testPredictions = predict(testData,weightList, bias)
test = [0 if i < .45 else 1 for i in testPredictions]
print(stats(testLabels, test))
