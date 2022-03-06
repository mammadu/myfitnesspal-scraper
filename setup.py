from setuptools import setup

setup(
    name = 'myfitnesspal-scraper'
    , version = '0.1'
    , description = "Scrapes nutrional data from myfitnesspal and saves to various locations"
    , url='https://github.com/mammadu/myfitnesspal-scraper'
    , python_requires='>=3.6'
    , install_requires = [
        'beautifulsoup4'
        , 'requests'
        , 'datetime'
        , 'pytest'
        , 'pandas'
        , 'flask'
        , 'lxml'
    ]
)