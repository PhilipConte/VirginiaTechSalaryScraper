import pandas as pd
import locale, os

locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

def file_loc(file_name):
    return os.path.join("files", file_name)

def from_dollar(dollars):
    return int(dollars.replace("$", "").replace(",",""))

def to_dollar(moneyInt):
    return locale.currency( moneyInt, grouping=True )

def pLen(df):
    return len(df.index)

def get_percent(numerator, denominator):
    return "{:.0%}".format(1.0*numerator/denominator)

salaries = pd.read_csv(file_loc("VTsalaries.csv"))
salaries.columns = ['Name', 'Title', 'Pay']
salaries['Pay'] = salaries['Pay'].map(from_dollar)
withheld = salaries.loc[salaries["Name"] == "(Name withheld)"]

salaries["Title"].value_counts().to_csv(file_loc("titles.csv"))

words = ["the", str(pLen(withheld)), "employees with withheld names make up",
    get_percent(pLen(withheld), pLen(salaries)), "of the", str(pLen(salaries)), "employees.",
    "They cost", to_dollar(withheld["Pay"].sum()), "or",
    get_percent(withheld["Pay"].sum(), salaries["Pay"].sum()),
    "of the total", to_dollar(salaries["Pay"].sum())]
with open(file_loc("stats.txt"), "w") as f:
    f.write(" ".join(words))