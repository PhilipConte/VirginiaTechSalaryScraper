from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
import requests, pickle, locale, os

locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

fileDir = "files"
rawPickleFile = os.path.join(fileDir, "rawPages.p")
csvFile = os.path.join(fileDir, "VTsalaries.csv")

year = 2016
baseURL = "http://data.richmond.com/salaries/"+str(year)+"/state/virginia-polytechnic-institute-and-state-university-virginia-tech?page="

def downloadPages():
    page = 1
    pages = []
    print("Downloading pages:")
    while True:
        req = requests.get(baseURL+str(page))
        req.raise_for_status()
        if (len(pages) > 0 and req.content == pages[-1].content):
            break
        pages.append(req)
        page += 1
        print(page)
    print("done")
    pickle.dump(pages, open(rawPickleFile, "wb"))

def getList(inputList):
    theList = []
    for index, page in enumerate(inputList):
        soup = BeautifulSoup(page.content, "html.parser")
        values = soup.findAll("td")[10:]
        
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

def moneyToInt(moneyStr):
    return int(''.join(ch for ch in moneyStr if ch.isdigit()))

def intToMoney(moneyInt):
    return locale.currency( moneyInt, grouping=True )

empList = returnData()
empList.to_csv(csvFile, index=None, sep=",")
