import json
from tqdm import tqdm
import os
import argparse

from demo_hub import demo_hub
from prompt_hub import prompt_hub
from utils.agents import Agent
from config import opt
from test import test

class Hub():
    prompt_hub = prompt_hub
    demo_hub = demo_hub
hub = Hub()
task_description_dict = {'gsm8k': 'Mathematical Reasoning Task', 'strategyqa': 'Commonsense Reasoning Task', 'clutrr': 'Kinship Reasoning Task', 'boolq': 'Reading Comprehension Task'}

def get_args_parser():
    parser = argparse.ArgumentParser('Self-Evolving Benchmark', add_help=False)

    parser.add_argument('--dataset', default='', type=str,
                        help='dataset: gsm8k, clutrr, strategyqa, boolq')
    parser.add_argument('--mode', default='', type=str,
                        help='mode: paraphrase, addnoise, reversepolar, alternative, complex, retrieval, planning, knowledge')
    parser.add_argument('--data_num', default=100, type=int,
                        help='the number of data to generate')
    parser.add_argument('--local_url', default=None, type=int,
                        help='url of the local model')
    parser.add_argument('--debug', action='store_true', 
                        help='debug mode')    
    return parser

def output_result(dataset, mode, instance_list):
    instance_list = sorted(instance_list, key=lambda x: x['id'])
    result_path = os.path.join('datasets', dataset, mode + '.jsonl')
    with open(result_path, 'w', encoding='utf-8') as w_f:
        for instance in instance_list:
            w_f.write(json.dumps(instance, ensure_ascii=False) + '\n')

def get_test_data(args, dataset, mode, data_num=100):
    filtered_data_path = os.path.join('results', dataset, mode, f'results_gpt_4_origin.json')
    evolved_dataset_path = os.path.join('datasets', dataset, mode + '.jsonl')

    if not os.path.exists(filtered_data_path):
        print("Filtered data file not found, run GPT-4 to filter data first...")
        success = test(args=args, test_data_path=os.path.join('datasets', dataset, 'test.jsonl'), result_path=filtered_data_path, model='gpt_4', dataset=dataset, mode='origin', data_num=data_num)
        if not success:
            raise ValueError('Original dataset not found, please first set up the original dataset at the path: datasets/{dataset}/test.jsonl')

    with open(filtered_data_path, 'r') as r_f:
        all_data = json.load(r_f) 

    exist_ids = []
    exist_instances = []
    if os.path.exists(evolved_dataset_path):
        with open(evolved_dataset_path, 'r', encoding='utf-8') as r_f:
            exist_instances = [json.loads(line) for line in r_f]
            exist_ids = [each['id'] for each in exist_instances]
    
    return all_data, exist_instances, exist_ids

def to_string(para):
    if type(para) == bool:
        if para:
            return 'Yes'
        else:
            return 'No'
    else:
        return para.strip()

def get_problem(each, dataset, mode):
    # gsm8k
    if dataset == 'gsm8k':
        context = ". ".join(each['question'].split(". ")[:-1]).strip() + "."
        question = each['question'].split(". ")[-1].strip()
        answer = to_string(each['answer'])
        return {'context': context, 'question': question, 'answer': answer}

    # hotpotqa
    elif dataset == 'hotpotqa' or dataset == 'clutrr':
        context = each['context'].replace('\n', ' ').strip()
        question = each['question'].strip()
        answer = each['answer'].strip()
        return {'context': context, 'question': question, 'answer': answer}
    
    elif dataset == 'spartqa': 
        context = each['context'].replace('\n', ' ').strip()
        question = each['question'].replace('\n', ' ').strip()
        answer = ', '.join(each['answer'])
        return {'context': context, 'question': question, 'answer': answer}
    
    # strategyqa
    elif dataset == 'strategyqa':
        context = None
        question = to_string(each['question'])
        answer = to_string(each['answer'])
        return {'context': context, 'question': question, 'answer': answer}
    
    elif dataset == 'boolq':
        context = each['context']
        question = each['question'] if mode != 'complex' else None
        answer = to_string(each['answer']) if mode != 'complex' else None
        return {'context': context, 'question': question, 'answer': answer}


def construct_new_inst(new_inst, status=None, context=None, question=None, answer=None, option=None, cause=None):
    if status:
        new_inst['status'] = status
    if context:
        new_inst['context'] = context
    if question:
        new_inst['question'] = question
    if answer:
        new_inst['answer'] = answer
    if cause:
        new_inst['cause'] = cause
    if option:
        new_inst['option'] = option
    return new_inst

def construct_new_inst_from_response(new_inst, problem, response_list, mode):
    if mode == 'paraphrase' or mode == 'addnoise':
        assert "context: " in response_list[0].lower()
        new_context = response_list[0].lower().split("context: ")[-1].strip()
        return construct_new_inst(new_inst, context=new_context, question=problem["question"], answer=problem["answer"])
    
    elif mode == 'reversepolar':
        if "context: " not in response_list[0].lower() or "answer: " not in response_list[-1].lower():
            return construct_new_inst(new_inst, status='fail', cause='Generator error: no context or answer')
        new_context = response_list[0].lower().split("context: ")[-1].strip()
        new_answer = response_list[-1].lower().split("answer: ")[-1].strip()
        return construct_new_inst(new_inst, context=new_context, question=problem["question"], answer=new_answer)
    
    elif mode == 'alternative' or mode == 'complex' or mode in opt.sub_ability_mode:
        assert "question: " in response_list[0].lower() and "answer: " in response_list[-1].lower()
        new_question = response_list[0].lower().strip().split("question: ")[1].strip()
        new_answer = response_list[-1].lower().strip().split("answer: ")[1].strip()
        return construct_new_inst(new_inst, context=problem["context"], question=new_question, answer=new_answer)
    else:
        raise ValueError('No such mode')

def get_answer_type(dataset):
    if dataset == 'strategyqa' or dataset == 'boolq':
        return 'yes/no'

def get_verifier_label(verifier_response):
    verifier_response_list = verifier_response.split('\n')
    assert 'judgement: ' in verifier_response_list[-1].lower()
    judgement = verifier_response_list[-1].split('judgement: ')[-1].strip()
    if 'yes' in judgement.lower() and 'no' not in judgement.lower():
        return 'pass'
    else:
        return 'fail'
    
def get_option(option_response):
    option_response_list = option_response.split('\n')
    assert 'option: ' in option_response_list[-1].lower()
    option = option_response_list[-1].lower().split('option: ')[-1].strip()
    return option

def generate_dataset(args, mode, task_description):
    dataset = args.dataset
    data_num = args.data_num

    # initialize agents
    generator = Agent(opt, hub, 'generator', mode, dataset, task_description)
    verifier = Agent(opt, hub, 'verifier', mode, dataset, task_description)
    option_generator = Agent(opt, hub, 'option_generator', mode, dataset, task_description)

    # get test data
    test_data, exist_instances, exist_ids = get_test_data(args, dataset, mode, data_num)

    # generate dataset
    for id in tqdm(range(data_num)):
        each = test_data[id]
        if id in exist_ids :
            continue
        
        new_inst = {'id': id, 'status': '', 'cause': '', 'context': '', 'question': '', 'answer': '', 'option': ''}
        if each['status'] == 'fail':
            new_inst = construct_new_inst(new_inst, status='fail', cause='Problem error: Original question failed')
            exist_instances.append(new_inst)
            output_result(dataset, mode, exist_instances)
            continue
        
        problem = get_problem(each, dataset, mode)

        # 1. generate new instance
        if args.debug:
            print('---------------------------------------------------------------------')
            print('Generate new instance:')
        response = generator.ask(context=problem["context"], question=problem["question"], answer=problem["answer"], temp=0.0, max_tokens=512)
        if mode not in ['paraphrase', 'addnoise']:
            response_list = response.split('\n')
        else:
            response_list = [response]

        if args.debug:
            print(response)
        new_inst = construct_new_inst_from_response(new_inst, problem, response_list, mode)
        if new_inst['status'] == 'fail':
            exist_instances.append(new_inst)
            output_result(dataset, mode, exist_instances)
            continue

        if get_answer_type(dataset) == 'yes/no' and mode not in opt.sub_ability_mode:
            if new_inst['answer'].lower() not in ['yes', 'no']:
                new_inst = construct_new_inst(new_inst, status='fail', cause='Generator error: Answer type error')
                exist_instances.append(new_inst)
                output_result(dataset, mode, exist_instances)
                continue

        # 2. verify new instance
        if args.debug:
            print('---------------------------------------------------------------------')
            print('Verify new instance:')
        verifier_response = verifier.ask(context=new_inst["context"], question=new_inst["question"], answer=new_inst["answer"], temp=0.0, max_tokens=512)
        if args.debug:
            print(verifier_response)
        label = get_verifier_label(verifier_response)
        if label == 'fail':
            new_inst = construct_new_inst(new_inst, status='fail', cause='Verify error: 1')
            exist_instances.append(new_inst)
            output_result(dataset, mode, exist_instances)
            continue
        else:
            # 3. generate option
            if args.debug:
                print('---------------------------------------------------------------------')
                print('Generate option:')
            
            if "yes" == new_inst['answer'].lower():
                if args.debug:
                    print('Directly generate option: No')
                new_inst['option'] = "No"
            elif "no" == new_inst['answer'].lower():
                if args.debug:
                    print('Directly generate option: Yes')
                new_inst['option'] = "Yes"
            else:
                option_response = option_generator.ask(context=new_inst["context"], question=new_inst["question"], answer=new_inst["answer"], temp=0.0, max_tokens=512)
                if args.debug:
                    print(option_response)
                option = get_option(option_response)
                new_inst['option'] = option

            # 4. verify option
            if args.debug:
                print('---------------------------------------------------------------------')
                print('Verify option:')
            verifier_response = verifier.ask(context=new_inst["context"], question=new_inst["question"], answer=new_inst["option"], temp=0.0, max_tokens=512)
            if args.debug:
                print(verifier_response)
            label = get_verifier_label(verifier_response)
            if label == 'pass':
                new_inst = construct_new_inst(new_inst, status='fail', cause='Verify error: 2')
                exist_instances.append(new_inst)
                output_result(dataset, mode, exist_instances)
                continue
            else:
                new_inst = construct_new_inst(new_inst, status='pass')
                exist_instances.append(new_inst)
                output_result(dataset, mode, exist_instances)
        
    print(f'Length of generated dataset: {len([each for each in exist_instances if each["status"] == "pass"])}')

def main(args):
    # set parameters
    task_description = task_description_dict[args.dataset]
    mode_list = [args.mode] if args.mode != 'all' else opt.rewrite_mode + opt.sub_ability_mode
    if args.dataset not in opt.dataset_registry:
        raise ValueError(f'Dataset:{args.dataset} not registered')

    # generate dataset
    for mode in mode_list:
        if mode not in opt.rewrite_mode + opt.sub_ability_mode:
            raise ValueError(f'Mode:{mode} not registered')
        print(f'{args.dataset} evolve with mode {mode}...')
        generate_dataset(args, mode, task_description)

if __name__ == '__main__':
    args = get_args_parser().parse_args()
    main(args)