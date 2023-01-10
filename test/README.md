# Kleborate tests

Kleborate comes with a few automated tests to help with development and spotting bugs. To run them, you'll need the `pytest` and `pytest-mock` packages installed.

To run the tests, execute this command from Kleborate's root directory:
```
python3 -m pytest
```

Or if you have [Coverage.py](https://coverage.readthedocs.io) installed, you can run the tests through it to get some code coverage stats:
```
coverage run --source . -m pytest && coverage report -m
```
