from bs4 import BeautifulSoup
import requests
import csv


createdPlayer = 0
playerWithData = 0
alphabeticalIndex = 0
PlayerListHeader = "https://www.basketball-reference.com/players/"
PlayerPageHeader = "https://www.basketball-reference.com/"
headerSufficies = ["a/", "b/", "c/", "d/", "e/", "f/", "g/", "h/", "i/", "j", "k/", "l/", "m/", "n/", "o/", "p/", "q/", "r/", "s/", "t/", "u/", "v/", "w/", "x/", "y/", "z/"]
playerData = {}
for i in range(len(headerSufficies)): 
    webpage_request = requests.get('https://www.basketball-reference.com/players/' + headerSufficies[i])
    webpage =  BeautifulSoup(webpage_request.content, "html.parser")
    table = webpage.find("table")
    links = table.findAll("a")
    for row in table.findAll('tr'):
        list_of_cells = []
        for i in range(3):
            text = row.findAll(["th","td"])[i].get_text()
            list_of_cells.append(text)
        if list_of_cells[1] != "From" and int(list_of_cells[1]) > 1997 and int(list_of_cells[2]) - int(list_of_cells[1]) > 6:
            playerData[list_of_cells[0]] = []
            playerCell = row.findAll(["th","td"])[0]
            link = row.find("a")
            player_webpage_request = requests.get(PlayerPageHeader + link["href"]) 
            playerWebpage = BeautifulSoup(player_webpage_request.content, "html.parser")
            playerTable = playerWebpage.find("table")
            row2  =  playerTable.findAll('tr')[2] 
        
            if "Did Not Play" in row2.get_text() or int(row2.findAll(["th", "td"])[5].get_text()) <= 30:
                playerData.pop(list_of_cells[0])
            else:
                
                points = float(row2.findAll(["th","td"])[29].get_text())
                trueShooting = float(row2.findAll(["th","td"])[9].get_text()) + (.44 * float(row2.findAll(["th","td"])[19].get_text()))
                trueShooting = points/ (2* trueShooting)
                assists = float(row2.findAll(["th","td"])[24].get_text())
                rebounds = float(row2.findAll(["th","td"])[23].get_text())
                blocks = float(row2.findAll(["th","td"])[26].get_text())
                steals = float(row2.findAll(["th","td"])[25].get_text())
                allstar = 0 if playerTable.find("span" ,{"class" : "sr_star"}) is None else 1
                playerData[list_of_cells[0]] = [points, assists, rebounds, blocks, steals, trueShooting, allstar]
        

        




   
with open('NBAdata.csv', 'w') as f: 
    writer = csv.writer(f)
    writer.writerow(["Player Name", "Points Per Game",  "Assists Per Game", "Rebounds Per Game", "Blocks Per Game", "Steals Per Game", "True Shooting Percentage", "All Star Player?"])
    for key in playerData.keys():
        tempList = list(playerData[key])
        tempList.insert(0, str(key).encode('utf8'))
        writer.writerow(tempList)
print(playerData)


            








        
            





    
 




