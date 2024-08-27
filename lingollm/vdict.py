import shelve
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import re
from typing import Optional, List
import editdistance # pip install editdistance
from thefuzz import fuzz, process # pip install thefuzz
import spacy
import fst_src
import json
import subprocess

class VDict:
    def __init__(self, filename, initial_words: Optional[List]=None, create_new_dict=False):
        self.filename = filename
        self.db = shelve.open(filename, flag='n' if create_new_dict else 'c', writeback=create_new_dict)
        if initial_words is not None:
            for key, value in initial_words:
                self.db[key] = value
    
    def dict_match(self, key):
        if key in self.db:
            return self.db[key]
        self.db[key] = self.real_match(key)
        return self.db[key]
    
    def real_match(self, key):
        raise NotImplementedError
    
    def sync(self):
        self.db.sync()

class Manchu_VDict(VDict):
    def __init__(self, filename, initial_words: Optional[List]=None, wait_time=3, create_new_dict=False):
        super().__init__(filename, initial_words, create_new_dict)
        self.driver = None
        self.wait_time = wait_time
    
    def real_match(self, key):
        if self.driver is None:
            self.driver = webdriver.Chrome()
        self.driver.get("https://buleku.org/home")
        search_box = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div/div/div/div/input')
        search_box.send_keys(Keys.COMMAND + "a")
        search_box.send_keys(Keys.BACK_SPACE)
        search_box.send_keys(key)
        time.sleep(self.wait_time)
        
        try:
            no_res = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div/div/div/h6/span')
        except NoSuchElementException:
            pass
        else:
            return None
        
        try:        
            first_entry = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div/div/div/div')
        except NoSuchElementException:
            return None
        first_entry.click()
        time.sleep(self.wait_time)
        
        word_form = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/header/div/div/div/div/h6').text
        if not key.startswith(word_form) and not word_form.startswith(key):
            return None
        
        first_result = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div/div[1]/div/div/ul/li[1]/div')
        res = first_result.text
        
        try:
            parent = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div/div[1]/div/div/ul/span/li/div/p/span/a').text
        except NoSuchElementException:
            pass
        else:
            parent_res, pkey = self.match(parent)
            res = word_form + " - " + res + f"; parent: {pkey}" + parent_res
            
        
        # dict_name = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div/div[1]/div/div/div/button/span[1]').text
        
        # if dict_name != 'CMED':
        #     print(f"Wrong dictionary, {dict_name}!")
        
        return res
    
    def match(self, key):
        if key[0].isupper():
            return "{key} is a person's given name: {key}", key
        if key == "wangging":
            return "the capital of Korea", key
        if key == "diyanhvwa":
            return "noun. phone, telephone", key
        if key == "fi":
            return "noun. Pen, pencil", key
        if key == "bithesa":
            return "books (plural)", key
        if key == "g'angfi":
            return "fountain pen (Chin.)", key
        if key == "qi":
            return "(comparative participle) than; (ablative participle) from, by way of", key
        if key == "oho":
            return "o-ho (perfect participle) of ombi; ombi: 1. to become, to change into 2. to be, to exist 3. to be proper, to be permissible", key
        while len(key) > 0:
            res = self.dict_match(key)
            if res is not None:
                return res, key
            key = key[:-1]
        return "", ""


class WolofDict(VDict):
    def __init__(self, filename, initial_words: Optional[List]=None, create_new_dict=False):
        super().__init__(filename, initial_words, create_new_dict)
        self.vdict = json.load(open("data/wolof/new_Wollof2En.dict.json", "r"))
    
    def match(self, query):
        query = query.lower()
        
        keys = list(self.vdict.keys())
        keys = sorted(keys, key=lambda x: editdistance.eval(query, x))
        
        res = ""
        for k in keys[:3]:
            res += f"{k}: {self.vdict[k]};\n"
        
        return res, query


bribri_specials = "ôö̂òö̀óö́èë̀éë́éë́âä̂àä̀áä́ûü̂ùǜúǘîï̂ìï̀íḯêë̂ÉË́'"
class Bribri_VDict(VDict):
    def __init__(self, filename, initial_words: Optional[List]=None, create_new_dict=False):
        super().__init__(filename, initial_words, create_new_dict)
        self.driver = None
        self.wait_time = 0.1
        
    def dict_match(self, key):
        return self.match(key)
    
    def normalize(self, key):
        return ''.join([c if c != "'" else "’" for c in key])
    
    def real_match(self, key):
        key = self.normalize(key)
        
        if key in self.trace:
            return ""
        
        self.trace.add(key)
        if self.driver is None:
            self.driver = webdriver.Chrome()
            self.driver.get("https://www.haakonkrohn.com/bribri/bri-esp.html")
        driver = self.driver
        
        search_box = driver.find_element(By.XPATH, '//*[@id="campoBuscar"]')
        
        # clear the search box
        search_box.send_keys(Keys.COMMAND + "a")
        search_box.send_keys(Keys.BACK_SPACE)
        # search for a non-existent word
        search_box.send_keys(key)
        
        search_btn = driver.find_element(By.XPATH, '//*[@id="botónBuscar"]')
        search_btn.click()
        
        entries = driver.find_elements(By.CLASS_NAME, 'resultado')
        
        if entries == []:
            return ""
        
        
        entries = sorted(entries, key=lambda x: editdistance.eval(key, x.text) + (key[0] == x.text[0]) * (-2))
        entry = entries[0]
        entry.click()
        
        articulo = driver.find_element(By.XPATH, '//*[@id="artículo"]')
        lines = articulo.text.split('\n')[1:] # remove the first line which is the word itself
        lines = [line for line in lines if not line.startswith('Fuentes: ')]
        meaning = '\n'.join(lines) + "\n"
        
        pars = driver.find_elements(By.CLASS_NAME, 'enlace')
        pars = [par.text for par in pars]
        if pars != []:
            # import pdb; pdb.set_trace()
            for par in pars:            
                parent_res = self.real_match(par)
                meaning += f"{par}: {parent_res}; \n"

        return meaning
    
    def match(self, key):
        self.trace = set()
        
        is_bribri = False
        for c in bribri_specials:
            if c in key:
                is_bribri = True
                
        if not is_bribri:
            if "q" in key or "f" in key or "g" in key:
                return f"Non-bribri word, might be spanish or english {key}", key

        original_len = len(key)
        while len(key) > 0:
            meaning = self.real_match(key)
            if meaning != "":
                if original_len > len(key) * 2:
                    return f"Partial match, might be a non-bribri word: {key}: {meaning}", key
                return meaning, key
            key = key[:-1]
        
        return "", key 

class Dinka_VDict(VDict):
    def __init__(self, filename, initial_words: Optional[List]=None, create_new_dict=False):
        super().__init__(filename, initial_words, create_new_dict)

    def real_match(self, key):
        return None

    def match(self, key):
        final_res = ''
        key = key.lower()
        res = res1 = self.dict_match(key)
        if res != None:
          final_res += res
          return final_res
        for i in range(0,len(key)):
          subword1 = key[:i] + '-'
          res1 = self.dict_match(subword1.strip())
          prefix = False
          for j in range(0,len(key)):
            subword2 = key[i:len(key)-j]
            subword3 = '-' + key[-j:]
            if i > (len(key)-j):
              break
            res2 = self.dict_match(subword2.strip())
            res3 = self.dict_match(subword3.strip())
            if res2 is not None and i != 0 and j != 0 and res3 is not None and j != len(key) and j!= 0:
                final_res += '\n' + subword2 + ':' + res2
                final_res += '\n' + subword3 + ':' + res3
                prefix = True
          if res1 is not None and i != 0 and i != len(key) and prefix:
                final_res += '\n' + subword1 + ':' + res1
        return final_res

class EnDinka_VDict(VDict):
    def __init__(self, filename, initial_words: Optional[List]=None, create_new_dict=False):
        super().__init__(filename, initial_words, create_new_dict)

    def real_match(self, key):
        return None

    def match(self, key):
        final_res = ''
        key = key.lower()
        res = self.dict_match(key)
        if res is not None:
          final_res += res
        return final_res

class Gitksan_VDict(VDict):
    def __init__(self, filename, initial_words: Optional[List]=None, create_new_dict=False):
        super().__init__(filename, initial_words, create_new_dict)

    def normalize(self, key):
        return ''.join([c if c != "'" else "’" for c in key])

    def partial_match(self, key):
        key = self.normalize(key)
        fuzz_matches = process.extract(key, self.db.keys(), scorer=fuzz.ratio)
        least_distance = float('inf')
        match = []
        for m in fuzz_matches:
            dis = editdistance.eval(key, m[0])
            match.append((m[0], m[1], dis))
        #print(match)
        match = sorted(match, key=lambda x: (x[2], -x[1]))
        matches = []
        for m in match:
            matches.append('Partial match: '+ m[0] + str(self.db[m[0]]))
        return matches
    
    def match(self, key):
        key = self.normalize(key)
        if key in self.db:
            return self.db[key]
        return self.partial_match(key)
        
class EnGitksan_VDict(VDict):
    def __init__(self, filename, initial_words: Optional[List]=None, create_new_dict=False):
        super().__init__(filename, initial_words, create_new_dict)
        self.driver = None
        self.nlp = spacy.load('en_core_web_sm')
        
    def match(self, key):
        self.trace = set()
        lemmatized_word = self.nlp(key)[0].lemma_.lower()
        return self.dict_match(lemmatized_word)
        
    def real_match(self, key):
        if self.driver == None:
            service = Service(executable_path='./chromedriver')
            options = webdriver.ChromeOptions()
            self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get("https://www.firstvoices.com/gitsenimx/search?q=&domain=both&types=word%2Cphrase%2Csong%2Cstory&sort=")
        time.sleep(10)
        lemmatized_word = self.nlp(key)[0].lemma_.lower()
        search_box = self.driver.find_element(By.ID, "SearchInput")
        search_box.clear()
        search_box.send_keys(lemmatized_word)
        search_box.submit()
        self.driver.implicitly_wait(30)
        time.sleep(10)
        res = ""
        try:
            entries = self.driver.find_elements(By.ID, "EntryDetails")
            possible_match=[]
            for e in entries:
                entry = e.text.replace('Play audio', '').strip().split('\n')
                word = entry[0]
                translation = ' '.join(entry[1:])
                possible_match.append((translation, word))
            possible_match = sorted(possible_match, key=lambda x: editdistance.eval(lemmatized_word, x[0]))
            if len(possible_match) > 0:
                i = 0
                for m in possible_match:
                    if lemmatized_word not in m[0].lower():
                        continue
                    if i == 5 or i == len(possible_match):
                        break
                    res += "(" + str(i+1) + ")" + m[0] + ":" + m[1] + ' '
                    i += 1
        except NoSuchElementException:
            return None
        return res


class Arapaho_VDict(VDict):
    def __init__(self, filename, initial_words: Optional[List]=None, wait_time=3, create_new_dict=False):
        super().__init__(filename, initial_words, create_new_dict)
        self.driver = None
        self.wait_time = wait_time
        self.fst = fst_src.Parser('./arapahoverbs.foma')

    def match(self, key):
        self.trace = set()
        return self.dict_match(key)
    
    def real_match(self, key):
        fst_result = self.fst.analyze(key)
        if not (len(fst_result) == 1 and fst_result[0] == '???'):
            stem = re.sub('[\[].*?[\]]', '', fst_result[0])
            key = stem
        if self.driver == None:
            service = Service(executable_path='./chromedriver')
            options = webdriver.ChromeOptions()
            self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get("https://verbs.colorado.edu/arapaho/public/view_search")
        language_select = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="language"][value="arapaho"]')[0]
        if not language_select.is_selected():
            language_select.click()
        search_box = self.driver.find_element("name", "search_string")
        search_box.clear()
        search_box.send_keys(key)
        search_box.submit()
        self.driver.implicitly_wait(self.wait_time)
        possible_match = []
        try:
            result = self.driver.find_element(By.ID, "search_results_view")
            word_entries = result.find_elements(By.CSS_SELECTOR, 'ul li')
            possible_match = []
            for entry in word_entries:
                word = entry.text.split(' ')[0]
                possible_match.append((word, ' '.join(entry.text.split(' ')[1:])))
            possible_match = sorted(possible_match, key=lambda x: editdistance.eval(key, x[0]))
            best_match = possible_match[0]
            if not (len(fst_result) == 1 and fst_result[0] == '???'):
                regex_pattern = r'\[([^\]]+)\]\[([^\]]+)\]'
                match = re.search(regex_pattern, fst_result[0])
                if match:
                    part_of_speech = (match.group(1)[0]+match.group(2)).lower()
                    print(part_of_speech)
                for match in possible_match:
                    if '('+part_of_speech+')' in match[1]:
                        best_match = match
                        break
            
            if best_match[0] == key:
                dict_result = best_match[1]
            else:
                dict_result = 'Partial match: ' + best_match[0] + ': ' + best_match[1]
            if not (len(fst_result) == 1 and fst_result[0] == '???'):
                return fst_result[0] + dict_result
            else:
                return dict_result
        except NoSuchElementException:
            return None

class EnArapaho_VDict(VDict):
    def __init__(self, filename, initial_words: Optional[List]=None, wait_time=3, create_new_dict=False):
        super().__init__(filename, initial_words, create_new_dict)
        self.driver = None
        self.wait_time = wait_time
        #self.fst = fst_src.Parser('./arapahoverbs.foma')

    def match(self, key):
        self.trace = set()
        return self.dict_match(key)
    
    def real_match(self, key):
        if self.driver == None:
            service = Service(executable_path='./chromedriver')
            options = webdriver.ChromeOptions()
            self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get("https://verbs.colorado.edu/arapaho/public/view_search")
        search_box = self.driver.find_element("name", "search_string")
        search_box.clear()
        search_box.send_keys(key)
        search_box.submit()
        self.driver.implicitly_wait(self.wait_time)
        possible_match = []
        exact_match = []
        try:
            result = self.driver.find_element(By.ID, "search_results_view")
            word_entries = result.find_elements(By.CSS_SELECTOR, 'ul li')
            possible_match = []
            for entry in word_entries:
                word = entry.text.split(' ')[0]
                translation =  ' '.join(entry.text.split(' ')[1:])
                if key in translation:
                    possible_match.append((word, translation))
                if ("\""+key+"\"") in translation:
                    exact_match.append((word, translation))
            if len(exact_match) != 0:
                dict_result = ""
                for m in exact_match:
                    dict_result += m[0] + ":" + m[1]
                return dict_result
            possible_match = sorted(possible_match, key=lambda x: editdistance.eval(key, x[0]))
            if len(possible_match) == 0:
                return ""
            best_match = possible_match[0]
            
            if best_match[1] == key:
                dict_result = best_match[0]
            else:
                dict_result = 'Partial match: ' + best_match[0] + ': ' + best_match[1]

            return dict_result
        except NoSuchElementException:
            return ""

class Shipibo_VDict(VDict):
    def __init__(self, filename, initial_words: Optional[List]=None, wait_time=3, create_new_dict=False):
        super().__init__(filename, initial_words, create_new_dict)
        self.driver = None

    def match(self, key):
        self.trace = set()
        return self.dict_match(key)
        
    def real_match(self, key):
        fst_outputs = subprocess.check_output('echo '+key+' | flookup morph_shk.fst', shell=True).decode('utf-8').split('\n')
        res = ""
        for output in fst_outputs:
            if output == '':
                continue
            root = key
            if '+?' not in output:
                pattern =  r'\b(\w+)\[.*Root.*\]'
                match = re.search(pattern, output)
                if match:
                    print(match.group(1))
                    root = match.group(1)
            print("output", output, ", root: ", root)
            if self.driver == None:
                service = Service(executable_path='./chromedriver')
                options = webdriver.ChromeOptions()
                self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.get("https://diccionario.nonjoi.org/")
            self.driver.implicitly_wait(30)
            search_box = self.driver.find_element(By.ID, "query_box")
            search_box.clear()
            search_box.send_keys(root)
            search_box.send_keys(Keys.ENTER)
            self.driver.implicitly_wait(30)
            part_res = "gloss:" + output + ", root word translation:"
            try:
                possible_match = []
                table = self.driver.find_element(By.CLASS_NAME, "table-striped")
                rows = table.find_elements(By.TAG_NAME, "tr")
                for r in rows:
                    columns = r.find_elements(By.TAG_NAME, "td")
                    if len(columns) == 2:
                        word = columns[0].text
                        translation = columns[1].text
                        possible_match.append((word, translation))
                possible_match = sorted(possible_match, key=lambda x: editdistance.eval(root, x[0]))
                i = 0
                for m in possible_match:
                    if i == 5 or i == len(possible_match):
                        break
                    part_res += "(" + str(i+1) + ")" + m[0] + ":" + m[1] + ' '
                    i += 1
                if len(possible_match) == 0:
                    part_res = ""
            except NoSuchElementException:
                pass
            res += part_res
            print(output, 'part_res: ', part_res)
        return res

class Uspanteko_VDict(VDict):
    pass

class Natugu_VDict(VDict):
    pass