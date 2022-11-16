"Example tests"
import logging

import pytest

from .examples import (
    divide,
    logging_func,
    my_function_with_print_statements,
    my_slow_func,
    printing_func,
    remove_special_characters,
    subtract_floats,
    sum_list,
)


def test_sum_list():

    # arrange
    test_list = [1, 2, 3]

    # act
    answer = sum_list(test_list)

    # Assert
    assert answer == 6


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


def test_type_error():
    with pytest.raises(TypeError):
        divide("abc", 10)


def test_printing_func(capsys):
    name = "John"
    printing_func(name)

    output = capsys.readouterr()
    assert output.out == "Hello John\n"


def test_logging_func(caplog):
    caplog.set_level(logging.INFO)
    logging_func()
    records = caplog.records

    # first message
    assert records[0].levelname == "INFO"
    assert records[0].message == "Running important function"

    # second message
    assert records[1].levelname == "INFO"
    assert records[1].message == "Function completed"


def test_add_floats():
    assert subtract_floats(1.2, 1.0) == pytest.approx(0.2)


def test_preprocess_categorical_columns():
    ...


def test_preprocess_numerical_columns():
    ...


def test_preprocess_text():
    ...


def test_train_model():
    ...


@pytest.mark.slow
def test_my_slow_func():
    assert my_slow_func()


@pytest.mark.parametrize(
    "input_string,expected",
    [
        ("hi*?.", "hi"),
        ("f*()oo", "foo"),
        ("1234bar", "1234bar"),
        ("", ""),
    ],
)
def test_remove_special_characters(input_string, expected):
    assert remove_special_characters(input_string) == expected


def test_my_function_with_print_statements():
    assert my_function_with_print_statements()


@pytest.mark.parametrize(
    "input_string,expected",
    [
        ("hi*?.", "hi"),
        ("f*()oo", "foo"),
        ("1234bar", "1234bar"),
        ("", ""),
    ],
    ids=[
        "remove_special_chars_from_end",
        "remove_special_chars_from_middle",
        "ignore_numbers",
        "no_input",
    ],
)
def test_remove_special_characters_id_arg(input_string, expected):
    assert remove_special_characters(input_string) == expected


@pytest.mark.parametrize(
    "input_string,expected",
    [
        pytest.param("hi*?.", "hi", id="remove_special_chars_from_end"),
        pytest.param("f*()oo", "foo", id="remove_special_chars_from_middle"),
        pytest.param("1234bar", "1234bar", id="ignore_numbers"),
        pytest.param("", "", id="no_input"),
    ],
)
def test_remove_special_characters_pytest_param(input_string, expected):
    assert remove_special_characters(input_string) == expected
