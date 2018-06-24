import copy
import json
import operator
import os
import random
import unicodedata


class QuebNameGenerator:
    _BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    _DATA_DIR = os.path.join(_BASE_DIR, 'data')

    def __init__(self):
        """Instantiate a Queb name generator.

        The generator reads from lists of names and surnames, located
        inside the data directory, as JSON files named `names.json`
        and `surnames.json`, respectively.

        Each file contains a list of name entries, with each entry
        containing the "name" itself, a "weight" value denoting the
        relative frequency of the name, and for first names, a
        "gender" value, which can be either "male" or "female".
        """
        self._names = self._get_names()
        self._male_names = self._get_male_names()
        self._female_names = self._get_female_names()
        self._surnames = self._get_surnames()

    def generate(self, gender=None, part=None, snake_case=False, weighted=False):
        """Generate a Queb name.

        :param str gender: Gender of name to generate, one of 'male'
            or 'female'. If not specified, either gender can be
            generated. (optional)
        :param str part: Part of the name to generate, one of 'first'
            or 'last'. If not specified, full names are
            generated. (optional)
        :param bool snake_case: If True, generate a name in
            "snake_case" format, also stripping diacritics if
            any. (default: False)
        :param bool weighted: If True, generate names according to
            their relative popularity. (default: False)
        :return str: The generated name.
        """
        if weighted:
            get_random_name = self._get_weighted_random_name
        else:
            get_random_name = self._get_random_name

        if gender == 'male':
            first_names = self._male_names
        elif gender == 'female':
            first_names = self._female_names
        else:
            first_names = self._names

        name = ''
        surname = ''

        if part == 'first':
            name = get_random_name(first_names)
        elif part == 'last':
            surname = get_random_name(self._surnames)
        else:
            name = get_random_name(first_names)
            surname = get_random_name(self._surnames)

        return self._format_name(name, surname, snake_case=snake_case)

    def _read_name_file(self, filename):
        """Read a name file from the data directory

        :param filename: Name of the file to read.
        :return: A list of name entries.
        """
        file_path = os.path.join(self._DATA_DIR, filename)
        with open(file_path) as f:
            names = json.load(f)

        return names

    def _get_names(self):
        """Get the list of first names.

        :return: A list of first name entries.
        """
        names = self._read_name_file('names.json')
        names = self._compute_weights(names)

        return names

    def _get_male_names(self):
        names = copy.deepcopy(self._names)
        names = [name for name in names if name['gender'] == 'male']
        names = self._compute_weights(names)

        return names

    def _get_female_names(self):
        names = copy.deepcopy(self._names)
        names = [name for name in names if name['gender'] == 'female']
        names = self._compute_weights(names)

        return names

    def _get_surnames(self):
        """Get the list of surnames.

        :return: A list of surname entries.
        """
        names = self._read_name_file('surnames.json')
        names = self._compute_weights(names)

        return names

    @staticmethod
    def _compute_weights(name_list):
        name_list = sorted(name_list, key=operator.itemgetter('weight'))

        cumulative_weight = 0
        for name_entry in name_list:
            name_entry['weight_low'] = cumulative_weight
            cumulative_weight += name_entry['weight']
            name_entry['weight_high'] = cumulative_weight

        return name_list

    @staticmethod
    def _get_random_name(name_list):
        """Get a random name from a given list.

        The choice of the name is fully random.

        :param name_list: The list of names from which to pick.
        :return str: A randomly chosen name.
        """
        length = len(name_list)
        index = random.randrange(length)

        return name_list[index]['name']

    @staticmethod
    def _get_weighted_random_name(name_list):
        """Get a random name from a given list, according to its frequency.

        The choice of the name is random, but weighted in proportion
        to the relative frequency or popularity of each name in the
        list. If one name is twice as popular as another one, then it
        is twice as likely to get chosen.

        :param name_list: The list of names from which to pick.
        :return str: A randomly chosen name.
        """
        total_weight = name_list[-1]['weight_high']
        random_weight = random.randrange(total_weight + 1)

        left = 0
        right = len(name_list) - 1

        while left <= right:
            index = (left + right) // 2
            entry = name_list[index]

            if random_weight > entry['weight_high']:
                left = index + 1
            elif random_weight < entry['weight_low']:
                right = index - 1
            else:
                return entry['name']

    def _format_name(self, name, surname, snake_case=False):
        """Format a first name and a surname into a cohesive string.

        Note that either name or surname can be empty strings, and
        formatting will still succeed.

        :param str name: A first name.
        :param str surname: A surname.
        :param bool snake_case: If True, format the name as
            "snake_case", also stripping diacritics if any. (default:
            False)
        :return str: The formatted name.
        """
        if not name or not surname:
            sep = ''
        elif snake_case:
            sep = '_'
        else:
            sep = ' '

        if snake_case:
            name = self._snakify_name(name)
            surname = self._snakify_name(surname)

        disp_name = '{}{}{}'.format(name, sep, surname)

        return disp_name

    def _snakify_name(self, name):
        """Snakify a name string.

        In this context, "to snakify" means to strip a name of all
        diacritics, convert it to lower case, and replace any spaces
        inside the name with hyphens.

        This way the name is made "machine-friendly", and ready to be
        combined with a second name component into a full "snake_case"
        name.

        :param str name: A name to snakify.
        :return str: A snakified name.
        """
        name = self._strip_diacritics(name)
        name = name.lower()
        name = name.replace(' ', '-')

        return name

    @staticmethod
    def _strip_diacritics(string):
        """Strip diacritics from a string.

        :param str string: The string from which to strip diacritics.
        :return str: The string stripped of its diacritics.
        """
        return (
            unicodedata.normalize('NFKD', string)
            .encode('ascii', 'ignore')
            .decode('utf-8')
        )
