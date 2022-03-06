import sys
import pathlib

test_path = pathlib.Path(__file__).resolve().parent
source_path = test_path.parent.joinpath("src")
sys.path.insert(0, str(source_path))
print(source_path)
# print(type(sys.path[1]))

# sys.path.insert(0, source_path)
# sys.path.insert(0, base_path)

#construct test object
from mfp_scraper import scraper
mfps = scraper()

print(mfps.session())

# Test to check if login method works
