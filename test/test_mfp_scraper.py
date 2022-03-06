import sys
import pathlib

test_path = pathlib.Path(__file__).resolve().parent
base_path = test_path.parent
source_path = test_path.parent.joinpath("src")
sys.path.insert(0, str(base_path))
sys.path.insert(0, str(source_path))

# setup
import mfp_scraper
mfps = mfp_scraper.scraper()
full_login_info_path = base_path.joinpath("login_info.txt")
with open(f"{full_login_info_path}", "r") as file:
    username_line = file.readline()
    username = username_line.split("=")[1][:-1]
    password_line = file.readline()
    password = password_line.split("=")[1]

# Test to check if login method works
def test_login():
    assert mfps.login(username, password) == True
