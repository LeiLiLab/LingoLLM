import re
from . import STEM_PAT


def fst_to_story_gloss(fst_gloss: str) -> str:
    """ 
    Input a gloss from the FST to convert it approximately to how it
    would look in the Gitksan interlinear gloss format used in stories.
    Instead of a definition for main stems, an empty '___' is used.
        - fst_gloss: string output from the parser
    """
    new_gloss = fst_gloss
    # morpheme/tag replacements: fst style as key, story form as value
    replacements = {
        "n$ee+AUX": 'NEG',
        "y$ukw+AUX": 'PROG',
        "d$im+MOD": 'PROSP',
        "j$i+MOD": 'IRR',
        "j$i+SUB": 'IRR',
        "w$il+SUB": 'COMP',
        "w$in+SUB": 'COMP',
        "'$ii+SUB": 'CCNJ',
        "w$ila+SUB": 'MANR',
        "hl$aa+SUB": 'INCEP',
        "hl$is+SUB": 'PERF',
        "k_'$ap+MDF": 'VER',
        "'$ap+MDF": 'VER',
        "g_$an+MDF": 'REAS',
        "g_$ay+MDF": 'CONTR',
        "'$alp'a+ADV": 'RESTR',
        "hind$a+ADV": 'WH',
        "nd$a+ADV": 'WH',
        "'$a+P": 'PREP',
        "g_$o'o+P": 'LOC',
        "g_$oo+P": 'LOC',
        "g_$a'a+P": 'LOC',
        "g_an+CNJ": 'PCNJ',
        "'$ii+CNJ": 'CCNJ',
        "'$oo+CNJ": 'or',
        "=YNQ": '=Q',
        "+PRO": '',
        "+OP": '',
    }
    for fst_ver, ilg_ver in replacements.items():
        new_gloss = new_gloss.replace(fst_ver, ilg_ver)
    # specific replacements where fst and story breakdowns differ
    new_gloss = re.sub(r"(\w+)\+OBL", r"OBL-\1.II", new_gloss)
    new_gloss = re.sub(r"(\w+)\+DEM", r"DEM.\1", new_gloss)
    if '+QUOT' in new_gloss:
        new_gloss = re.sub(r"(\d)SG\+QUOT", r"\1.I=QUOT", new_gloss)
        new_gloss = re.sub(r"3PL\+QUOT", r"3.I=QUOT.3PL", new_gloss)
        new_gloss = re.sub(r"(\d)PL\+QUOT", r"\1.I=QUOT.PL", new_gloss)
    # replace various stems with '___'
    new_gloss = re.sub(STEM_PAT, '___', new_gloss)
    return new_gloss

def filter_matching_glosses(analyses: list, story_gloss: str) -> list:
    """
    Given a list of FST analyses and an interlinear/story gloss to 
    validate against, this function returns a subset of the FST analyses
    which possibly match the validator as a list. If one analysis is 
    an exact match, that item will be the only element in the returned
    list. Any analyses which are not feasible matches are filtered out.
    The remaining analyses are sorted by match goodness.
    """
    options = {}
    for analysis in analyses:
        approximation = fst_to_story_gloss(analysis)
        score = match_score(approximation, story_gloss)

        if score == 1:
            return [(analysis, score)]
        elif score:
            options[analysis] = score

    # return list(options.items())
    return sorted(options.items(), reverse=True, 
                    key=lambda pair: options[pair[0]])

def match_score(converted_gloss: str, story_gloss: str) -> int:
    """
    Given a FST output analysis converted to its closest interlinear
    equivalent, and an actual interlinear gloss string, this function
    provides a numeric score from 0 to 1 indicating how likely the two
    gloss strings are to be a match. 0 = no match, 1 = exact match.
    Floats between 0 and 1 can be used to sort match goodness.
    """
    if converted_gloss == story_gloss:
        # find exact match
        return 1
    else:
        # reject analysis with no match when using simple wildcard

        # remove brackets around -T/-TR in story string
        story_gloss = re.sub(r'\[(-TR?)', r'\1', story_gloss)
        story_gloss = re.sub(r'(-TR?)\]', r'\1', story_gloss)

        pattern = re.sub('___', '.+', re.escape(converted_gloss))
        if not re.match(pattern, story_gloss):
            return 0

    # otherwise, generate score based on number of fst morphemes
    # that match morphemes in ilg gloss (reject if not found)
    score = 0.5

    fst_morphs = re.split(r'[\-=~\[\]\(\)<>]+', converted_gloss)
    ilg_morphs = re.split(r'[\-=~\[\]\(\)<>]+', story_gloss)

    # refactor if we need to consider duplicate morphemes (TODO)
    for morph in fst_morphs:
        if morph in ilg_morphs:
            # TODO: this can generate a score above 1 if enough matches
            score *= 1.15
        elif morph == '___':
            score *= 0.95
        else:
            score = 0
            break
    
    return round(score, 3)
