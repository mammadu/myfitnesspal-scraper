#!/usr/bin/python3

import mfp_scraper, pandas, os

class frontend():

    def __init__(self):
        self.options = [
        "scrape myfitnesspal"
        , "save to csv"
        , "save to google fit"
        , "save to MySQL database"
    ]
        self.start_date = ""
        self.end_date = ""
        self.login_path = ".."
        self.save_path = "../myfitnesspal_data/"
    
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

    def get_dates(self):
        self.start_date = input("enter start date (YYY-MM-DD): ")
        self.end_date = input("enter end date (YYY-MM-DD): ")
        print()
    
    def get_login(self):
        login = {
            "username": ""
            , "password": ""
        }
        choice = input(f"use default login found in '{self.login_path}/login_info'? (y/n):")
        if choice.lower() == "y":
            with open(f"{self.login_path}/login_info", "r") as file:
                username_line = file.readline()
                login["username"] = username_line.split("=")[1]
                password_line = file.readline()
                login["password"] = password_line.split("=")[1]
        else:
            login["username"] = input("Enter myfitnesspal username: ")
            login["password"] = input("Enter myfitnesspal password: ")

        return login

    def scrape_myfitnesspal(self):
        self.get_dates()
        scraper = mfp_scraper.scraper()
        login = self.get_login()
        scraper.login(login["username"], login["password"])
        list_of_dates = scraper.list_of_dates(self.start_date, self.end_date)
        data = scraper.nutrition_dataframe(list_of_dates)
        return data

    def save_to_csv(self, data):
        choice = input("save to default path? (y/n): ")
        if choice.lower() == "y":
            data.to_csv(f"{self.save_path}/data.csv")
        else:
            path = input("specify csv save path: ")
            data.to_csv(f"{path}/data.csv")


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