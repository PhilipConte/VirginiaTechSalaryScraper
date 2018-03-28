import pandas as pd
import locale, os

def file_loc(file_name):
    return os.path.join("files", file_name)

def parse_dollar(dollars):
    return int(dollars.replace("$", "").replace(",",""))

def analyses(emps):
    emps["Total gross pay"] = emps["Total gross pay"].apply(lambda x: moneyToInt(x))
    withheld = emps.loc[emps["Name"] == "(Name withheld)"]
    print("the", str(pLen(withheld)), "employees with withheld names make up",
        "{:.0%}".format(1.0*pLen(withheld)/pLen(emps)), "of the", pLen(emps), "employees.",
        "They cost", intToMoney(withheld["Total gross pay"].sum()), "or",
        "{:.0%}".format(1.0*withheld["Total gross pay"].sum()/emps["Total gross pay"].sum()),
        "of the total", intToMoney(emps["Total gross pay"].sum()))

salaries = pd.read_csv(file_loc("VTsalaries.csv"))
salaries.columns = ['Name', 'Title', 'Pay']
salaries['Pay'] = salaries['Pay'].map(parse_dollar)

myS = list(set(salaries["Title"].tolist()))
with open(file_loc("set of titles.txt"), "w") as f:
    for item in myS:
        f.write(item+'\n')