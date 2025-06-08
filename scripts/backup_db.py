name: Python
CI

on:
push:
branches: [main]
pull_request:
branches: [main]

jobs:
test:
runs - on: ubuntu - latest

steps:
- uses: actions / checkout @ v3

- name: Set
up
Python
3.10
uses: actions / setup - python @ v4
with:
    python - version: "3.10"

- name: Install
dependencies
run: |
python - m
pip
install - -upgrade
pip
pip
install - r
requirements.txt
pip
install
pytest
pytest - cov

- name: Run
tests
run: |
pytest - -cov =./ --cov - report = xml

- name: Upload
coverage
uses: codecov / codecov - action @ v3

- name: Lint
with flake8
    run: |
    pip
    install
    flake8
    flake8. - -count - -show - source - -statistics