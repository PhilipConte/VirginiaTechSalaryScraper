from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
import requests, pickle

rawPickleFile = "rawPages.p"

year = 2016
baseURL = "http://data.richmond.com/salaries/"+str(year)+"/state/virginia-polytechnic-institute-and-state-university-virginia-tech?page="

def downloadPages():
    page = 1
    reqList = []

    while True:
        req = requests.get(baseURL+str(page))
        req.raise_for_status()
        if (len(reqList) > 0 and req.content == reqList[-1].content):
            break
        reqList.append(req)
        page += 1
        print(page)
    
    pickle.dump(reqList, open(rawPickleFile, "wb"))

def getList(inputList):
    theList = []
    for index, page in enumerate(inputList):
        soup = BeautifulSoup(page.content, "html.parser")
        values = soup.findAll('td')[10:]
        
        empList = list(zip(*(iter(values),)*3))
        for emp in empList:
            try:
                theList.append([item.string.strip() for item in emp])
            except AttributeError as e:
                print("badly formed list on page ", index)
                continue

    return theList

def listToPd(inputList):
    headers = ["Name", "Title", "Total gross pay"]
    df = pd.DataFrame(inputList, columns=headers)
    return df

def returnData():
    if not Path(rawPickleFile).is_file():
        downloadPages()
    return listToPd(getList(pickle.load(open(rawPickleFile, "rb"))))

empList = returnData()
empList.to_csv('VTsalaries.csv', index=None, sep=",")
