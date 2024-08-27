import csv, os
from collections import defaultdict

from . import helpers


class LexiconError(Exception):
    pass


class Lexicon():
    """
    Class for reading a configuration file to build the stem component 
    of a lexc file for use in a foma parser.
    """
    def __init__(self, config: dict):
        self._validate_config_file(config)
        self._make_categories(config["legal_categories"])
        self._make_dict(config["dictionary"])

    def as_dict(self) -> dict:
        """
        Returns a dictionary of all stems in the Lexicon object.
        """
        return self.dict.copy()

    def as_lexc_str(self) -> str:
        """
        Returns all stems as a string formatted for input to lexc.
        Lists each category under 'Root', and lists each stem
        under its 'RootCategory'.
        """
        # list all categories under 'Root'
        stems_txt = 'LEXICON Root\n'
        for category in self.dict.keys():
            stems_txt += 'Root' + category + ' ;\n'

        # list stems under individual RootCategories
        for category, stems in self.dict.items():
            stems_txt += '\nLEXICON Root' + category + '\n'
            for stem in stems:
                stems_txt += "{} \t{} ;\n".format(self.lexc_form(stem),
                                                    category)
            stems_txt += '\nLEXICON ' + category + '\n'

        return stems_txt
    
    @staticmethod
    def lexc_form(word: str) -> str:
        """
        Takes a neutral gitksan wordform using underscore and reformats
        with an initial apostrophe, into an appropriate single-word unit
        with updated boundaries and flags where needed (e.g. big T).
        """
        word = helpers.neutral_to_lexc(word)
        return word

    def _make_categories(self, category_list: list):
        """
        Reads and stores a standardized list of valid categories.
        Only words with these categories will ultimately be imported.
        Categories stored as camelcase.
        """
        categories = [helpers.camelcase(cat) for cat in category_list]
        self.categories = list(set(categories))

    def _make_dict(self, dict_input: list or dict):
        """
        Reads dictionary items from the files listed in config.
        If input is a list of dictionaries, loads each to the lexicon.
        """
        self.dict = defaultdict(list)

        if type(dict_input) is list:
            for item in dict_input:
                self._import_dict(item)
        else:
            self._import_dict(dict_input)

    def _import_dict(self, input_dict: dict):
        """
        When input a valid dictionary, imports all stems from that
        dictionary which have a valid category (based on config) to
        the Lexicon object.
        Words with invalid categories are not imported.
        """
        input_dict = self._validate_dict_type(input_dict)

        self.illegal_categories = set()
        for cat in input_dict.keys():
            if cat in self.categories:
                self.dict[cat] += input_dict[cat]
            elif helpers.camelcase(cat) in self.categories:
                self.dict[helpers.camelcase(cat)] += input_dict[cat]
            else:
                self.illegal_categories.add(cat)

    @classmethod
    def _validate_config_file(cls, config: dict) -> bool:
        """
        Ensures that the configuration file contains the needed keys
        to successfully build and export a lexicon object:
            - dictionary
            - legal_categories
        Ensures that dictionary items exist and are of the right type.
        """
        # check for required keys to compile lexicon
        if not "dictionary" in config:
            raise LexiconError(
                'Configuration file requires "dictionary" key')
        if not "legal_categories" in config:
            raise LexiconError(
                'Configuration file requires "legal_categories" key')

        # check type and location of dictionary input
        d_item = config["dictionary"]
        if type(d_item) is dict:
            return True
        elif type(d_item) is str and d_item[-4:] == '.csv':
            cls._validate_dict_filepath(config)
        else:
            raise LexiconError(
                'Dictionary input must be dict or path to csv file')
        
        return True

    @staticmethod
    def _validate_dict_filepath(config: dict) -> bool:
        """
        Ensures that the dictionary input, if a filename, points to an
        existing file. Attempts to resolve relative filepaths
        using directory information from config file.
        """
        if os.path.exists(config["dictionary"]):
            return True
        if 'dir' in config:
            long_filename = os.path.join(
                config['dir'], config["dictionary"])
            if os.path.exists(long_filename):
                config["dictionary"] = long_filename
                return True

        raise FileNotFoundError(
                    'No such lexicon file: {}'.format(config['dictionary']))

    @staticmethod
    def _validate_dict_type(input_dict: dict):
        """
        Checks that the lexicon input is a dictionary or is
        convertable to one, and returns the loaded dictionary.
        If lexicon input is a csv file, uses a GitDictCSV loader to 
        return a dictionary.
        Other input types will raise an error.
        """
        if type(input_dict) is dict:
            return input_dict
        elif type(input_dict) is str and input_dict[-4:] == '.csv':
            return GitDictCSV.load(input_dict)
        else:
            raise LexiconError('Unknown dictionary type')


class GitDictCSV():
    """
    Object to convert a Gitksan dictionary CSV to a dictionary
    in the correct format for reading to foma/lexc.
    """
    
    @classmethod
    def load(cls, filename: str) -> dict:
        """
        Shorthand to create a reader object 
        and return the loaded dictionary.
        """
        return cls(filename).dictionary

    def __init__(self, filename: str):
        self.dictionary = defaultdict(list)
        self._read_from_csv(filename)

    def _read_from_csv(self, filename: str):
        """
        Reads the CSV file and imports rows containing sufficient info.
        """
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if self.is_legal_row(row):
                    self._add_entries(row)

    def _add_entries(self, entry: dict):
        """
        Adds one CSV row to the dictionary object.
        """
        for cat in self._categories_from_entry(entry):
            for word in self._wordforms_from_entry(entry):
                self.dictionary[cat].append(word)

    @staticmethod
    def _categories_from_entry(entry: dict) -> list:
        """
        Reads categories in a CSV row (entry) and returns as a list.
        """
        return entry['categories'].split('; ')

    @staticmethod
    def _wordforms_from_entry(entry: dict) -> list:
        """
        Reads a CSV row (entry) and returns a list of all wordforms in
        the 'word' and 'plural' columns, formatted for the parser
        and marked with a stress symbol ($) if available.
        """
        words = [helpers.csv_to_neutral(wd) for wd
                in entry['word'].split('; ')]
        words = helpers.assign_stress(words, entry['stress'])

        plurals = [helpers.csv_to_neutral(wd) for wd
                in entry['plural form'].split('; ')
                if wd]
        if plurals:
            plurals = helpers.assign_stress(plurals, entry['plural stress'])
            words += plurals
        return words
    
    @staticmethod
    def is_legal_row(row: dict) -> bool:
        """
        Does the CSV row have text in both wordform and category column?
        """
        if row['word'] and row['categories']:
            return True
        return False
