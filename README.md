# Overview #

This program scrapes data from myfitnesspal and saves it to various locations

___

## Tested operating systems ##

- Linux (Linux Mint)
- Windows Subsystem for Linux (WSL Ubuntu)

___

## How to run ##

1. Clone this repository
2. In terminal, navigate to the repository
3. In terminal, type ```python3 -m pip install -r requirements.txt```
4. Optionally Enter myfitnesspal login information into ```login_info.txt``` for ease of use
5. Change directory to ```./src```
6. Execute 'run.py' (e.g. ```python3 run.py```)
7. Select option 0 to scrape from myfitnesspal. Scraping must occur before all other options
8. Select option 1, 2, or 3 to save scraped data.
9. To run tests, navigate to the root of the repository and type ```pytest``` in the commandline

___

## Requirements ##

### Accounts ###

- A valid myfitnesspal account

### Python libraries ##

- python 3.6+
- beautifulsoup4
- requests
- pandas
- flask
- lxml
- pytest

___

## Todo ##

### Gather calorie data ##

- [x] Scrape from myfitnesspal
- [x] Speed up data collection

### Save to various locations ##

- [x] Save as a csv file
- [ ] Save to google fit
- [ ] Save to database
