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

An example output is in `data/manchu/outputs/direct_Aug27_0811_53`.

**Manchu Few-Shot Translation**

```bash
python gen.py --src manchu --tgt english --pipeline fewshot_translate --work_dir manchu --input_fn laoqida.in --dict_name manchu_dict_laoqida_new.db --demo manchu.demo --llm gpt-4o-2024-08-06
```

An example output is in `data/manchu/outputs/fewshot_Aug27_0815_06`.

**Manchu Dictionary Only Translation**

```bash
python gen.py --src manchu --tgt english --pipeline dict_translate --work_dir manchu --input_fn laoqida.in --dict_name manchu_dict_laoqida_new.db --demo manchu.demo --llm gpt-4o-2024-08-06
```

**Manchu Dictionary + Grammar Translation**

Paper: https://arxiv.org/abs/2402.18025


