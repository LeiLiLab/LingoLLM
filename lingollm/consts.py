from .vdict import (
    Manchu_VDict,
    Bribri_VDict,
    EnDinka_VDict,
    Dinka_VDict,
    Gitksan_VDict,
    #EnGitksan_VDict,
    Arapaho_VDict,
    EnArapaho_VDict,
    WolofDict,
)

import os

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

DICT_CLASSES = {
    "manchu-english": Manchu_VDict,
    "bribri-spanish": Bribri_VDict,
    "english-dinka": EnDinka_VDict,
    "dinka-english": Dinka_VDict,
    "gitksan-english": Gitksan_VDict,
    #"english-gitksan": EnGitksan_VDict,
    "arapaho-english": Arapaho_VDict,
    "english-arapaho": EnArapaho_VDict,
    "wolof-english": WolofDict,
}

MANCHU_GRAMMAR = """All Manchu phrases are head-final; the head-word of a phrase (e.g. the noun of a noun phrase, or the verb of a verb phrase) always falls at the end of the phrase. Thus, adjectives and adjectival phrases always precede the noun they modify, and the arguments to the verb always precede the verb. As a result, Manchu sentence structure is subject–object–verb (SOV).

Manchu uses a small number of case-marking particles that are similar to those found in Korean, but there is also a separate class of true postpositions. Case markers and postpositions can be used together, as in the following sentence:

> bi tere niyalma-i emgi gene-he
> 
> 
> I that person-GEN with go-PST
> 
> I went with that person
> 

In this example, the postposition **emgi**, "with", requires its nominal argument to have the genitive case, which causes the genitive case marker **i** between the noun **niyalma** and the postposition.

Manchu also makes extensive use of converb structures and has an inventory of converbial suffixes to indicate the relationship between the subordinate verb and the finite verb that follows it. An example is these two sentences, which have finite verbs:

> tere sargan boo qi tuqi-ke
> 
> 
> that woman house ABL go out-PST.FIN
> 
> That woman came out of the house
> 

> tere sargan hoton de gene-he
> 
> 
> that woman town DAT go-PST.FIN
> 

Both sentences can be combined into a single sentence by using converbs, which relate the first action to the second:

> tere sargan boo qi tuqi-fi, hoton de gene-he
> 
> 
> that woman house ABL go out-PST.CVB, town DAT go-PST.FIN
> 
> That woman, having come out of the house, went to town.
> 

> tere sargan boo qi tuqi-me, hoton de gene-he
> 
> 
> that woman house ABL go outp-IMPERF.CVB, town DAT go-PST.FIN
> 
> That woman, coming out of the house, went to town.
> 

> tere sargan boo qi tuqi-qibe, hoton de gene-he
> 
> 
> that woman house ABL go out-CONC.CVB, town DAT go-PSF.FIN
> 
> That woman, though she came out of the house, went to town
> 

### Cases

Manchu has five cases, which are marked by particles: nominative, accusative, genitive, dative-locative, and ablative. The particles can be written with the noun to which they apply or separately. They do not obey the rule of vowel harmony but are also not truly postpositions.

**Manchu Pronoun Cases**

|  | Nominative | Accusative | Genitive | Dative | Ablative |
| --- | --- | --- | --- | --- | --- |
| 1st SG | bi | mimbe | mini | minde | minqi |
| 2nd SG | si | simbe | sini | sinde | sinqi |
| 3rd SG | i | imbe | ini | inde | inqi |
| 1st PL inclusive | muse | musebe | musei | musede | museqi |
| 1st PL exclusive | be | membe | meni | mende | menqi |
| 2nd PL | suwe | suwembe | suweni | suwende | suwenqi |
| 3rd PL | qe | qembe | qeni | qende | qenqi |

### Nominative

One of the principal syntactic cases, it is used for the subject of a sentence and has no overt marking.

### Accusative

(*be*): one of the principal syntactic cases, it indicates participants/direct object of a sentence. Direct objects sometimes also take the nominative. It is commonly felt that the marked accusative has a definite sense, like using a definite article in English. It is written separate from the word that it follows. The accusative can be used in the following ways:

- Nominative-accusative strategy – indicates opposition between syntactic roles (subject = nominative; object – accusative)
    
    > i boo be weile-mbi
    > 
    > 
    > he house ACC build-IMPERF
    > 
    > "he builds a house"
    > 
- transitive verbs
    
    > fe kooli be dahame yabu-mbi
    > 
    > 
    > old regulations ACC [according.to](http://according.to/) act-IMPERF
    > 
- Transitive verb (negative form)
- Indicate when agent is caused to perform an action
- Indicate motion that is happening

### Genitive

(*i* or *ni*): one of the principal syntactic cases, it is used to indicate possession or the means by which something is accomplished.

Its primary function is to indicate the possessor of an object:

> boo i ejen
> 
> 
> house GEN master
> 
> the master of the house
> 

It can also indicate a person's relationships:

> han i jui
khan GEN child
the khan's child
> 

Other functions of genitive are:

- Attributive: nouns followed by genitive marker indicate attributives, which are also used for participles and verbs.
- Adverb: the noun is repeated with the addition of the genitive marker (i)

**Dative-locative**

(*de*): indicates location, time, place, or indirect object.

Its primary function is to indicate the semantic role of the recipient:

> ere niyalma de bu-mbi
> 
> 
> this man DAT give-IMPERF
> 
> "(someone) gives to this man"
> 

It also has other functions:

- Agent of a passive verb
- Indicate person who is in possession of something
- Indicate sources of something
- Indicate instrument of action (verbs in past tense, talking about others)

### Ablative

(*qi*): indicates the origin of an action or the basis for a comparison

That can be the starting point in space or time:

> boo-qi tuqi-ke
House-ABL go.away-PAST
> 
> 
> (Someone) went away from the house
> 

It can also be used to compare objects:

> ere erin qi oyonggo ningge akv
> 
> 
> this time ABL important NLMZ COP.NEG
> 

### Verbs

There are 13 basic verb forms, some of which can be further modified with the verb *bi* (is), or the particles *akv, i, o,* and *ni* (negative, instrumental, and interrogatives).

**Conjugation of the verb** *afa-* **(to attack)**

| Form | Usual Suffix | Example |
| --- | --- | --- |
| imperative | ∅ | afa |
| imperfect participle | -ra/re/ro | afara |
| perfect participle | -ha/he/ho | afaha |
| imperfect converb | -me | afame |
| perfect converb | -fi | afafi |
| conditional | -qi | afaqi |
| concessive | -qibe | afaqibe |
| terminal converb | -tala/tele/tolo | afatala |
| prefatory converb | -nggala/nggele/nggolo | afanggala |
| desiderative 1 | -ki | afaki |
| desiderative 2 | -kini | afakini |
| optative | -qina | afaqina |
| temeritive | -rahv | afarahv |

### Imperfect Participle

The imperfect participle is formed by adding the variable suffix *-ra, -re, -ro* to the stem of the verb. *Ra* occurs when the final syllable of the stem contains an *a*. *Re* occurs when the final syllable of the stem contains *e*, *i*, *u* or *v*. *Ro* occurs with stems containing all *o*'s. An irregular suffix *-dara, -dere, -doro* is added to a limited group of irregular verbs (*jon-, wen-, ban-*) with a final *-n*. (The perfect participle of these verbs is also irregular). Three of the most common verbs in Manchu also have irregular forms for the imperfect participle:

- *bi-, bisire* — 'be'
- *o-, ojoro* — 'become'
- *je-, jetere* — 'eat'

Imperfect participles can be used as objects, attributes, and predicates. Using *ume* alongside the imperfect participle makes a negative imperative.

As an attribute:

> habša-ra niyalma
> 
> 
> complain-IPC man
> 

When this form is used predicatively it is usually translated as a future tense in English; it often carries an indefinite or conditional overtone when used in this fashion:

> bi sinde alara
> 
> 
> 1sg 2sg-ACC tell-IPTC
> 

As an object:

> gisure-re be han donji-fi
> 
> 
> speak-IPTC ACC king hear-PCVB
> 
> "The king having heard what was being said"
>"""

GRAMMARS = {
    "Manchu": MANCHU_GRAMMAR,
}

arapaho_morphology = """
1. Initial Change: Verbal stems undergo initial change to indicate present/present perfect tense when there is no preceding element. When preverbs or other elements precede the verb stem, no initial change is indicated.

2. Person and Number Inflection: Verb stems are obligatorily marked for person and number. AI verbs use suffixes -noo (1S), -n (2S), -t (3S), -ni’ (PL), etc. TA verbs use suffixes like -é3en (1S/2S), -oot (3S/4), -owoo (1S), etc. TI verbs use -owoo (1S), -ow (2S), -o’ (3PL), etc.

3. Obviation: In Arapaho, animate nouns can be inflected for the obviative (4th person), which is used to distinguish between two third persons in a discourse. The obviative is indicated by suffixes such as -owuní3 (4S), -owuní3i (4PL), etc.

4. Possession: Possession is indicated by prefixes for the possessor and suffixes for plural possessors and objects. Examples include ne-/he-/i- for 1S/2S/3S possessors, and -no’ (singular object) and -nínoo (plural object or possessor).

5. Locative: The locative suffix /(v)’/ is added to noun stems to indicate location.

6. Detachment Construction: This construction uses the suffix /ini/ to detach preverbs or initials from verb stems without affecting initial change but maintaining the morphosyntactic integrity of the verb.

7. Reduplication: Reduplication is used to express multiple objects, repetitive/iterative action, extension, and habitual action. It involves adding /:n/ to the first syllable of a stem and creating a reduplicated form.

8. Preverbs and Verb Initials: Preverbs and initials are added to verb stems to modify their meaning, such as indicating direction, intensity, or other adverbial notions. When used as preverbs, consonant-final roots take a derivational /-i/, and vowel-final roots take /:n/ to form initials.

9. Denominalizations: Nouns can be turned into verbs by adding verb finals, with /ini/ for 'have as a . . .' and /éee/ for 'gathering/producing'.

10. Proclitics: Proclitics are attached to the beginning of phrases and indicate various grammatical functions such as interrogation, intensity, and aspect. They precede tense markers and do not inhibit initial change.

11. Aspectual, Auxiliary, Qualifiers, Quantifiers, Intensifiers, and Delimiters: These are preverbs/initials that indicate aspect (e.g., /béet/ for finishing), ability (e.g., /X-ni’/ for 'able to'), quantity (e.g., /bee3/ for 'a lot'), intensity (e.g., /tes/ for 'very'), and spatial/temporal relationships (e.g., /nih-/ for past tense).

12. Derivation from Verbs to Nouns and Nouns to Verbs: Verb stems can be turned into nouns using suffixes like /(i)hííh/ for agentive or patient nominalizations. Nouns can be transformed into verbs using finals such as /iini/ for the 'to be a . . .' construction or /éee/ for the gathering/producing construction.

13. Concrete Finals: These are finals added to verb stems that include a lexical root and an abstract final. They often express transitive action involving a physical transformation of a patient.

14. Medials: Lexical roots inserted between the verb's initial and its final. Medials typically represent topics like body parts or common objects that are affected by the verbal action.

15. Direction and Location Preverbs/Initials: A wide range of stems indicate direction or location, such as /cei(t)/ 'to here', /noow/ 'downward', /iini3/ 'around and continuing', etc. They can combine with abstract directionals like /ii3/.

16. Time Preverbs/Initials: Stems expressing time concepts like /benii’ow/ 'spring', /tousebi/ 'to bathe', etc., often become part of verb stems to indicate timing of the action.

17. Manner Preverbs/Initials: These express the manner of actions like /beebii3/ 'straight/correctly', /nihi’(nee)/ 'quickly', etc.

18. Auxiliaries and Modals: Some preverbs function like auxiliary verbs in English, expressing modal meanings. For example, /béétoh/ means 'want to', and /no’/ is used to express completion or arrival.

19. Negative Construction: The negative construction uses the negative marker /ihoowu/, which is a preverb that precedes the verb stem to negate the action.

20. Deictic Directional Preverbs: The preverbs /cih/ (to speaker) and /eh/ (from speaker) are specifically deictic and used to encode spatial and temporal deixis. They appear immediately after tense markers and before other preverbs or verb stems.

21. Reduplicative Forms: Some stems in Arapaho only exist in a reduplicated form, expressing iterative or spatially/temporally extended actions, such as /nonookéí/ 'soar'.

22. Derivation of Additional Preverbs and Verb Initials: New preverbs or initials can be created from independent verbs or nouns. When used as initials, derivational elements are added, such as final /:n/ for vowel-final stems.

23. Verb Stem Structure: Arapaho verb stems typically contain an initial and a final element. The initial provides the main lexical content, and the final indicates the verb stem class—whether the verb is AI, II, TA, or TI—and contributes additional semantic content, such as aspect or manner of action.

24. Pronominal Prefixes: Arapaho verb stems take pronominal prefixes to indicate person and number directly on the verb. These prefixes include forms like ne- (1S), he- (2S), and hi- (3S). When prefixes are combined with verb stems, phonological rules apply, like addition of epenthetic /t/ for vowel-initial verb stems or consonant mutation.

25. Obviative Prefixes: Additional pronominal prefixes indicate obviation. They are used to differentiate two third persons, marking one as more peripheral to the discourse (the obviative) than the other (the proximate).

26. Inverse Marking: Arapaho verbs can include morphology that inverses the hierarchy of animacy and agency, which allows the language to flexibly mark the subject and object based on discourse salience rather than purely grammatical or semantic roles.

27. Independent vs. Dependent Stems: Some verb stems are "dependent" in that they cannot stand alone and require other verbal elements or qualifiers. Dependent stems often correspond to secondary actions or states of another verb or noun, e.g., modifiers like 'sing well' or 'dance energetically'.

28. Intransitive Motion Verbs: Intransitive motion verbs emerge from certain finals that inherently involve motion, such as /see/ 'go' and /koohu/ 'run'. These verbs are often AI or II and may be modified by directional initials.

29. Reflexive Verbs: Reflexive verbs are constructed using finals like /eti/, indicating that subjects both perform and receive the action. For example, /betee3etí/ means 'to dance reflexively or with one another'.

30. Medial Consonant Drop: As with noun initials, when creating verb initials from independent verbs, initial consonants are typically dropped if they are /b/, /w/, or /n/.

31. Causative Constructions: Causative forms of verbs are created with finals like /owuun/ (to cause an action for someone's benefit) or /h/ (general causative), turning intransitive verbs into transitive ones with causative meaning.

32. Transitive Verbs with Indirect Objects: Many transitive verbs in Arapaho can take indirect objects in addition to the direct object, expanding the valency of the verb.

33. Augmented States: Arapaho verbs can incorporate elements that elevate the intensity or state of the action or quality, such as reduplication for iterative action or specific augmentative preverbs for heightened states.

34. Complex Verb Stems with Compounding: Verb stems can be compounded with multiple modifiers such as directional, locational, and aspectual elements, creating complex stems that express intricate semantic nuances.

35. Morphophonemic Changes: Verb stems and prefixes undergo various morphophonemic adjustments when combined. These include alterations such as vowel harmony adjustments, consonant mutations, and epenthetic insertions, which affect the pronunciation and sometimes the meaning of the verb stem.

"""