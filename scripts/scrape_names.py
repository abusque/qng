#!/usr/bin/env python3
import json
import os
import sys

import bs4
import requests


_SOURCE_URL_FMT = 'https://www.prenomsquebec.ca/recherche.php?sexe={gender}&annee={year}'

# For computing valid URLs for pages to scrape.
_GENDERS = ['garcons', 'filles']
_YEAR_BEGIN = 1980
_YEAR_END = 2017

# Indices to data within a row.
_NAME_INDEX = 1
_WEIGHT_INDEX = 2

# Retrieve list of "canonical" name forms.
_BASE_DIR = os.path.dirname(os.path.realpath(__file__))
_CANONICAL_NAMES_FILE = os.path.join(_BASE_DIR, 'canonical_names.json')
with open(_CANONICAL_NAMES_FILE) as f:
    _CANONICAL_NAMES = json.load(f)


def _canonicalize_name(name: str) -> str:
    # Initially convert to lower case for comparison with canonical
    # forms.
    name = name.lower()

    if name in _CANONICAL_NAMES:
        name = _CANONICAL_NAMES[name]

    name = name.replace(' ', '-')
    name = name.title()

    return name


def _parse_row(row):
    name = row.contents[_NAME_INDEX].string
    weight_string = row.contents[_WEIGHT_INDEX].string

    name = _canonicalize_name(name)
    weight = int(weight_string)

    return name, weight

def _process_entries(gender, year, names):
    url = _SOURCE_URL_FMT.format(gender=gender, year=year)

    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.content, 'html.parser')
    rows = soup.find_all('tr')

    for row in rows:
        name, weight = _parse_row(row)
        if name not in names:
            names[name] = {
                'gender': gender,
                'weight': 0,
            }

        names[name]['weight'] += weight


def main():
    results = []
    names = {}

    for gender in _GENDERS:
        for year in range(_YEAR_BEGIN, _YEAR_END + 1):
            _process_entries(gender, year, names)

    for name, entry in names.items():
        if entry['gender'] == 'garcons':
            gender = 'male'
        else:
            gender = 'female'

        results.append({
            'name': name,
            'gender': gender,
            'weight': entry['weight'],
        })

    json.dump(results, sys.stdout, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
