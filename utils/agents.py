from utils.call_llm import get_openai_response

class Agent():
    def __init__(self, opt, hub, role, mode, dataset, task_description):
        self.task_description = task_description
        self.opt = opt
        # prompt
        if role == 'generator':
            if mode == 'planning':
                demos = hub.demo_hub[role][mode][dataset][0]
                self.prompt = hub.prompt_hub[role][mode].get(
                    dataset, hub.prompt_hub[role][mode]['default']) \
                .format(
                    task_description=task_description, demo_input=demos[0], 
                    demo_output_1=demos[1], demo_output_2=demos[2], 
                    demo_output_3=demos[3])
            elif mode == 'retrieval' or mode == 'knowledge':
                demos = hub.demo_hub[role][mode][dataset][0]
                self.prompt = hub.prompt_hub[role][mode].get(
                    dataset, hub.prompt_hub[role][mode]['default']) \
                .format(
                    task_description=task_description, demo_input=demos[0], 
                    demo_output=demos[1])
            else:
                self.prompt = hub.prompt_hub[role][mode].get(
                    dataset, hub.prompt_hub[role][mode]['default']) \
                .format(task_description=task_description)
        elif role == 'verifier' or role == 'option_generator':
            self.prompt = hub.prompt_hub[role].get(
                dataset, hub.prompt_hub[role]['default']) \
            .format(task_description=task_description)

        # demo pairs
        if role == 'generator':
            if mode == 'planning' or mode == 'retrieval' or mode == 'knowledge':
                self.demo_pairs = []
            else: 
                self.demo_pairs = hub.demo_hub[role][mode][dataset]
        elif role == 'verifier' or role == 'option_generator':
            if mode == 'planning' or mode == 'retrieval' or mode == 'knowledge':
                self.demo_pairs = hub.demo_hub[role][mode][dataset]
            else:
                self.demo_pairs = hub.demo_hub[role]['origin'][dataset]
    
    def get_input_list(self, context=None, question=None, answer=None):
        demos_list = []
        for demo_p in self.demo_pairs:
            demos_list.extend([demo_p[0], demo_p[1]])

        cur_input = (f"""Context: {context}\n""" if context else '') + (f"""Question: {question}\n""" if question else '') + (f"""Answer: {answer}""" if answer else '')
        return [self.prompt] + demos_list + [cur_input]
    
    def ask(self, context=None, question=None, answer=None, temp=0.0, max_tokens=256):
        input_list = self.get_input_list(context, question, answer)
        if self.opt.api_key['openai_api_key'] == '':
            raise ValueError("Please set the OpenAI API key in the config.py file.") 
        response = get_openai_response(input_list, api_key=self.opt.api_key['openai_api_key'], model='gpt_4', temp=temp, max_tokens=max_tokens)
        return response
