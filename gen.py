import argparse
from lingollm.pipelines import PIPELINES
import os
from datetime import datetime
import json
import shutil
import glob
from tqdm import tqdm
from lingollm.llms import get_llm_wrapper

parser = argparse.ArgumentParser(description='Generate translation')
parser.add_argument('--src', type=str, help='source language', required=True)
parser.add_argument('--tgt', type=str, help='target language', required=True)
parser.add_argument('--gloss_fn', type=str, help='gloss', required=False)
parser.add_argument('--pipeline', choices=PIPELINES.keys(), help='generation pipeline', required=True)
parser.add_argument('--work_dir', type=str, help='working directory, like `gitksan`', required=True)
parser.add_argument('--input_fn', type=str, help='input filename, like `dev.in`', required=True)
parser.add_argument('--dict_name', type=str, help='dictionary filename, like `gitksan_dict.db`', required=True)
parser.add_argument('--output_dir', type=str, default=None, help='output directory, like `direct`')
parser.add_argument('--grammar_fn', type=str, default=None, help='grammar file name')
parser.add_argument('--iter', default=None, type=int, help='iteration number')
parser.add_argument('--demo', type=str, default="", help='demo examples', required=False)
parser.add_argument("--llm", type=str, default="", help="LLM model id", required=True)
parser.add_argument("--start", type=int, default=0, help="Start from line")
parser.add_argument("--copy_prompt", type=str, default="", help="the output directory to copy prompts from", required=False)



def check_dirs(args):
    work_dir = args.work_dir
    input_fn = args.input_fn
    dict_fn = args.dict_name
    output_dir = args.output_dir
    pipeline_name = args.pipeline
    src_lang = args.src
    tgt_lang = args.tgt
    
    if not os.path.exists(f'data/{work_dir}'):
        print(f"Working directory data/{work_dir} does not exist!")
        exit(1)
    
    if not os.path.exists(f'data/{work_dir}/{input_fn}'):
        print(f"Input file data/{work_dir}/{input_fn} does not exist!")
        exit(1)
    
    # if not os.path.exists(f'data/{work_dir}/{dict_fn}'):
    #     print(f"Dictionary data/{work_dir}/{dict_fn} does not exist!")
    #     exit(1)
    
    if output_dir is None:
        output_dir = pipeline_name
        if output_dir.endswith('_translate'):
            output_dir = output_dir[:-10]
        # time stamping the output
        now = datetime.now()
        formatted_date = now.strftime("%h%d_%H%M_%S")
        output_dir += f'_{formatted_date}'
        
    return output_dir

def make_logs(src_lang, tgt_lang, pipeline_name, input_fn, dict_fn, output_dir, gloss_fn, grammar_fn, iter, demo_fn, llm, copy_prompt):
    config = {
        'src_lang': src_lang,
        'tgt_lang': tgt_lang,
        'pipeline_name': pipeline_name,
        'input_fn': input_fn,
        'dict_fn': dict_fn,
        'gloss_fn': gloss_fn,
        "grammar_fn": grammar_fn,
        'iter': iter,
        'llm': llm,
        'copy_prompt': copy_prompt,
    }
    
    json.dump(config, open(f'{output_dir}/config.json', 'w'))
    
    os.makedirs(f'{output_dir}/code_bak', exist_ok=True)
    
    # # save code backup
    # for fn in glob.glob('lingollm/*.py'):
    #     shutil.copy(fn, f'{output_dir}/code_bak/{fn.split("/")[-1]}')
        
    if os.path.exists(demo_fn):
        shutil.copy(demo_fn, f'{output_dir}/code_bak/{demo_fn.split("/")[-1]}')

if __name__ == '__main__':
    args = parser.parse_args()
    work_dir = args.work_dir
    input_fn = args.input_fn
    dict_fn = args.dict_name
    output_dir = args.output_dir
    pipeline_name = args.pipeline
    src_lang = args.src
    tgt_lang = args.tgt
    iter = args.iter
    demo = args.demo
    llm = args.llm
    start = args.start
    
    output_dir = check_dirs(args)
    
    if args.gloss_fn is None:
        args.gloss_fn = input_fn
    
    work_dir = f"data/{work_dir}"
    input_fn = f"{work_dir}/{input_fn}"
    dict_fn = f"{work_dir}/{dict_fn}"
    output_dir = f"{work_dir}/outputs/{output_dir}"
    gloss_fn = f"{work_dir}/{args.gloss_fn}"
    demo_fn = f"{work_dir}/{args.demo}"
    grammar_fn = ""
    if args.copy_prompt:
        copy_prompt = args.copy_prompt
    else:
        copy_prompt = None
    if args.grammar_fn:
        grammar_fn = f"{work_dir}/{args.grammar_fn}"
        
    print(f"OUTPUT_DIR: {output_dir}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    make_logs(src_lang, tgt_lang, pipeline_name, input_fn, dict_fn, output_dir, gloss_fn, grammar_fn, iter, demo_fn, llm, copy_prompt)
    
    pipeline = PIPELINES[pipeline_name]
    llm = get_llm_wrapper(llm)
    
    grammar = "[]" if grammar_fn == "" else open(grammar_fn, 'r').read()
    demo = "" if demo_fn == "" else open(demo_fn, 'r').read()
    if grammar.endswith('.json'):
        grammar = json.loads(grammar)
    
    with open(input_fn, 'r') as f:
        with open(gloss_fn, 'r') as g:
            for i, (sent, gloss) in tqdm(enumerate(zip(f, g))):
                if i < start:
                    continue
                sent = sent.strip()
                if sent == '':
                    continue
                history = []
                if copy_prompt:
                    with open(f'{work_dir}/outputs/{copy_prompt}/history_{i}.json', 'r') as f:
                        history = json.load(f)[:2]
                
                res, messages = pipeline(llm, history, src_lang, tgt_lang, sent, dict_fn, gloss, demo, grammar, iter)
                with open(f'{output_dir}/output_{i}', 'w') as f:
                    f.write(res)
                with open(f'{output_dir}/history_{i}.json', 'w') as f:
                    f.write(json.dumps(messages, indent=2))
                    f.write('\n')
    
    if os.path.exists(dict_fn):
        shutil.copy(dict_fn, f'{output_dir}/code_bak/{dict_fn.split("/")[-1]}')