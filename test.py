import json
from tqdm import tqdm
import os
import argparse

from utils.call_llm import get_completion
from utils.construction import get_input_list, get_result
from utils.judge_result import judge_result
from config import opt

def get_args_parser():
    parser = argparse.ArgumentParser('Self-Evolving Benchmark', add_help=False)

    parser.add_argument('--dataset', default='', type=str,
                        help='dataset: gsm8k, clutrr, strategyqa, boolq')
    parser.add_argument('--mode', default='', type=str,
                        help='mode: origin, paraphrase, addnoise, reversepolar, alternative, complex, retrieval, planning, knowledge, all')
    parser.add_argument('--model', default='', type=str,
                        help='model: gpt_4, chatgpt, chatglm_turbo, Llama-2-70b-chat, mistral-7b-instruct-v0.2')
    parser.add_argument('--local_url', default=None, type=str,
                        help='url of the local model')
    parser.add_argument('--data_num', default=100, type=int,
                        help='the number of data to test')
    parser.add_argument('--debug', action='store_true',
                        help='debug mode')
    parser.set_defaults(debug=False)
    
    return parser

def get_test_data(test_data_path, result_path, data_num):
    if not os.path.exists(test_data_path):
        return [], []
    with open(test_data_path, 'r', encoding='utf-8') as r_f:
        all_data = [json.loads(line, ) for line in r_f][:data_num] 

    result_list = []
    if os.path.exists(result_path):
        with open(result_path, 'r') as r_f:
            result_list = json.load(r_f)
    else:
        if not os.path.exists(os.path.dirname(result_path)):
            os.makedirs(os.path.dirname(result_path))
    
    test_data = []
    for each in all_data:
        if 'status' in each and each['status'] == 'fail':
            continue
        flag = False
        for i, result in enumerate(result_list):
            if each['question'] == result['question']:
                if 'context' in each:
                    if each['context'] == result['context']:
                        flag = True
                        break
                else:
                    flag = True
                    break
        if flag:
            continue
        else:
            test_data.append(each)
    return test_data, result_list

def test(args, test_data_path, result_path, model, dataset, mode, data_num=100):
    test_data, result_list = get_test_data(test_data_path, result_path, data_num)
    if test_data == [] and result_list == []:
        return False

    for each in tqdm(test_data):
        input_list, answer = get_input_list(each, dataset, mode)
        response = get_completion(input_list, model, opt.api_key, args.local_url)
        if args.debug:
            print('Response: \n', response)
        result = get_result(each, answer, response, dataset, mode)
        result['status'] = judge_result(answer, response, dataset, mode)

        result_list.append(result)
        with open(result_path, 'w') as w_f:
            json.dump(result_list, w_f, indent=4)

    pass_num = 0
    for result in result_list:
        result['status'] = judge_result(result['answer'], result['response'], dataset, mode)
        if result['status'] == 'pass':
            pass_num += 1
    print('------------------------------------')
    print(f'model: {model}, dataset: {dataset}, mode: {mode} ')
    print(f'len: {len(result_list)}')
    if len(result_list) > 0:
        print(f'pass rate: {pass_num / len(result_list)}')
    with open(result_path, 'w') as w_f:
        json.dump(result_list, w_f, indent=4)

    return True

def main(args):
    dataset = args.dataset
    mode_list = [args.mode] if args.mode != 'all' else opt.rewrite_mode + opt.sub_ability_mode
    data_num = args.data_num
    model = args.model

    if model not in ['gpt_4', 'chatgpt', 'chatglm_turbo', 'Llama-2-70b-chat', 'mistral-7b-instruct-v0.2']:
        raise ValueError(f'Model:{model} not registered')
    if dataset not in opt.dataset_registry:
        raise ValueError(f'Dataset:{dataset} not registered')

    for mode in mode_list:
        if mode in opt.rewrite_mode + opt.sub_ability_mode:
            test_data_path = os.path.join('datasets', dataset, mode + '.jsonl')
        elif mode == 'origin':
            test_data_path = os.path.join('datasets', dataset, 'test.jsonl')
        else:
            raise ValueError(f'No such mode: {mode}')
        result_path = os.path.join('results', dataset, mode, f'results_{model}.json')
        test(args, test_data_path, result_path, model, dataset, mode, data_num=data_num)

if __name__ == '__main__':
    args = get_args_parser().parse_args()
    main(args)