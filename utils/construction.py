import random
from config import opt

def set_up_gsm8k_input_list(query):
    instruction = "Answer the following math questions using as short language as possible."

    demo_input_1 = """Question: Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn?"""
    demo_output_1 = """Weng earns 12/60=0.2 per minute. Working 50 minutes, she earned 0.2x50=10. The answer is 10."""

    demo_input_2 = "Question: James writes a 3-page letter to 2 different friends twice a week.  How many pages does he write a year?"
    demo_output_2 = "He writes each friend 3*2=6 pages a week. So he writes 6*2=12 pages every week That means he writes 12*52=624 pages a year. The answer is 624."

    cur_input = f"""{query}"""

    return [instruction, demo_input_1, demo_output_1, demo_input_2, demo_output_2, cur_input]

def set_up_strategyqa_input_list(query):
    instruction = "Answer the following questions with as simple analysis as possible and conclude with yes or no, no other choice."
    demo_input_1 = """Are more people today related to Genghis Khan than Julius Caesar?"""
    demo_output_1 = """Julius Caesar had three children. Genghis Khan had sixteen children. Modern geneticists have determined that out of every 200 men today has DNA that can be traced to Genghis Khan. The answer is yes."""

    demo_input_2 = "Do the anchors on Rede Globo speak Chinese?"
    demo_output_2 = "Rede Globo is a Brazilian television network. The official language of Brazil is Portuguese. The answer is no."
    cur_input = f"""{query}"""

    return [instruction, demo_input_1, demo_output_1, demo_input_2, demo_output_2, cur_input]

def set_up_clutrr_input_list(query):
    instruction = "Considering the context, please provide a brief analysis of the following kinship reasoning question and conclude with a simple, direct kinship term such as 'daughter', 'grandfather', 'mother-in-law', etc. Start the conclusion on a new line with 'Conclusion: [relationship]'."

    demo_input_1 = """Context: [Michael] got mad at his brother [Milton] after he stole his pretzels. [Michael]'s grandfather, [Clarence], was part of a famous band.\nQuestion: What is Clarence's role in Milton'life?"""
    demo_output_1 = """Clarence is Michael's grandfather, and Michael is Milton's brother. The question asks for Clarence's role. Therefore, Clarence is Milton's grandfather.
Conclusion: Grandfather"""

    demo_input_2 = "Context: [Jacob] took his sister [Constance] and his brother [Herman] out to dinner for their birthday last night and they had a great time.\nQuestion: What is Constance's role  in Herman's life?"
    demo_output_2 = """Constance is Jacob's sister, and Jacob is Herman's brother.  The question asks for Constance's role. Therefore, Constance is Herman's sister.
Conclusion: Sister"""

    cur_input = f"""{query}"""

    return [instruction, demo_input_1, demo_output_1, demo_input_2, demo_output_2, cur_input]

def set_up_boolq_input_list(query):
    instruction = "Answer the following questions with as simple analysis as possible and conclude with yes or no, no other choice."
    demo_input_1 = "Context: Cincinnati Bengals\nThe Bengals are one of the 12 NFL teams to not have won a Super Bowl as of the 2017 season; however, they are also one of 8 NFL teams that have been to at least one Super Bowl, but have not won the game.\nQuestion: did the cincinnati bengals ever win a superbowl?"
    demo_output_1 = "The Bengals are one of the 12 NFL teams to not have won a Super Bowl as of the 2017 season. The answer is no."
    demo_input_2 = "Context: Ectopic pregnancy\nOn May 29, 2008 an Australian woman, Meera Thangarajah (age 34), who had an ectopic pregnancy in the ovary, gave birth to a healthy full term 6 pound 3 ounce (2.8 kg) baby girl, Durga, via caesarean section. She had no problems or complications during the 38\u2010week pregnancy.\nQuestion: can an ectopic pregnancy be carried to term?"
    demo_output_2 = "Durga was born via caesarean section. She had no problems or complications during the 38\u2010week pregnancy. The answer is yes."

    return [instruction, demo_input_1, demo_output_1, demo_input_2, demo_output_2, query]

def set_up_ab_two_way_qa_input_list(query, option_1, option_2):
    instruction = "Choose the better option out of two for the given question. Just output 'B' or 'A' without adding any other words."
    cur_input = f"""{query}
A. {option_1}
B. {option_2}"""
    return [instruction, cur_input]

def get_context_question(each):
    return (('Context: ' + each['context'] + '\n') if 'context' in each else '') + 'Question: ' + each['question'], each['answer']


def get_context_question_ab_option(each):
    correct_answer = each['answer']
    wrong_option = each['option']
    if random.random() > 0.5:
        option_1 = correct_answer
        option_2 = wrong_option
        answer = 'A'
    else:
        option_1 = wrong_option
        option_2 = correct_answer
        answer = 'B'
        
    return 'Question: ' + (each['context'] if 'context' in each else '') + each['question'], option_1, option_2, answer

def get_input_list(each, dataset, mode):
    assert dataset in opt.dataset_registry and mode in ['origin'] + opt.sub_ability_mode + opt.rewrite_mode

    if mode in opt.sub_ability_mode:
        query, option_1, option_2, answer = get_context_question_ab_option(each)
        return set_up_ab_two_way_qa_input_list(query, option_1, option_2), answer

    elif mode in opt.rewrite_mode or mode == 'origin':
        query, answer = get_context_question(each)

    if dataset == 'gsm8k':
        return set_up_gsm8k_input_list(query), answer
    elif dataset == 'strategyqa':
        return set_up_strategyqa_input_list(query), answer
    elif dataset == 'clutrr':
        return set_up_clutrr_input_list(query), answer
    elif dataset == 'boolq':
        return set_up_boolq_input_list(query), answer

def get_result(each, answer, response, dataset, mode):
    assert dataset in opt.dataset_registry and mode in ['origin'] + opt.sub_ability_mode + opt.rewrite_mode

    result = {}
    if mode in opt.sub_ability_mode:
        result['id'] = each['id'] if 'id' in each else ''
        result['context'] = each['context'] if 'context' in each else ''
        result['question'] = each['question']
        result['correct_option'] = each['answer']
        result['option'] = each['option']
        result['answer'] = answer
        result['response'] = response
    elif mode in opt.rewrite_mode or mode == 'origin':
        result['id'] = each['id'] if 'id' in each else ''
        result['context'] = each['context'] if 'context' in each else ''
        result['question'] = each['question']
        result['answer'] = answer
        result['response'] = response
    
    return result
        
if __name__ == "__main__":
    pass