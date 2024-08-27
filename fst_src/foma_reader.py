import os
import subprocess
import re


class FomaError(Exception):
    pass


class FomaReader():
    """
    Orchestrator object to interact with the foma subprocess.
    Takes a foma file and optional foma binary file as input.
    Runs the foma file and returns its output; lookup queries can 
    be made via flookup if a binary file is provided.
    """

    def __init__(self, foma_file: str, bin_file: str = None) -> None:
        self._fomafile = foma_file
        self._binfile = bin_file
        self._validate()
        self._load()

    def query(self, command: str, raw: bool = False) -> str:
        """
        Runs foma as a subprocess and returns the output of query.
        """
        foma = subprocess.Popen(['foma'],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True
                                )

        try:
            command = 'source {}\n{}'.format(self._fomafile, command)
            outs, errs = foma.communicate(command)
        except subprocess.TimeoutExpired:
            foma.kill()
            outs, errs = foma.communicate()
            raise FomaError("Timeout...\nOutput: \n{}Errors:\n{}".format(outs,
                                                                        errs))
        
        if raw:
            return outs
        else:
            return self._format_foma_output(outs)
    
    def lookup(self, query: str, inverse: bool = False) -> list:
        """
        Runs foma 'apply up/down' or calls flookup to find the other
        side of a given query. Returns output as a list of strings.
            Default / inverse False = apply up (parse/analyze)
            Reverse / inverse True = apply down (generate)
        """
        if self._binfile:
            result = self._flookup(query, inverse)
            return self._flookup_as_list(result)
        else:
            command = 'apply up\n' if not inverse else 'apply down\n'
            result = self.query(command + query)
            return self._format_applyx_as_list(result)

    def _flookup(self, query: str, inverse: bool) -> str:
        """
        Using the specified bin file, runs the flookup utility
        (inverted if desired) and returns the output string.
        """
        command = ["flookup", '-x', self._binfile]
        if inverse:
            command.insert(2, '-i')

        try:
            echo = subprocess.Popen(["echo", query], stdout=subprocess.PIPE)
            flookup = subprocess.Popen(command,
                                       stdin=echo.stdout,
                                       stdout=subprocess.PIPE,
                                       text=True)
            echo.stdout.close()

            output, err = flookup.communicate()
        finally:
            echo.kill()
            echo.wait()
            flookup.kill()
            flookup.wait()
        
        return output

    def _load(self) -> None:
        """
        Runs the foma compilation and stores the its state/arc/path
        figures. If none output, raises an error; else saves these
        figures to variables stored in the FomaReader.
        Parses any foma warnings and prints them to console.
        """
        raw_foma = self.query(None, raw=True)

        # needs testing -- not sure if it displays warnings yet
        warnings = re.findall('(Warning: .*)', raw_foma)
        for w in warnings:
            print(w)

        fst_info = re.findall("(\d+) states?, (\d+) arcs?, (\d+) paths?.", raw_foma)
        # needs testing
        if fst_info:
            self.states, self.arcs, self.paths = (int(n) for n in fst_info[-1])
        else:
            raise FomaError("Your foma file did not compile a machine!")
        
        if not self._binfile and not self._seek_binfile(raw_foma):
            print('Warning: no binary file for this compilation; lookups are slow.')

    def _validate(self) -> None:
        """
        Ensures that input foma and bin paths lead to valid files.
        If foma file is invalid, raises an error.
        If bin file is invalid, the reference is deleted.
        An alternate bin location is sought from foma output on load.
        """
        if not os.path.exists(self._fomafile):
            raise FileNotFoundError('Cannot find foma file: {}'.format(self._fomafile))
        if self._binfile and not os.path.exists(self._binfile):
            self._binfile = None

    def _seek_binfile(self, foma_output: str) -> bool:
        """
        Attempts to read the location for a binary file for this 
        foma compilation based on the text output when loading foma. 
        Saves location to the object if the file exists.
        Returns a boolean of whether a binary file is ultimately found.
        """
        bin_text = re.findall("Writing to file (\S+).", foma_output)
        if bin_text:
            bin_text = bin_text[-1]
            if os.path.exists(bin_text):
                self._binfile = bin_text
            else:
                foma_dir = os.path.dirname(self._fomafile)
                binfile = os.path.join(foma_dir, bin_text)
                if os.path.exists(binfile):
                    self._binfile = binfile
        
        return True if self._binfile else False
    
    @staticmethod
    def format_foma_pairs(text: str) -> list:
        """
        Formats text output from a foma 'pairs' command as a
        nice list of tuples. Removes empty lines.
        """
        return [tuple(item.split("\t"))
                for item in text.splitlines()
                if item.strip() != '']

    @staticmethod
    def _format_foma_output(text: str) -> str:
        """
        Formats text output from foma as a nice text block.
        Removes the initial blob from loading foma.
        """
        # remove output from loading foma
        text = text.split('foma[1]:')[1]
        # remove the line with the command that was called
        text = text.split('\n', 1)[1]
        return text.strip()

    @staticmethod
    def _format_applyx_as_list(text: str) -> list:
        """
        Formats text output from foma 'apply up/down' as a list
        of the output lines. Strips the apply up/down query and prompt.
        """
        return text.splitlines()[1:-1]

    @staticmethod
    def _flookup_as_list(text: str) -> list:
        """
        Formats the output of the flookup process as a list.
        Removes empty analyses.
        """
        return [item for item in text.splitlines()
                if item and item != '+?']

