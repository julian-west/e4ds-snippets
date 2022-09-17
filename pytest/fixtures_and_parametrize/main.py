import re


def extract_ctry_date_and_extension_from_filename(uri: str) -> tuple[str, str, str]:
    """Extract country, date and file extension from a filename"""

    file_name_regex_pat = r"(\w+)_(\d{8})\.(.*)"

    if matches := re.match(file_name_regex_pat, uri):
        return matches.groups()
    else:
        raise ValueError(f"{uri} is not a valid filename")
