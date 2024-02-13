import re
from config import opt

def clear_sign(text):
    text = re.sub(r'[^\w\s]','',text)
    text = re.sub(r'\s+',' ',text)
    text = text.strip()
    return text.lower()

def judge_gsm8k_result(answer, response, mode):
    assert mode in ['origin'] + opt.rewrite_mode

    if mode == 'origin':
        pure_answer = float(answer.split('####')[1].strip().replace(',', ''))  
    else:
        pure_answer = answer.strip().replace(',', '')
        pure_answer = re.findall(r"-?\d+\.?\d*", pure_answer)
        pure_answer = float(pure_answer[-1]) if pure_answer else None

    pure_response = response.replace(',', '')
    pure_response = re.findall(r"-?\d+\.?\d*", pure_response)
    pure_response = [float(ea[:-1]) if ea[-1] == '.' else float(ea) for ea in pure_response]

    if pure_answer and pure_response and  any([(abs(pure_answer - ea) < 0.0001) for ea in pure_response[-2:]]):
        return 'pass'
    else:
        return 'fail'
    
def judge_strategyqa_result(answer, response):
    response = response.strip()
    if type(answer) == str:
        if answer.lower() == 'yes':
            answer = True
        elif answer.lower() == 'no':
            answer = False
        else:
            return 'fail'
    if response.lower() == 'yes' and answer or response.lower() == 'no' and not answer:
        return 'pass'
    if 'incorrect' in response.lower() and not answer or 'correct' in response.lower() and answer:
        return 'pass'
    if (answer and bool(re.search(r"(^|\s)yes(\s|\.|,)", response.lower()))) or (not answer and bool(re.search(r"(^|\s)no(\s|\.|,)", response.lower()))):
        return 'pass'
    else:
        return 'fail'
    
def judge_hotpotqa_result(answer, response):
    if answer.lower() in response.lower() or response.lower() in answer.lower() or all([res in answer.lower() for res in re.split(r'[;""\'.,\s]\s*', response.lower())]) or all([res in response.lower() for res in re.split(r'[;""\'.,\s]\s*', answer.lower())]):
        return 'pass'
    else:
        return 'fail'
    
def judge_with_rouge(answer, response):
    answer = clear_sign(answer)
    response = clear_sign(response)
    from rouge import Rouge
    rouge = Rouge()
    score = rouge.get_scores(response, answer)
    if score[0]['rouge-2']['r'] > 0.5 or score[0]['rouge-1']['r'] > 0.5 or score[0]['rouge-l']['r'] > 0.5 or score[0]['rouge-2']['p'] > 0.5 or score[0]['rouge-1']['p'] > 0.5:
        return 'pass'
    else:
        return 'fail'
    
def judge_clutrr_result(answer, response):
    reflect_dict = {'wife': ['spouse'], 'husband': ['spouse'], 'brother': ['sibling'], 'sister': ['sibling'], 'father': ['parent'], 'mother': ['parent'], 'son': ['child', 'children'], 'daughter': ['child', 'children'], 'grandfather': ['grandparent'], 'grandmother': ['grandparent'], 'grandson': ['grandchild', 'grandchildren'], 'granddaughter': ['grandchild', 'grandchildren'], 'stepdaughter': ['daughter', 'stepchild', 'stepchildren'], 'stepson': ['son', 'stepchild', 'stepchildren'], 'stepmother': ['mother', 'stepparent'], 'stepfather': ['father', 'stepparent'], 'fatherinlaw': ['father'], 'motherinlaw': ['mother'], 'brotherinlaw': ['brother'], 'sisterinlaw': ['sister'], 'soninlaw': ['son'], 'daughterinlaw': ['daughter'], 'granddaughterinlaw': ['granddaughter'],'adoptedson': ['son'], 'adopteddaughter': ['daughter'], 'adoptiveson': ['son'], 'adoptivedaughter': ['daughter']}
    pure_response = response.split('\n')[-1].strip()
    if 'Conclusion: ' not in pure_response:
        return 'fail'
    pure_response = pure_response.split('Conclusion: ')[-1].strip()

    def process_str_to_list(s):
        s = s.replace('\\n', '').replace('great-', 'great').replace('Great-', 'great').replace('-in-law', 'inlaw').replace('Adopted ', 'adopted').replace('adopted ', 'adopted').replace('adoptive ', 'adoptive').replace('Adoptive ', 'adoptive')
        s = s.strip()
        s = re.split(r'[;""\-\'\.,\s]\s*', s.lower())
        for i in range(len(s) - 1):
            if s[i] == 'great':
                s[i] = s[i] + s[i + 1]
                s[i + 1] = ''
        s = [ea for ea in s if ea and ea != 'and' and ea != 'or' and ea != 'answer:']
        s = [ea[:-1] if ea[-1] == 's' else ea for ea in s]
        extended_s = []
        for ea in s:
            if ea in reflect_dict:
                extended_s.extend(reflect_dict[ea] + [ea])
            else:
                extended_s.append(ea)
        return s, extended_s
    answer_l, extended_answer_l = process_str_to_list(answer)
    response_l, extended_response_l = process_str_to_list(pure_response)
    if all([res in extended_answer_l for res in response_l]) or all([res in extended_response_l for res in answer_l]):
        return 'pass'
    else:
        return 'fail'
    
def judge_ab_two_way_qa_result(answer, response):
    response = response.strip()
    if 'the answer is ' in response.lower():
        response = response.lower().split('the answer is ')[-1].strip()
        if response[0].lower() == 'a' or response[0].lower() == 'b':
            response = response[0].lower()
        if answer.lower() == response.lower():
            return 'pass'

    response = response.split('.')[0].strip()
    if response[-1] == 'A' or response[-1] == 'B':
        response = response[-1]
    if answer.lower() == response.lower() or f'{answer} ' in response or f' {answer}.' in response or f'{answer}\n' in response or f'({answer})' in response:
        return 'pass'
    else:
        return 'fail'

def judge_result(answer, response, dataset, mode):
    assert dataset in opt.dataset_registry and mode in ['origin'] + opt.sub_ability_mode + opt.rewrite_mode

    if mode in opt.sub_ability_mode:
        return judge_ab_two_way_qa_result(answer, response)
    
    if dataset == 'gsm8k':
        return judge_gsm8k_result(answer, response, mode)
    elif dataset == 'strategyqa' or dataset == 'boolq':
        return judge_strategyqa_result(answer, response)
    elif dataset == 'clutrr':
        return judge_clutrr_result(answer, response)
    else:
        raise ValueError('No such dataset')