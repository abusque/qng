#!/usr/bin/env python3
import json
import sys

import bs4
import requests


_SOURCE_URL = 'http://www.stat.gouv.qc.ca/statistiques/population-demographie/caracteristiques/noms_famille_1000.htm'

# Length of rows with the name entries.
_DATA_ROW_LENGTH = 29

# For computing indices to data within a row.
_NAMES_PER_ROW = 4
_ENTRY_OFFSET = 8
_NAME_OFFSET = 2
_PERCENT_OFFSET = 4


def _is_data_row(row):
    return len(row.contents) == _DATA_ROW_LENGTH


def _parse_weight(percent_string):
    percent_string = percent_string.replace(',', '.')
    percent = float(percent_string)
    weight = int(percent * 1000)

    return weight


def _parse_name_entry(row, index):
    name_index = index * _ENTRY_OFFSET + _NAME_OFFSET
    percent_index = index * _ENTRY_OFFSET + _PERCENT_OFFSET

    name = row.contents[name_index].string
    percent_string = row.contents[percent_index].string
    weight = _parse_weight(percent_string)

    result = {
        'name': name,
        'weight': weight,
    }

    return result


def main():
    resp = requests.get(_SOURCE_URL)
    soup = bs4.BeautifulSoup(resp.content, 'html.parser')
    rows = soup.find_all('tr')

    header_found = False
    results = []

    for row in rows:
        if not _is_data_row(row):
            continue

        if not header_found:
            # Header has same length as data rows. Skip.
            header_found = True
            continue

        for i in range(_NAMES_PER_ROW):
            result = _parse_name_entry(row, i)
            results.append(result)

    json.dump(results, sys.stdout, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
