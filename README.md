# VirginiaTechSalaryScraper


In light of the recent "Virginia Tech Giving Day", I was inspired to take a closer look at some of the ways VT uses its funds.

This script scrapes the data.richmond.com salaries pages for VT, extracts the salaries, and stores them as a csv. It can then be opened in either a text editor or Excel and searched at one's leasure. Additionally, one can interact with the data directly from the interpreter when the script is run with the -i flag.

## Installation
 Begin by installing python3 and virtualenv

Then:
```bash
# Clone this repository
git clone https://github.com/PhilipConte/VirginiaTechSalaryScraper.git

# Go into the repository
cd VirginiaTechSalaryScraper

# Create a virtual environment
virtualenv env

#activate the virtual environment
source env/bin/activate

# install dependencies
pip install -r requirements.txt
```

## Usage
```bash
#run it normally
python PayScrape.py

#use the -i flag to be dropped into the shell to play around with the data interactively
python -i PayScrape.py
```
either way, VTsalaries.csv will be created
