import sys
import pathlib
import pandas
import json

# setup
current_working_dir = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(current_working_dir))
path_list = {
    "source_path": current_working_dir.parent.joinpath("src")
    , "test_files_path": current_working_dir.joinpath("test_files")
    , "base_path": current_working_dir.parent
}
login_info_path = path_list["base_path"].joinpath("login_info.txt")
for value in path_list.values():
    sys.path.insert(0, str(value))

import google_fit_converter, mfp_scraper

def convert

def test_create_point():
    # Load example json that works with google fit
    json_location = str(path_list["test_files_path"].joinpath("test_point.json"))
    with open(json_location, "r") as file:
        comparison_point = json.load(file)

    # Create input dataframe
    csv_location = str(path_list["test_files_path"].joinpath("test_nutrition_data.csv"))
    input_df = pandas.read_csv(csv_location, index_col=0, dtype=object)
    row = input_df.iloc[0]

    converter = google_fit_converter.Converter()
    output_point = converter.create_point(row)

    assert comparison_point == output_point

def test_convert_to_json():
    # Load example json that works with google fit
    json_location = str(path_list["test_files_path"].joinpath("test_json_data.json"))
    with open(json_location, "r") as file:
        comparison_json = json.load(file)

    # Create input dataframe
    csv_location = str(path_list["test_files_path"].joinpath("test_nutrition_data.csv"))
    input_df = pandas.read_csv(csv_location, index_col=0, dtype=object)

    # convert input dataframe to google fit dataframe
    converter = google_fit_converter.Converter() #instantiate class
    dataSourceId = "test"
    output_json = converter.convert(input_df, dataSourceId)

    # Assert converted json matches sample json
    assert output_json == comparison_json
