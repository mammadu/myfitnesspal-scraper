# Overview #

This program scrapes data from myfitnesspal and saves it to various locations

## How to run ##

1. Clone this repository
2. In terminal, navigate to the repository
3. In terminal, type ```python3 setup.py install```
4. Change directory to ```./myfitnesspal-scraper```
5. Execute 'run.py' (e.g. ```python3 run.py```)
6. Select option 0 to scrape from myfitnesspal. Enter login information in login_info file or manually

## Requirements ##

### Python libraries ##

- python 3.6+
- beautifulsoup
- requests
- datetime
- pandas
- flask
- getpass
- lxml

## Todo ##

### Gather calorie data ##

- [x] Scrape from myfitnesspal
- [ ] Speed up data collection

### Save to various locations ##

- [x] Save as a csv file
- [ ] Save to google fit
- [ ] Save to database
