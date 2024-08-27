# LingoLLM

### Installation

```bash
conda create -n lingollm python=3.11
conda activate lingollm
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Running LingoLLM

`gen.py` is the main script to run LingoLLM. It has the following arguments:

- `--src`: Source language
- `--tgt`: Target language
- `--pipeline`: Translation pipeline (direct_translate, fewshot_translate, ...)
- `--work_dir`: Working directory, by default we use the low resource language name as the working directory
- `--input_fn`: Input file name in source language. Each line is a sentence.
- `--dict_name`: Dictionary cache path for the source language
- `--demo`: In-context demonstration file name in the working directory
- `--llm`: LLM model name, check `llms.py` to see the available models and add your own favorite ones

Now let's see some examples.

### LingoLLM on Manchu as an example

**Manchu Zero-Shot Translation**

```bash
python gen.py --src manchu --tgt english --pipeline direct_translate --work_dir manchu --input_fn laoqida.in --dict_name manchu_dict_laoqida_new.db --demo manchu.demo --llm gpt-4o-2024-08-06
```

Takes about 3 minutes to run on my machine. An example output is in `data/manchu/outputs/direct_Aug27_1834_01`.

**Manchu Few-Shot Translation**

```bash
python gen.py --src manchu --tgt english --pipeline fewshot_translate --work_dir manchu --input_fn laoqida.in --dict_name manchu_dict_laoqida_new.db --demo manchu.demo --llm gpt-4o-2024-08-06
```

Takes about 3 minutes to run on my machine. An example output is in `data/manchu/outputs/fewshot_Aug27_1837_57`.

**Manchu Dictionary Only Translation**

```bash
python gen.py --src manchu --tgt english --pipeline dict_translate --work_dir manchu --input_fn laoqida.in --dict_name manchu_dict_laoqida_new.db --demo manchu.demo --llm gpt-4o-2024-08-06
```

Takes about 15 minutes to run on my machine. An example output is in `data/manchu/outputs/dict_Aug27_1819_34`.

Note that this command utilizes the dictionary cache `manchu_dict_laoqida_new.db` to translate the input sentences.

To create the dictionary yourself, you can change the name of the dictionary and run the same command.
Since we use selenium to manipulate chrome in searching for words on buleku.org, you need to make sure that the chrome driver is installed on your machine.

### To Contribute

### TODOs

**To be released**

- [ ] Data and evaluation scripts for other languages in the paper
- [ ] Better readme for more pipelines

**To be added**

- [ ] Batched LLM call for faster inference
- [ ] Make it more flexible for more languages
- [ ] Migrate to LiteLLM / other more universal LLM call interfaces

...

### Cite Us

```
@inproceedings{zhang-etal-2024-hire,
    title = "Hire a Linguist!: Learning Endangered Languages in {LLM}s with In-Context Linguistic Descriptions",
    author = "Zhang, Kexun  and
      Choi, Yee  and
      Song, Zhenqiao  and
      He, Taiqi  and
      Wang, William Yang  and
      Li, Lei",
    editor = "Ku, Lun-Wei  and
      Martins, Andre  and
      Srikumar, Vivek",
    booktitle = "Findings of the Association for Computational Linguistics ACL 2024",
    month = aug,
    year = "2024",
    address = "Bangkok, Thailand and virtual meeting",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.findings-acl.925",
    pages = "15654--15669",
}
```


