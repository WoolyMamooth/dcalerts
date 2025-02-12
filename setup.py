from setuptools import setup, find_packages

setup(
    name="dcalerts",
    version="0.2.0",
    description="A Python decorator to send Discord webhook notifications before and after function execution.",
    author="WoolyMamooth",
    author_email="",
    url="https://github.com/WoolyMamooth/dcalerts",
    packages=find_packages(),
    install_requires=[
        "requests",
        "time",
        "functools"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
