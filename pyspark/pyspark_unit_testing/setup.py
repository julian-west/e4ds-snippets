from setuptools import setup

setup(
    name="pyspark-unit-testing",
    version="0.1.0",
    packages=["src"],
    description="Example of unit testing with pyspark and pytest",
    install_requires=["pytest==7.1.3", "pyspark==3.3.0"],
)
