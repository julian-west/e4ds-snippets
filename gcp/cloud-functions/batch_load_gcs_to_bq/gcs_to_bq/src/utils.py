"""Utility functions"""


def extract_file_extension(file_name: str) -> str:
    """Extract the file extension from the file path"""
    return file_name.split(".")[-1]


def identify_source_format(
    file_name: str, supported_file_extensions: dict[str, str]
) -> str:
    """Identify the bigquery.SourceFormat of the input data

    raises:
        ValueError if the file extension is not one of the values listed in the
        extension_mapping dictionary

    """
    file_extension = extract_file_extension(file_name)
    source_format = supported_file_extensions.get(file_extension)
    if source_format:
        return source_format
    else:
        raise ValueError(f"{file_extension} source format not supported")


def extract_table_name(file_name: str) -> str:
    """Extract the table name name from the filename

    Assumes the name of the bigquery table the data is being inserted to is the first
    word of the filename

    Examples:
    extract_file_extension(properties/properties_09.csv)
    >>> "properties"

    """
    return file_name.split("/")[0]
