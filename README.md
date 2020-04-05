![Supported Python Versions](https://img.shields.io/badge/Python->=3.7-blue.svg?logo=python&logoColor=white)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Student/Track Matching Script

## About

This Python script assigns [ENSC](https://ensc.bordeaux-inp.fr) students to specialty tracks based on their grades, track wishes and track capacities.

Input data (student names, grades and track wishes) is loaded from a CSV file. Students ranking and track assignments are written to CSV files.

Algorithm goes as follow:

- For each student, a weighted average of their grades during past semesters is computed.
- These average grades are used to sort students by merit (best first).
- In that order, students are assigned to the highest non-full track in their wishes.

## Usage

```bash
> python -m match <students CSV file name>
```

## Development Notes

This script needs Python 3.7+ and uses the following tools:

- [black](https://github.com/psf/black) for code formatting.
- [pylint](https://www.pylint.org/) and [mypy](http://mypy-lang.org/) for linting.

Run the following commands to check the codebase.

```bash
> python -m pylint match.py  # linting (including type checks)
> python -m mypy match.py    # type checks only
```
