import sys
import pathlib

test_path = pathlib.Path(__file__).resolve().parent
base_path = test_path.parent
source_path = test_path.parent.joinpath("myfitnesspal-scraper/")
sys.path.insert(0, base_path)
sys.path.insert(0, source_path)

#construct test object
import mfp_scraper
mfps = mfp_scraper.scraper()

print(mfps.session())

# Test to check if login method works
