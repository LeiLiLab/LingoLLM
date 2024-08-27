import re
import json
import os

from . import helpers, ilg_helpers, STEM_PAT
from .builder import FomaBuilder
from .foma_reader import FomaReader


class ParserError(Exception):
    pass


proj_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

BASIC_E = os.path.join(proj_root, 'fst/basic_east.json')
BASIC_EW = os.path.join(proj_root, 'fst/basic_dialectal.json')
FULL_E = os.path.join(proj_root, 'fst/full_east.json')
FULL_EW = os.path.join(proj_root, 'fst/full_dialectal.json')

class Parser():
    """
    Skeleton class for FST in foma. Compiles lexc and foma files
    and captures output. By default, constructs and loads the fullest 
    FST version (includes east/west variation, functional items).

    load_input = path to a foma file or json configuration file
                default: 'fst/full_dialectal.json'
    """

    def __init__(self, load_input: str or dict = FULL_EW) -> None:
        print(load_input)
        self.reload(load_input)
    
    def reload(self, load_input: str or dict) -> None:

        if type(load_input) is dict:
            foma_location, bin_location = self._build(load_input)
        elif type(load_input) is str and load_input[-5:] == '.foma':
            foma_location, bin_location = load_input, None
        elif type(load_input) is str and load_input[-5:] == '.json':
            with open(load_input) as f:
                load_input = json.load(f)
            foma_location, bin_location = self._build(load_input)
        else:
            raise ParserError('Unknown file type provided for foma file')
        
        # TODO: validate to make sure foma location exists/is file

        self._reader = FomaReader(foma_location, bin_location)
        self.analyzer_dict = {}
        self.generator_dict = {}

    def analyze(self, query: str, gloss_validator: str = None) -> list:
        """
        Input a surface wordform; returns list of possible analyses.
        Saves wordforms to internal dictionary if not already present.
        """
        query = helpers.convert_to_underscore(query)

        if gloss_validator:
            # triggers one self-referential lookup without validators
            full_result = self.analyze_properties(query, gloss_validator)
            return full_result['validated']

        # base case for analyze and analyze_properties recursive lookup
        if query not in self.analyzer_dict:
            self.analyzer_dict[query] = self._reader.lookup(query)
        return self.analyzer_dict[query]
    
    def analyze_to_ilg(self, query: str) -> list:
        """
        Input a surface wordform; returns list of possible analyses
        converted to their nearest equivalent as seen in the 
        interlinear gloss format used by the Gitksan lab.
        Stems are given as ___ rather than as a one-word definition.
        """
        fst_output = self.analyze(query)
        converted = [ilg_helpers.fst_to_story_gloss(res, STEM_PAT) 
                    for res in fst_output]
        return helpers.unique(converted)

    def generate(self, query: str) -> list:
        """
        Input a foma analysis; returns list of possible surface 
        wordforms. Saves analyses to an internal dictionary.
        """
        if query not in self.generator_dict:
            result_list = self._reader.lookup(query, inverse=True)
            result_list = [helpers.convert_to_lowline(item)
                            for item in result_list]
            self.generator_dict[query] = result_list
        return self.generator_dict[query]

    def lemmatize(self, form: str) -> list:
        """
        Input a word, returns a list of lists of tuples. Each sublist is
        a possible breakdown of the word; each tuple references an 
        identified lemma in the word and its category.
        Returns None if no breakdowns/lemmas can be identified.
        Compound forms have multiple tuples:
            e.g. [("form", "A"), ("form", "B")]
        Forms where multiple variants can be generated are split 
        with slashes within the first tuple element:
            e.g. ("form/Form", "X")
        """
        parses = self.analyze(form)
        if not parses: return None

        # for each possible parse, find all stem+category strings
        stem_options = [re.findall(STEM_PAT, p) for p in parses]
        unique_options = helpers.unique(stem_options)
        
        # convert each stem string to a tuple of (surface forms, CAT)
        results = []
        for option in unique_options:
            option = [self._analysis_to_lemma_tuple(stem) for stem in option]
            if option and option not in results:
                results.append(option)

        if results:
            return sorted(results)
    
    def analyze_properties(self, word: str, gloss_validator: str = None) -> dict:
        """
        Input a surface wordform and optional validation string.
        Returns a dictionary holding properties of the string and its
        output after running through the analyze (foma: apply up) 
        function. Also holds information about validated output upon
        comparison with optionally supplied validator strings.
        Dictionary keys:
            - input (surface wordform: str)
            - output (analyses returned by FST: list of str)
            - *valid_gloss (analyses filtered by gloss_validator:
                            list of str)
            - *valid_gloss_scored (analyses filtered by gloss_validator
                                    with their validation score,
                                    list of 2-tuples (str, num))
        """
        result = {'input': word}
        output = self.analyze(word)
        result['output'] = output
        
        if output:
            if gloss_validator:
                res = ilg_helpers.filter_matching_glosses(output, 
                                    gloss_validator)
                result['valid_gloss_scored'] = res
                result['valid_gloss'] = [text for text, score in res]
                result['validated'] = result['valid_gloss'].copy()
        
        # has a superset of options and 1 or 2 possible validated options via different criteria
        # want to output:
            # if 2 validated options: only their overlapping contents
            # if 1 validated option: return that list
            # else, don't make validated list
        
        # if gloss input only, and has 4 options, return those 4
        # if gloss input with 0, return empty list
        # if segment input only, and has 2 options, return those 2
        # if gloss input with 4, and segment input with 2, and the 2 overlap, return all 2
        # if gloss input with 4, and segment input with 2, and only 1 overlaps, return the 1
        # if gloss input with 4, and segment input with 2, and no overlaps, return empty list
        # if gloss input with 4, and segment input with 0, return empty list

        return result
    
    def pairs(self) -> list:
        """
        Calls foma to run 'pairs', generating the last 100 listed pairs.
        Reads the foma output and stores as a list of up to 100 2-tuples
        in the format: (analysis, surfaceform).
        """
        result = self._reader.query('pairs')
        return self._reader.format_foma_pairs(result)

    def random_pairs(self) -> list:
        """
        Calls foma to run 'random-pairs', generating random pairs.
        Returns a list of up to 100 tuple pairs.
        """
        result = self._reader.query('random-pairs')
        return self._reader.format_foma_pairs(result)

    def random_unique_pairs(self, limit: int = 50) -> list:
        """
        Calls foma to run 'random-pairs', and stores unique results
        up to the limit specified. May take a while since only 100 items
        can be queried at a time and foma may return duplicates.
        Extended system usage prohibited by a timeout limit calculated
        by the number of forms queried; throws a ParserError.
        """
        if limit >= self._reader.paths:
            raise ParserError(
                '{} random pairs requested, but {} available'.format(
                    limit, self._reader.paths))

        sample_pairs = []
        result = []
        counter = 0
        while len(result) < limit:
            if not sample_pairs:
                counter += 1
                sample_pairs = self.random_pairs()
            item = sample_pairs.pop()
            if item not in result:
                result.append(item)
            
            if counter > (round(limit/3) + 1):
                raise ParserError('Timeout: ' +
                    '{} unique random items could not be found.'.format(limit))
        
        return list(result)
    
    def _build(self, config: dict) -> tuple:
        """
        Constructs a new foma file from configuration dictionary.
        Returns a tuple of the new foma filepath and binary filepath.
        """
        builder = FomaBuilder(config)
        builder.build()
        return (builder.foma_filepath(), builder.fomabin_filepath())

    def _analysis_to_lemma_tuple(self, analysis_str: str) -> tuple:
        """
        Takes a string corresponding to a single stem generated from 
        the FST parser ('upper' form). Outputs a 2-tuple consisting of:
            - the generated form (with variants separated by slashes)
            - the category abbreviation for that form
            e.g. 'cat+N' -> ('cat/Cat', 'N')
        """
        forms = self.generate(analysis_str)
        pat = r"\+([A-Z]+)"  # finds partofspeech abbreviation
        abbrev = re.search(pat, analysis_str).group(1)
        if forms and abbrev:
            surface_forms = "/".join(sorted(helpers.unique(forms)))
            return (surface_forms, abbrev)
        elif abbrev == 'DEM':
            if 'PROX' in analysis_str:
                surface_forms = '-un'
            else:
                surface_forms = '-ust'
            return (surface_forms, abbrev)
