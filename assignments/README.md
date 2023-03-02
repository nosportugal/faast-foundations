# FAAST Advance Foundations Assignments

## Introduction

This assignment uses life expectancy in Europe grouped by Country (or other, like group of countries), Age, Sex, and Time. But the data format makes it hard to use. The task consists into cleaning the data and applying the concepts you've learned in the previous modules.

## Installing

Before installing, make sure your `pip` is up to date.

```bash
pip --version
```

Prior to the introduction of `pyproject.toml`-based builds (in PEP 517 and PEP 518), pip had only supported installing packages using setup.py files that were built using `setuptools`. But in version 21.3, pip added support for performing editable installs of packages that use `pyproject.toml`. This means that you can use pip to install packages described in the `pyproject.toml`.

To update pip, run:

```bash
pip install --upgrade pip
```

Now you're ready to go!

1. Clone the Faast-Foundations repo and, from it, create a new repo with just the assignments:

  ```bash
  git clone git@github.com:nosportugal/faast-foundations.git
  cp -r faast-foundations/assignments assignments
  cd assignments
  git init
  ```
  
   You will be later pushing this new repo to your personal GitHub account.

2. Create a virtual environment with `python -m venv .venv`. If you are using conda, you can create a virtual environment with `conda create --name foundations pip`.
3. Activate the virtual environment with `source .venv/bin/activate` or `.venv\Scripts\activate` on Windows. Or, if you are on conda, activate the environment with `conda activate foundations`.
4. Install its dependencies on editable mode with:

  ```bash
  pip install -e '.[dev]'
  ```
  
  And now you should be ready to get started!

## Using this project

Open the `README.md` file inside each assignment and follow the instructions.

> **Note**: Remember that all commands inside the Readme files assume you are in the root of the project.
