from .prompts import (
    prompt_direct_translate,
    prompt_cot_translate,
    prompt_cot_translate,
    prompt_dict_translate,
    prompt_fewshot_translate,
    prompt_fewshot_solve,
    prompt_dict_grammar_translate,
    prompt_system,
    extract_enclosed_text,
    prompt_gloss_translate,
    prompt_gloss_dict_translate,
    prompt_gloss_dict_grammar_translate,
    prompt_gloss_grammar,
    prompt_wordmap_translate,
    prompt_wordmap_grammar,
    prompt_gloss_translation_iter,
    prompt_gloss_grammar_iterative,
    prompt_zeroshot_cot,
    prompt_dict_grammar_solve,
    prompt_direct_solve,
)

import openai
import random
from .consts import OPENAI_API_KEY, DICT_CLASSES

def copy_prompt_translate(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    messages = [
        {"role": "system", "content": copy_prompt[0]["content"]},
        {"role": "user", "content": copy_prompt[1]["content"]},
    ]
    messages[1]["content"] = messages[1]["content"].replace("Please enclose your translation in ###",  'Please enclose your translation in ###.\nFor example, if your translation is "Hello world", the last part of your output should be ####Hello world###')
    messages[1]["content"] = messages[1]["content"].replace( "please translate the sentence into english and enclose your translation in ###",  'Please translate the sentence into english and enclose your translation in ###.\nFor example, if your translation is "Hello world", the last part of your output should be ###Hello world###')
    result = llm(messages)
    messages.append({"role": "assistant", "content": result})
    messages.append({"role": "user", "content": "So, what's your translation of the sentence? I want ONLY your translation. For example, if your translation is 'Hello world', your output should be ###Hello world###. Make sure to only output the translation"})
    messages.append({"role": "assistant", "content": "My translation is: ###"})
    result = llm(messages)
    messages[-1]['content'] = messages[-1]['content'] + result
    return extract_enclosed_text(messages[-1]['content'], boundary="###"), messages
    
    

def direct_translate(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_direct_translate(src_lang, tgt_lang, sent)}
    ]
    result = llm(messages)
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages
    
def copy_prompt_translate(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    messages = [
        {"role": "system", "content": copy_prompt[0]["content"]},
        {"role": "user", "content": copy_prompt[1]["content"]},
    ]
    messages[1]["content"] = messages[1]["content"].replace("Please enclose your translation in ###",  'Please enclose your translation in ###.\nFor example, if your translation is "Hello world", the last part of your output should be ####Hello world###')
    messages[1]["content"] = messages[1]["content"].replace( "please translate the sentence into english and enclose your translation in ###",  'Please translate the sentence into english and enclose your translation in ###.\nFor example, if your translation is "Hello world", the last part of your output should be ###Hello world###')
    result = llm(messages)
    messages.append({"role": "assistant", "content": result})
    messages.append({"role": "user", "content": "So, what's your translation of the sentence? I want ONLY your translation. For example, if your translation is 'Hello world', your output should be ###Hello world###. Make sure to only output the translation"})
    messages.append({"role": "assistant", "content": "My translation is: ###"})
    result = llm(messages)
    messages[-1]['content'] = messages[-1]['content'] + result
    return extract_enclosed_text(messages[-1]['content'], boundary="###"), messages
    
    

def direct_translate(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_direct_translate(src_lang, tgt_lang, sent)}
    ]
    result = llm(messages)
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages

def cot_translate(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_cot_translate(src_lang, tgt_lang, sent)}
    ]
    result = llm(messages)
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result, boundary="###"), messages

def direct_solve(src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    openai.api_key = OPENAI_API_KEY
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_direct_solve(src_lang, tgt_lang, sent)}
    ]
    completion = openai.ChatCompletion.create(
        model=MODEL_CKPT,
        messages=messages,
        top_p=0.5,
    )   
    result = completion.choices[0].message['content']
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages
    
def cot_translate(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_cot_translate(src_lang, tgt_lang, sent)}
    ]
    result = llm(messages)
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages

def direct_solve(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    openai.api_key = OPENAI_API_KEY
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_direct_solve(src_lang, tgt_lang, sent)}
    ]
    completion = openai.ChatCompletion.create(
        model=MODEL_CKPT,
        messages=messages,
        top_p=0.5,
    )   
    result = completion.choices[0].message.content
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages

def zeroshot_cot(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    openai.api_key = OPENAI_API_KEY
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_zeroshot_cot(src_lang, tgt_lang, sent)}
    ] 
    result = llm(messages)
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages

def fewshot_translate(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_fewshot_translate(src_lang, tgt_lang, sent, demo)}
    ]
    result = llm(messages)
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages

def fewshot_solve(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    openai.api_key = OPENAI_API_KEY
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_fewshot_solve(src_lang, tgt_lang, sent, demo)}
    ]
    result = llm(messages)
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages


def dict_translate(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    #import pdb; pdb.set_trace()
    openai.api_key = OPENAI_API_KEY
    vdict = DICT_CLASSES[f"{src_lang}-{tgt_lang}"]
    vdict = vdict(dict_fn, create_new_dict=False)
    words = sent.split()
    wordbyword = ""
    i = 0
    while i < len(words):
        if i + 1 < len(words):
            word = words[i] + " " + words[i + 1]
            if word == "tuttu oqi" or word == "uttu oqi" or word == "jetere jaka":   
                wres, key = vdict.match(word)
                if word == key:
                    wordbyword = wordbyword + word + ": " + wres + "\n"
                    i += 2
                    continue
        wres, key = vdict.match(words[i])
        wordbyword = wordbyword + "### " + words[i] + "\n" + wres + "\n"
        i += 1
    
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_dict_translate(src_lang, tgt_lang, demo, sent, wordbyword)}
    ]
    result = llm(messages)
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result, boundary="###"), messages


def dict_translate_mask(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    openai.api_key = OPENAI_API_KEY
    vdict = DICT_CLASSES[f"{src_lang}-{tgt_lang}"]
    vdict = vdict(dict_fn, create_new_dict=False)
    words = sent.split()
    wordbyword = ""
    i = 0
    mask_prob = 0.5
    while i < len(words):
        if i + 1 < len(words):
            word = words[i] + " " + words[i + 1]
            if word == "tuttu oqi" or word == "uttu oqi" or word == "jetere jaka":   
                wres, key = vdict.match(word)
                if "; parent: " in wres:
                    wres = wres.split("; parent: ")[0]
                if word == key:
                    if random.random() > mask_prob:
                        wordbyword = wordbyword + word + ": " + wres + "\n"
                    i += 2
                    continue
        if random.random() > mask_prob:
            wres, key = vdict.match(words[i])
            if "; parent: " in wres:
                wres = wres.split("; parent: ")[0]
            wordbyword = wordbyword + words[i] + ": " + wres + "\n"
        i += 1
    
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_dict_translate(src_lang, tgt_lang, sent, wordbyword)}
    ]
    completion = openai.ChatCompletion.create(
        model=MODEL_CKPT,
        messages=messages,
        top_p=0.5,
    )
    result = completion.choices[0].message['content']
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages

def dict_grammar_translate(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    openai.api_key = OPENAI_API_KEY
    vdict = DICT_CLASSES[f"{src_lang}-{tgt_lang}"]
    vdict = vdict(dict_fn, create_new_dict=False)
    words = sent.split()
    wordbyword = ""
    i = 0
    while i < len(words):
        if i + 1 < len(words):
            word = words[i] + " " + words[i + 1]
            if word == "tuttu oqi" or word == "uttu oqi" or word == "jetere jaka":             
                wres, key = vdict.match(word)
                if word == key:
                    wordbyword = wordbyword + word + ": " + wres + "\n"
                    i += 2
                    continue
        wres, key = vdict.match(words[i])
        wordbyword = wordbyword + words[i] + ": " + wres + "\n"
        i += 1
    
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_dict_grammar_translate(src_lang, tgt_lang, sent, wordbyword, grammar)}
    ]
    result = llm(messages)
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages

def wordmap_dict_translate(llm, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    openai.api_key = OPENAI_API_KEY
    vdict = DICT_CLASSES[f"{src_lang}-{tgt_lang}"]
    vdict = vdict(dict_fn, create_new_dict=False)
    words = sent.split()
    wordbyword = ""
    i = 0
    while i < len(words):
        subword = words[i].replace('-', ' ')
        wres = vdict.match(subword)
        if wres == "" or "Partial match:" in wres:
            subword = subword.split()
            for w in subword:
                wres = vdict.match(w)
                wordbyword = wordbyword + w + ": " + wres + "\n"
            for j, _ in enumerate(subword):
                wres = vdict.match(' '.join(subword[j:]))
                wordbyword = wordbyword + ' '.join(subword[j:]) + ": " + wres + "\n"
                j += 1
        else:
            wordbyword = wordbyword + words[i] + ": " + wres + "\n"
        #print(wordbyword)
        i += 1
    
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_dict_translate(src_lang, tgt_lang, sent, wordbyword)}
    ]
    result = llm(messages)
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages

def gloss_dict_translate(llm, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    openai.api_key = OPENAI_API_KEY
    vdict = DICT_CLASSES[f"{src_lang}-{tgt_lang}"]
    vdict = vdict(dict_fn, create_new_dict=False)
    words = sent.split()
    wordbyword = ""
    i = 0
    while i < len(words):
        subword = words[i].replace('-', ' ')
        wres = vdict.match(subword)
        if wres == "" or "Partial match:" in wres:
            subword = subword.split()
            for w in subword:
                wres = vdict.match(w)
                wordbyword = wordbyword + w + ": " + wres + "\n"
            for j, _ in enumerate(subword):
                wres = vdict.match(' '.join(subword[j:]))
                wordbyword = wordbyword + ' '.join(subword[j:]) + ": " + wres + "\n"
                j += 1
        else:
            wordbyword = wordbyword + words[i] + ": " + wres + "\n"
        i += 1
    
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_gloss_dict_translate(src_lang, tgt_lang, sent, gloss, wordbyword)}
    ]
    result = llm(messages)
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages

def gloss_dict_grammar_translate(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    openai.api_key = OPENAI_API_KEY
    vdict = DICT_CLASSES[f"{src_lang}-{tgt_lang}"]
    vdict = vdict(dict_fn, create_new_dict=False)
    words = sent.split()
    wordbyword = ""
    i = 0
    while i < len(words):
        subword = words[i].replace('-', ' ')
        wres = vdict.match(subword)
        if wres == "" or "Partial match:" in wres:
            subword = subword.split()
            for w in subword:
                wres = vdict.match(w)
                wordbyword = wordbyword + wres + "\n"
            for j, _ in enumerate(subword):
                wres = vdict.match(' '.join(subword[j:]))
                wordbyword = wordbyword + wres + "\n"
                j += 1
        else:
            wordbyword = wordbyword + wres + "\n"
        i += 1
    
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_gloss_dict_grammar_translate(src_lang, tgt_lang, sent, gloss, wordbyword, grammar)}
    ]
    result = llm(messages)
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages

def dict_grammar_translate(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    openai.api_key = OPENAI_API_KEY
    vdict = DICT_CLASSES[f"{src_lang}-{tgt_lang}"]
    vdict = vdict(dict_fn, create_new_dict=True)
    words = sent.split()
    wordbyword = ""
    i = 0
    while i < len(words):
        if i + 1 < len(words):
            word = words[i] + " " + words[i + 1]
            if word == "tuttu oqi" or word == "uttu oqi" or word == "jetere jaka":             
                wres, key = vdict.match(word)
                if word == key:
                    wordbyword = wordbyword + word + ": " + wres + "\n"
                    i += 2
                    continue
        wres, key = vdict.match(words[i])
        wordbyword = wordbyword + words[i] + ": " + wres + "\n"
        i += 1
    
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_dict_grammar_translate(src_lang, tgt_lang, sent, wordbyword, grammar)}
    ]
    result = llm(messages)
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages

def dict_grammar_solve(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    openai.api_key = OPENAI_API_KEY
    vdict = DICT_CLASSES[f"{src_lang}-{tgt_lang}"]
    vdict = vdict(dict_fn, create_new_dict=False)
    words = sent.split()
    wordbyword = ""
    i = 0
    while i < len(words):
        if i + 1 < len(words):
            word = words[i] + " " + words[i + 1]
            if word == "tuttu oqi" or word == "uttu oqi" or word == "jetere jaka":             
                wres, key = vdict.match(word)
                if word == key:
                    wordbyword = wordbyword + word + ": " + wres + "\n"
                    i += 2
                    continue
        wres, key = vdict.match(words[i])
        wordbyword = wordbyword + words[i] + ": " + wres + "\n"
        i += 1
    
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_dict_grammar_solve(src_lang, tgt_lang, sent, wordbyword, grammar)}
    ]
    completion = openai.ChatCompletion.create(
        model=MODEL_CKPT,
        messages=messages,
        top_p=0.5,
    )
    result = completion.choices[0].message['content']
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages

def wordmap_translate(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_wordmap_translate(src_lang, tgt_lang, sent, gloss)}
    ]
    result = llm(messages)
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages

def gloss_translate(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_gloss_translate(src_lang, tgt_lang, sent, gloss)}
    ]
    result = llm(messages)
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages

def gloss_translate_iter(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    openai.api_key = OPENAI_API_KEY
    assert iter is not None, "Iteration number must be specified"
    
    all_messages = []
    
    # first iteration
    
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_gloss_translate(src_lang, tgt_lang, sent, gloss)}
    ]
    completion = openai.ChatCompletion.create(
        model=MODEL_CKPT,
        messages=messages
    )   
    result = completion.choices[0].message['content']
    messages.append({"role": "system", "content": result})
    translation = extract_enclosed_text(result)
    all_messages.append(messages)
    
    for _ in range(1, iter):
        messages.append({"role": "user", "content": prompt_gloss_translation_iter(src_lang, tgt_lang, sent, gloss, translation)})
        completion = openai.ChatCompletion.create(
            model=MODEL_CKPT,
            messages=messages
        )   
        result = completion.choices[0].message['content']
        messages.append({"role": "system", "content": result})
        translation = extract_enclosed_text(result)
        all_messages.append(messages)
        
    return translation, all_messages

def gloss_grammar_translate(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    openai.api_key = OPENAI_API_KEY
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_gloss_grammar(src_lang, tgt_lang, sent, gloss, grammar)}
    ]
    result = llm(messages)
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages

def wordmap_grammar_translate(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter=None):
    openai.api_key = OPENAI_API_KEY
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_wordmap_grammar(src_lang, tgt_lang, sent, gloss, demo, grammar)}
    ]
    completion = openai.ChatCompletion.create(
        model=MODEL_CKPT,
        messages=messages
    )   
    result = completion.choices[0].message['content']
    messages.append({"role": "system", "content": result})
    return extract_enclosed_text(result), messages

def gloss_grammar_chapter_by_chapter_translate(llm, copy_prompt, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter):
    assert iter is not None, "Iteration number must be specified"
    assert iter == len(grammar) + 1, "Iteration number must be equal to the number of chapters plus one"
    openai.api_key = OPENAI_API_KEY
    
    all_messages = []
    
    # first iteration
    
    messages = [
        {"role": "system", "content": prompt_system(src_lang)},
        {"role": "user", "content": prompt_gloss_translate(src_lang, tgt_lang, sent, gloss)}
    ]
    completion = openai.ChatCompletion.create(
        model=MODEL_CKPT,
        messages=messages
    )   
    result = completion.choices[0].message['content']
    messages.append({"role": "system", "content": result})
    translation = extract_enclosed_text(result)
    all_messages.append(messages)
    
    for i in range(0, iter - 1):
        messages.append({
            "role": "user",
            "content": prompt_gloss_grammar_iterative(src_lang, tgt_lang, sent, gloss, translation,
                        chapter_name=grammar[i].split("\n")[0],
                        grammar=grammar[i].split("\n", 1)[1])})
        completion = openai.ChatCompletion.create(
            model=MODEL_CKPT,
            messages=messages
        )   
        result = completion.choices[0].message['content']
        messages.append({"role": "system", "content": result})
        translation = extract_enclosed_text(result)
        all_messages.append(messages)
        
    return translation, all_messages

PIPELINES = {
    "direct_translate": direct_translate,
    "direct_solve": direct_solve,
    "zeroshot_cot": zeroshot_cot,
    "cot_translate": cot_translate,
    "fewshot_translate": fewshot_translate,
    "fewshot_solve": fewshot_solve,
    "dict_translate": dict_translate,
    "dict_translate_mask": dict_translate_mask,
    "wordmap_dict_translate": wordmap_dict_translate,
    "gloss_dict_translate": gloss_dict_translate,
    "gloss_dict_grammar_translate" : gloss_dict_grammar_translate,
    "copy_prompt_translate": copy_prompt_translate,
    "dict_grammar_translate": dict_grammar_translate,
    "dict_grammar_solve": dict_grammar_solve,
    "gloss_translate": gloss_translate,
    "gloss_grammar_translate": gloss_grammar_translate,
    "gloss_translate_iter": gloss_translate_iter,
    "wordmap_translate": wordmap_translate,
    "wordmap_grammar_translate": wordmap_grammar_translate,
    "gloss_grammar_chapter_by_chapter_translate": gloss_grammar_chapter_by_chapter_translate,
}
