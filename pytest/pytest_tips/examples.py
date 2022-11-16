"Example functions"
import logging
import re
import time


def sum_list(my_list):
    return sum(my_list)


def remove_special_characters(input_string):
    return re.sub(r"[^A-Za-z0-9]+", "", input_string)


def divide(a, b):
    return a / b


def printing_func(name):
    print(f"Hello {name}")


def logging_func():
    logging.info("Running important function")
    # some more code...
    logging.info("Function completed")


def subtract_floats(a, b):
    return a - b


def my_slow_func():
    # some long running code...
    time.sleep(5)
    return True


def add(a, b):
    """Add two numbers

    >>> add(2,2)
    4
    """
    return a + b


def my_function_with_print_statements():
    print("foo")
    print("bar")
    return True
