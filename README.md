# Overview #

This program scrapes data from myfitnesspal and saves it to various locations

## How to run ##

1. Clone this repository
2. In terminal, navigate to the repository
3. In terminal, type ```python3 setup.py install```
4. Optionally Enter myfitnesspal login information into login_info.txt for ease of use
5. Change directory to ```./myfitnesspal-scraper```
6. Execute 'run.py' (e.g. ```python3 run.py```)
7. Select option 0 to scrape from myfitnesspal. Scraping must occur before all other options
8. Select option 1, 2, or 3 to save scraped data.

## Requirements ##

### Accounts ###

- A valid myfitnesspal account

### Python libraries ##

- python 3.6+
- beautifulsoup4
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
