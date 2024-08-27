import os
import re

from .lexicon import Lexicon


class BuilderError(Exception):
    pass


class FomaBuilder:
    """
    Class to orchestrate building a foma file from a configuration dict.
    Uses a dictionary to locate components of lexc files and foma rules;
    then splits and copies these files, writing them to a single 
    .foma file at the specified location.
    """

    def __init__(self, config: dict) -> None:
        self._validate_config_file(config)
        self.config = config
        self._set_directory()

    def build(self) -> None:
        """
        Builds lexc/foma files as specified with config settings from 
        input dict. Writes both files to dir 'foma/' inside specified 
        containing directory as listed in config dictionary.
        If no container dir specified, writes to '../fst/foma'.
        """
        target_path = os.path.join(self.config['dir'], 'foma')
        if not os.path.exists(target_path):
            os.mkdir(target_path)

        self._build_lexc()
        self._build_foma()

    def lexc_filepath(self) -> str:
        """
        Generates the path from which to write the main lexc file.
        Based on the configured directory and project name.
            e.g. configdir/foma/projname.txt
        """
        return os.path.join(self.config['dir'], 'foma', 
                            self.config['name'] + '.txt')

    def foma_filepath(self) -> str:
        """
        Generates the path from which to write the main foma file.
        Based on the configured directory and project name.
            e.g. configdir/foma/projname.foma
        """
        return os.path.join(self.config['dir'], 'foma',
                            self.config['name'] + '.foma')

    def fomabin_filepath(self) -> str:
        """
        Generates the path from which to write the foma binary file.
        Based on the configured directory and project name.
            e.g. configdir/foma/projname.fomabin
        """
        return os.path.join(self.config['dir'], 'foma',
                            self.config['name'] + '.fomabin')

    def _build_lexc(self) -> None:
        """
        Builds a lexc file from all specified files in lexc directory.
        File has three chunks: multicharacter symbols, lexicon/stems, 
        morphotactic descriptions.
        Calls orchestrator commands to write the lexc info to file.
        """
        self._build_dictionary()
        self._build_morph_description()

        with open(self.lexc_filepath(), 'w') as f:
            f.write(self._multichar_symbs)
            f.write(self._stems)
            f.write(self._morphotactics + '\n')

    def _build_dictionary(self) -> None:
        """
        Calls orchestrator commands to write a Lexicon object to
        text, for inclusion in the lexc file. Saved to a variable
        on the Builder object.
        """
        self._stems = Lexicon(self.config).as_lexc_str()

    def _build_morph_description(self) -> None:
        """
        Reads lexc component files to store the multicharacter symbols
        and morphological description component of the lexc output.
        These chunks are saved to variables on the Builder object.
        """

        multichar_symbs = ''
        morphotactics = []

        # read/process files in lexc directory
        for file in self.config['lexc_files']:
            with open(os.path.join(self.config['dir'], file)) as f:
                content = f.read()

            # split multichar symbols from morphotactic description
            chunks = content.split('\n\n', 1)
            header = chunks[0]
            if '\n' in header:
                multichar_symbs += header.split('\n', 1)[1] + '\n'
            morphotactics.append(chunks[1])
            
        self._morphotactics = '\n\n'.join(morphotactics)

        # clean up the multicharacter symbols
        self._build_multichars(multichar_symbs)

    def _build_multichars(self, text: str) -> None:
        """
        Input a chunk of text with a collection of multicharacter 
        symbols each on newlines. Sorts and alphabetizes all unique
        symbols, and provides a lexc header and footer.
        Saves text to a variable on the Builder object.
        """
        symbols = text.split('\n')
        symbols = sorted(set(symbols) - set(['']))
        new_text = '\n'.join(symbols)

        self._multichar_symbs = 'Multichar_Symbols\n' + new_text + '\n\n'

    def _build_foma(self) -> None:
        """
        Builds a foma file from all specified files listed in config.
        Calls orchestrator commands to read the component files,
        sets up header/footer, and writes foma file.
            foma written to: "specified_directory/foma/name.foma"
            bin set up to: "specified_directory/foma/name.fomabin"
        """
        self._build_rules()

        header = "read lexc {}\ndefine Lexicon ;".format(self.lexc_filepath())
        footer = "save stack {}".format(self.fomabin_filepath())

        with open(self.foma_filepath(), 'w') as f:
            f.write(header + '\n\n')
            f.write(self._rules + '\n\n')
            f.write(footer)

    def _build_rules(self) -> None:
        """
        Reads rules files, removes stem variation section unless 
        dialect_variation parameter in config dictionary set to True.
        """

        self._rules = ''
        for file in self.config['rules_files']:
            with open(os.path.join(self.config['dir'], file)) as f:
                self._rules += f.read()

        if not self.config.get('dialect_variation'):
            lines = self._rules.splitlines()
            valid_lines = []
            delete_toggle = False
            for line in lines:
                if re.search(r'! (end )?stem variation', line):
                    delete_toggle = not delete_toggle
                    continue
                if delete_toggle:
                    continue
                valid_lines.append(line)
            self._rules = '\n'.join(valid_lines)

    @staticmethod
    def _validate_config_file(config: dict) -> None:
        """
        Ensures that config dictionary input to the Builder object
        contains the required name, lexc, and rules components.
        """
        required_keys = ['name', 'lexc_files', 'rules_files']
        for key in required_keys:
            if not config.get(key):
                raise BuilderError('Key {} not found in config file')

    def _set_directory(self) -> None:
        """
        Sets the directory to which file read/write will proceed
        if not explicitly set.
        Default read/write is relative to project dir: '../fst'
        Test read/write is relative to test subdir: '../test/fixtures'
        """
        if not self.config.get('dir'):
            if self.config.get('test'):
                dir = os.path.join(
                    os.path.dirname(__file__), '../test/fixtures')
            else:
                dir = os.path.join(os.path.dirname(__file__), '../fst')
            self.config['dir'] = os.path.abspath(dir)
