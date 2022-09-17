from main import extract_ctry_date_and_extension_from_filename

import pytest


@pytest.fixture(scope="module")
def test_us_csv_file_name():
    return "us_20220917.csv"


@pytest.fixture(scope="module")
def test_gb_csv_file_name():
    return "gb_20220917.csv"


# parametrize with fixture
@pytest.mark.parametrize(
    "filename,expected",
    [
        ("test_us_csv_file_name", ("us", "20220917", "csv")),
        ("test_gb_csv_file_name", ("gb", "20220917", "csv")),
    ],
    ids=["us", "gb"],
)
def test_extract_ctry_date_and_extension_from_fileanme(filename, expected, request):
    filename = request.getfixturevalue(filename)
    assert extract_ctry_date_and_extension_from_filename(filename) == expected
