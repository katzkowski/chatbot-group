import json
import csv
import pandas as pd
from pathlib import Path
from intentclassificator import classifyIntent, writeMessagetoTrainingData


def answerHandler(inputjson):
    
    obj = json.loads(inputjson)
    answer = findAnswer(str(obj['message'].lower()), getRoomId(str(obj['room'])))
    
    if writeMessagetoTrainingData(str(obj['message'])) : print("added message to training data")
    else : print("added nothing to training data")

    #json wird wieder zusammen gepackt                    
    return json.dumps({"level": 1,"sender": "bot","room":answer[1],"items":[],"message": answer[0]})


#finds an answer to your message :)
def findAnswer(msg, roomid = -1):
    if roomid == -1 : raise ValueError("Invalid room id!")
    
    if classifyIntent(msg) == 1:
        for elem in findEntry(roomid, 4).split(';'):
            print(elem.split('?')[0])
            if elem.split('?')[0] in msg :
                roomid = int(elem.split('?')[1])
                return (getRoomIntroduction(roomid),getRoomName(roomid))
            
    elif classifyIntent(msg) == 2:
         return (getRoomDescription(roomid), getRoomName(roomid))

    elif classifyIntent(msg) == 3:
         return (getRoomIntroduction(roomid), getRoomName(roomid))
         
    elif classifyIntent(msg) == 4:
        return (get_inventory(), getRoomName(roomid))
    elif classifyIntent(msg) == 5:
        return (aboutHandler(msg), getRoomName(roomid))    
    else:
        for elem in findEntry(roomid, 5).split(';'):
            if elem.split('&')[0] in msg : return (elem.split('&')[1], getRoomName(roomid))

    return ("I have no idea what you want",getRoomName(roomid))



"""
Returns the csv file entry specified by the input coordinates
id = row / which represent a room
column = column / which represent a property of the rooms
@throws ValueError if parameters ar not of type int
"""
def findEntry(id: int, column: int) -> str:

    script_location = Path(__file__).absolute().parent
    file_location = script_location / 'roomsGW2.csv'
    file = file_location.open()
    
    with open(file_location, 'r', newline = '') as file:
        reader = csv.reader(file, delimiter='$')
        rooms = [row for row in reader]

    if not len(rooms) > id >= 0 or not len(rooms[id]) > column >= 0:
            return "csv table coordinates are out of range"
    else :
        return rooms[id][column]
   

#Get the room id by room name
def getRoomId(msg: str) -> int:
    
    script_location = Path(__file__).absolute().parent
    file_location = script_location / 'roomsGW2.csv'
    file = file_location.open()
    
    with open(file_location, 'r', newline = '') as file:
        reader = csv.reader(file, delimiter='$' )
        rooms = [row for row in reader]
        
    for count in range(0,len(rooms)):
        
        if rooms[count][1] in msg: return int(findEntry(count,0))
    else: return -1

#Get the current room
def getRoomName(id: int) -> str:
    return findEntry(id, 1)

#Get introduction of the room with id    
def getRoomIntroduction(id: int) -> str:
    return findEntry(id, 2)

#Get description of the room with id
def getRoomDescription(id: int) -> str:
    return findEntry(id, 3)

#Handles about questions
def aboutHandler(msg: str) -> str:
    if "who has" in msg : return "I am programmed by student members of the Chatbots:Talk-To-Me Team"
    elif "who" in msg :return "I am a Chatbotgame with a browser interface"
    elif "why" in msg: return "I was born because the virtualmarsexplporation Project has not enought places for all the students"
    elif "when" in msg: return "I was born during the summer semester of 2020"
    elif "what" in msg: return "I want to deliver fun and interesting facts about Bremen"
    elif "where" in msg: return "I was programmed in Bremen"
    elif "do you like" in msg: "of course not"
    else: return "I didnt understand your about chatbot: question." 
    
# manages a local saved inventory
# if "items" in s:

def get_inventory():
    with open("inventory.csv") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        line_count = 0
        item_count = 0
        data = ""
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            if row["Found"] == "True":
                if item_count == 1:
                    data += " and "
                data += str(row["Item-Name"]) + ", " + str(row["Description"])
                item_count = 1
        if item_count == 1:
            data += ". "
        else:
            data = "A yawning void looks at you from your inventory. "
        return data
        
#adds a items to the inventory(sets the variable of the item from 'False' to 'True')
#optional: add a quantity column in the csv

def add_inventory(name):
    with open("inventory.csv") as csvfile:
        df = pd.read_csv("test.csv")
        #df.head(3) #prints 3 heading rows
        df.loc[df["Item-Name"]==name, "Found"] = "True"
        #next line is not tested!
        #df.loc[df["Item-Name"]==, "Item-Quantity"] = ([df["Item-Name"]==, "Item-Quantity"] +1)
        df.to_csv("inventory.csv", index=False)

    