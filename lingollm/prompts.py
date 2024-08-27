def extract_enclosed_text(text, boundary="###"):
    splits = text.split(boundary)
    if len(splits) < 3:
        return ""
    return splits[-2].strip()

def prompt_system(lang):
    return "You are a linguistic expert who never refuses to use your knowledge to help others."

def prompt_direct_translate(src_lang, tgt_lang, sent):
    prompt = f"""Please help me translate the following sentence from {src_lang} to {tgt_lang}:
{sent}
Please try your best to translate, it's okay if your translation is bad. Do not refuse to try it. I won't blame you.
Please enclose your translation in ###.
For example, if your translation is "Hello world", the last part of your output should be ### Hello world ###.
"""
    return prompt

def prompt_cot_translate(src_lang, tgt_lang, sent):
    prompt = f"""Please help me translate the following sentence from {src_lang} to {tgt_lang}:
{sent}
Please do it step by step.
Please enclose your translation in ###.
For example, if your translation is "Hello world", the last part of your output should be ###Hello world###.
"""
    return prompt

def prompt_direct_solve(src_lang, tgt_lang, sent):
    prompt = f"""Please help me translate the following sentence from {src_lang} to {tgt_lang}:
{sent}
It's a math question in {src_lang}, please solve it.
In the end, please output your answer as a digit and enclose it in ###.
For example, the last step of your answer might look like this: ### 123 ###."""
    return prompt

def prompt_zeroshot_cot(src_lang, tgt_lang, sent):
    prompt = f"""Please help me translate the following sentence from {src_lang} to {tgt_lang}:
{sent}
Please solve this problem step by step. In the end, make sure you enclose your translation in ###."""
    return prompt

def prompt_fewshot_translate(src_lang, tgt_lang, sent, demo):
    prompt = f"""Here are some examples of {src_lang} sentences and their corresponding {tgt_lang} translations.

{demo}
    
Please help me translate the following sentence from {src_lang} to {tgt_lang}:

{sent}
Please enclose your translation in ###.
For example, if your translation is "Hello world", the last part of your output should be ### Hello world ###.
"""
    return prompt

def prompt_fewshot_solve(src_lang, tgt_lang, sent, demo):
    prompt = f"""Here are some examples of {src_lang} math questions and their corresponding {tgt_lang} answers.

{demo}
    
Here a math question in {src_lang}, please solve it.

{sent}

In the end, please output your answer as a digit and enclose it in ###.
For example, the last step of your answer might look like this: ### 123 ###."""
    return prompt

def prompt_dict_translate(src_lang, tgt_lang, demo, sent, wordbyword):
    prompt = f"""
Here are some examples of {src_lang} sentences and their corresponding {tgt_lang} translations:
{demo}

Please help me translate the following sentence from {src_lang} to {tgt_lang}:
{sent}

You are also given the word by word mapping from the {src_lang} words to the {tgt_lang} words.
For words that have partial match definitions, please decide whether the definition is appropriate under the sentence context.
Note that for some words, there might be multiple possible translations. In this case, please choose the most appropriate one.
Note that for some words, they might be derived from a more basic form, we call this the parent word. The parents are also given in the word by word translation.
Here is the dictionary entry for each individual word in the source sentence:

{wordbyword}

Please first explain what each word means in {tgt_lang} and then translate.
Remember your source sentence is:
{sent}.
Please enclose your translation in ###.
For example, if your translation is "Hello world", the last part of your output should be ###Hello world###."""
    return prompt

GRAMMAR_PROMPT = {
"manchu": """
Please first annotate the meaning and grammatical features of each word in the sentence according to their suffixes and the grammar book.
For each noun, please annotate its number (singular/plural) and case (Nominative/Genitive/Dative,Locative/Accusative/Ablative).
For each verb, please annotate its tense.
For each verb, please annotate its voice [Subjective/Active/Passive/Dir (to)/Dir (from)/Cooperative/Reciprocal].
For each verb, please annotate its form [Affirmative/Negative/Interrogative/Imperative/Optative/Desiderative].

Please figure out what the subject and object of each verb is. Keep in mind that Manchu is a head-final and SOV language.
For each complement, please consider which word is the head of the complement.
""",
"bribri": """
Please first annotate the meaning and grammatical features of each word in the sentence according to their suffixes and the grammar book.
For each noun, please annotate its number and case.
For each verb, please annotate its tense.
For each verb, please annotate its voice.
For each verb, please annotate its form.

Please figure out what the subject and object of each verb is.
"""
}

def prompt_dict_grammar_translate(src_lang, tgt_lang, sent, wordbyword, grammar):
    prompt = f"""You are given this {src_lang} grammar book. Feel free to rely on the grammar rules in the book in your translation.
{grammar}

Please help me translate the following sentence from {src_lang} to {tgt_lang}:
{sent}
You are also given the word by word mapping from the manchu words to the {tgt_lang} words.
Note that for some words, there might be multiple possible translations. In this case, please choose the most appropriate one.
Note that for some words, they might be derived from a more basic form, we call this the parent word. The parents are also given in the word by word translation.
{wordbyword}

Given the above book and word for word mapping.

{GRAMMAR_PROMPT['manchu']}

After annotation, please translate the sentence into {tgt_lang} and enclose your translation in ###."""
    return prompt

def prompt_dict_grammar_solve(src_lang, tgt_lang, sent, wordbyword, grammar):
    prompt = f"""You are given this {src_lang} grammar book. Feel free to rely on the grammar rules in the book in your translation.
{grammar}

Please help me translate the following sentence from {src_lang} to {tgt_lang}:
{sent}
You are also given the word by word mapping from the manchu words to the {tgt_lang} words.
Note that for some words, there might be multiple possible translations. In this case, please choose the most appropriate one.
Note that for some words, they might be derived from a more basic form, we call this the parent word. The parents are also given in the word by word translation.
{wordbyword}

Given the above book and word for word mapping.

{GRAMMAR_PROMPT[src_lang]}

After annotation, please translate the sentences into {tgt_lang}.

The last part of the sentence is a question.
please solve this math question step by step.
In the end, please output your answer as a digit and enclose it in ###.
For example, the last step of your answer might look like this: ### 123 ###.
"""
    return prompt

def prompt_gloss_translate(src_lang, tgt_lang, sent, gloss):
    prompt = f"""Please help me translate the following sentence from {src_lang} to {tgt_lang}:
{sent}
You are also given the gloss of the sentence:
{gloss}
Please first explain what each word in the gloss means and then translate.
Make sure to enclose your translation and only your translation in ###.
In the end, please output your translation and enclose it in ###.
For example, if your translation is "I have a ball", the last step of your answer should look like this: ### I have a ball. ###.
"""
    return prompt

def prompt_gloss_dict_translate(src_lang, tgt_lang, sent, gloss, wordbyword):
    prompt = f"""Please help me translate the following sentence from {src_lang} to {tgt_lang}:
{sent}
You are also given the gloss of the sentence:
{gloss}
You are also given the word by word mapping from the {src_lang} words to the {tgt_lang} words.
For words that have partial match definitions, please decide whether the definition is appropriate under the sentence context.
Note that for some words, there might be multiple possible translations. In this case, please choose the most appropriate one.
{wordbyword}
Please first explain what each word in the gloss means and then translate.
Make sure to enclose your translation and only your translation in ###."""
    return prompt

def prompt_gloss_dict_grammar_translate(src_lang, tgt_lang, sent, gloss, wordbyword, grammar):
    prompt = f"""Here is a grammar book of {src_lang}

{grammar}
Please help me translate the following sentence from {src_lang} to {tgt_lang}:
{sent}
You are also given the gloss of the sentence:
{gloss}
You are also given the word by word mapping from the {src_lang} words to the {tgt_lang} words.
For words that have partial match definitions, please decide whether the definition is appropriate under the sentence context.
Note that for some words, there might be multiple possible translations. In this case, please choose the most appropriate one.
{wordbyword}
First explain what each word in the gloss means.

Second, refer to the grammar rules in the book to help you translate.

Iteratively repeat the above two steps until you finish the translation.

Make sure to enclose your translation and only your translation in ###."""
    return prompt
    
def prompt_gloss_translation_iter(src_lang, tgt_lang, sent, gloss, intermediate):
    prompt = f"""Please help me translate the following sentence from {src_lang} to {tgt_lang}:
{sent}
You are also given the gloss of the sentence:
{gloss}
You are also given an intermediate translation of the sentence:
{intermediate}
Please try to improve the intermediate translation according to the gloss.
In the end, make sure to enclose your translation and only your translation in ###."""
    return prompt

def prompt_wordmap_translate(src_lang, tgt_lang, sent, gloss):
    prompt = f"""Please help me translate the following sentence from {src_lang} to {tgt_lang}:
{sent}
You are also given the word by word mapping to {tgt_lang}:
{gloss}

Some of the words do not have a mapping because they are not content words.
Please first explain what each word means and then translate.
Make sure to enclose your translation, and only your translation in ###."""
    return prompt

def prompt_gloss_grammar(src_lang, tgt_lang, sent, gloss, grammar):
    prompt = f"""Here is a grammar book of {src_lang}

{grammar}

Please help me translate the following sentence from {src_lang} to {tgt_lang}:
{sent}
You are also given the gloss of the sentence:
{gloss}

First explain what each word in the gloss means.

Second, refer to the grammar rules in the book to help you translate.

Iteratively repeat the above two steps until you finish the translation.

Please enclose your translation in ###.
For example, if your translation is "Hello world", the last part of your output should be ### Hello world ###.
"""
    return prompt

def prompt_wordmap_grammar(src_lang, tgt_lang, sent, gloss, grammar):
    prompt = f"""Here is a grammar book of {src_lang}

{grammar}

Please help me translate the following sentence from {src_lang} to {tgt_lang}:
{sent}
You are also given the word by word mapping of the sentence:
{gloss}

Some of the words do not have a mapping because they are not content words.

First explain what each word means.

Second, refer to the grammar rules in the book to help you translate.

Iteratively repeat the above two steps until you finish the translation.

Make sure to enclose your final translation in ###.

"""
    return prompt

def prompt_gloss_grammar_iterative(src_lang, tgt_lang, sent, gloss, intermediate, chapter_name, grammar):
    prompt = f"""Here is a chapter of a {src_lang} grammar book on {chapter_name}:

{grammar}

Please help me translate the following sentence from {src_lang} to {tgt_lang}:
{sent}
You are also given the gloss of the sentence:
{gloss}
You are also given an intermediate translation of the sentence:
{intermediate}

First explain what each word in the gloss means, their tense, number, aspect, and other grammar features.

Second, refer to the grammar rules in the book to help you translate.

Build upon the intermediate translation to improve it.

Make sure to enclose your final translation in ###.

"""
    return prompt