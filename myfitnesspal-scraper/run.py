#!/usr/bin/python3

import mfp_scraper
import chrono
import getpass
import pathlib

class frontend():

    def __init__(self):
        self.options = [
        "scrape myfitnesspal"
        , "save to csv"
        , "save to google fit"
        , "save to MySQL database"
        ]
        self.filename = pathlib.Path(__file__).resolve()
        self.login_info_filepath = self.filename.parent.parent
        self.login_info_filename = "login_info.txt"
        self.save_path = self.filename.parent.parent.joinpath('myfitnesspal_data')
        self.start_date = ""
        self.end_date = ""
    
    def print_title(self):
        program_version = "0.1"
        program_date = "2021-11-21"
        title = " ".join(["Myfitnesspal scraper", program_version, program_date])
        print(title)
        print()

    def print_dates(self, start_date = "", end_date = ""):
        dates = f"start date: {start_date}, end date: {end_date}"
        print(dates)

    def option_select(self):
        while(True):
            print()
            print("Options")
            for idx, option in enumerate(self.options):
                print(f"{idx}: {option}")
            print()
            user_input = input("enter option number or 'quit': ")
            if user_input == "quit":
                return user_input
            try:
                if int(user_input) in range(len(self.options)):
                    return user_input
                else:
                    print("invalid choice")
            except:
                print("enter number of option")

    def get_dates(self): #todo: implement logic to deal with bad dates
        chron = chrono.chrono()
        current_date = chron.today_to_ymd()
        choice = input(f"scrape from {current_date} to {current_date}? (y/n): ")
        if choice.lower() == "y":
            self.start_date = current_date
            self.end_date = current_date
        else:
            improper_dates = True
            while improper_dates == True:
                self.start_date = input("enter start date (YYYY-MM-DD): ")
                self.end_date = input("enter end date (YYY-MM-DD): ")
                if (chron.is_ymd_format(self.start_date) == False) or (chron.is_ymd_format(self.end_date) == False):
                    print("dates are improperly formatted")
                    continue
                if chron.future_before_past(self.start_date, self.end_date):
                    print("dates out of order")
                else:
                    improper_dates = False
            print()
    
    def get_login(self):
        login = {
            "username": ""
            , "password": ""
        }
        full_login_info_path = self.login_info_filepath.joinpath(self.login_info_filename)
        print(self.filename)
        choice = input(f"use default login found in '{full_login_info_path}'? (y/n): ")
        if choice.lower() == "y":
            with open(f"{full_login_info_path}", "r") as file:
                username_line = file.readline()
                login["username"] = username_line.split("=")[1][:-1]
                password_line = file.readline()
                login["password"] = password_line.split("=")[1]
        else:
            login["username"] = input("Enter myfitnesspal username: ")
            login["password"] = getpass.getpass(prompt='Enter myfitnesspal password: ')

        return login

    def scrape_myfitnesspal(self):
        scraper = mfp_scraper.scraper()
        login = self.get_login()
        login_success = scraper.login(login["username"], login["password"])
        if login_success == True:
            self.get_dates()
            chron = chrono.chrono()
            list_of_dates = chron.list_of_dates(self.start_date, self.end_date)
            data = scraper.nutrition_dataframe(list_of_dates)
        else:
            print("Could not log in. Review myfitnesspal username and password")
            data = None
        return data

    def save_to_csv(self, data):
        save_name = "data.csv"
        choice = input(f"save '{save_name}' to default path ('{self.save_path}')? (y/n): ")
        if choice.lower() == "y":
            save_location = self.save_path.joinpath(save_name)
        else:
            path = input("specify csv save path: ")
            save_location = pathlib.Path(path).joinpath(save_name)
        try:
            print(f"saving to {save_location}")
            data.to_csv(save_location)
        except (UnboundLocalError, AttributeError) as ex:
            print("you must first scrape myfitnesspal")
        except Exception as ex:
            print(f"could not save to {save_location}")
            # raise ex



def main():
    terminal = frontend()
    terminal.print_title()
    terminal.print_dates(terminal.start_date, terminal.end_date)
    user_input = terminal.option_select()
    while (user_input != "quit"):
        if terminal.options[int(user_input)] == "scrape myfitnesspal":
            data = terminal.scrape_myfitnesspal()
        elif terminal.options[int(user_input)] == "save to csv":
            terminal.save_to_csv(data)
        else:
            print(f"Option {user_input} has not been implemented yet")
            print()
        terminal.print_dates(terminal.start_date, terminal.end_date)
        user_input = terminal.option_select()

if __name__ == "__main__":
    main()