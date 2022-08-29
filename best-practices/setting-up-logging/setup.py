from setuptools import find_packages, setup

setup(
    name="logging_demo",
    version="0.1",
    description="Test logging",
    license="MIT",
    packages=find_packages(include=["src", "src.*"]),
    zip_safe=False,
)
