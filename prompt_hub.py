Generator_prompts = {
    "paraphrase": {
        "default": """You are an expert Question Creator.
You will receive an instance of {task_description}. Your task is to rephrase the given context in a short and easy-readable manner without summarizing or explaining. Confirm that the rephrased context do not change the answer to the original question. Simply output the rephrased context starting with "New Context: " and don't output the original question."""
    },
    "addnoise": {
        "default": """You are an expert Question Creator.
You are tasked with creating a new context derived from a given {task_description} by inserting irrelevant facts within the critical sentences of the original context.
These facts shouldn't change the correct answer to the question. Your objective is to embed these distractions in a way that challenges the respondent's focus, increasing the likelihood of errors in their answers.
Simply provide the new context with the added noise, starting with 'New Context:' and do not repeat the original question.""",
        "clutrr": """You are an expert Question Creator.
You are tasked with creating a new context derived from a given {task_description} by inserting irrelevant facts about people's relationships in any place of the original context.
You are encouraged to introduce additional characters not present in the original scenario and describing their connections with the others. However, ensure that these newly incorporated facts do not alter the correct answer to the original question.
Simply provide the new context with the added noise, starting with 'New Context:' and do not repeat the original question."""
    },
    
    "reversepolar": {
        "default": """You are an expert Question Creator.
You will receive an instance of {task_description}. Your task is to generate a new context by altering key details in the original context. Ensure that the rest of the original context remains unchanged. The altered details should change the answer to the question.
Please first output the rephrased context starting with "New Context: ". 
Then give a short step-by-step analysis of the original question based on the new context. 
Finally, generate the corresponding direct answer in a newline starting with "New Answer: "."""
    },
    
    "alternative": {
        "default": '''You are an expert Question Creator.
You are tasked with creating an alternative question derived from a given {task_description}. Your objective is to explore a different aspect of the original problem. 
Start by presenting the new question, beginning with "Alternative Question: ". Follow this by a short but clear analysis of the question in a new line. Conclude by providing the appropriate and direct answer, starting with "Alternative Answer: " in a new line.
Ensure that your newly formulated question closely matches the original in both format and the number of reasoning steps required. It should not be simpler than the original question.''',
        "boolq": """As an expert Question Creator, your objective is to create an alternative short question from a basic {task_description} to explore a different aspect of the original problem.. Here are the requirements for generating the question:
1. Focus on an Unexplored Aspect: Your question should concentrate on information not addressed in the original query.

2. Concise Expression: Make the alternative question as brief as possible, ideally a single short sentence.

3. Maintain Original Format: The alternative question should remain a yes/no judgment question.

Start by presenting the new question, beginning with "Alternative Question: ". Giving the appropriate and direct answer of yes or no, starting with "Alternative Answer: " in a new line."""
    },
    
    "complex": {
        "default": '''You are an expert Question Creator. 
You are tasked with creating a more complex question derived from a given {task_description}. Your objective is to incorporating more additional reasonning steps beyond what is required by the original question and answer.
Start by presenting the new question, beginning with "Complex Question: ". Follow this by a short but clear analysis of the question in a new line. Conclude by providing the appropriate and direct answer, starting with "Complex Answer: " in a new line.
Ensure that your newly formulated question closely matches the original in format like generative, multi-choice, yes/no judgement, etc.''',
        "boolq": """As an expert Question Creator, your objective is to develop a short, complex question from a basic {task_description} context. Here are the requirements for generating the question:

1. Focus on Additional Reasoning Steps: Create a very complex question that requires multiple steps of reasoning and knowledge. This may involve mathematical reasoning, time resoning, space reasoning, logical reasoning, inductive reasoning, analogical reasoning and so on.

2. Concise Expression: Make the complex question as brief as possible, ideally a single sentence. This limits the information provided, increasing the difficulty of answering.

3. Maintain Original Format: The complex question should remain a yes/no judgment question.

Start by presenting the new question, beginning with "Complex Question: ". Follow this by a short but clear analysis of the question in a new line. Giving the appropriate and direct answer of yes or no, starting with "Complex Answer: " in a new line."""
    },

    "planning": {
        "default": '''You are an expert Task Planner.
You will receive an instance of {task_description}. Your task is to generate a new question and its corresponding answer, aiming to ask about the plan to solve the original question given the context. 
Your new question can either inquire about all reasoning steps required or ask for the specific details about a certain (e.g., first, second, or last) step. 
Importantly, ensure that your new question contains all content of the original question, without omitting any details or "if" conditions.

For example, given the following instance:
{demo_input}

Three example questions and answers, respectively about all steps, the first step and the second step, can be generated:
Example 1:
{demo_output_1}
Example 2:
{demo_output_2}
Example 3:
{demo_output_3}

Please understand the following instance, first generate the new question in one newline (start with New Question:). Then generate the new answer in one newline (start with New Answer:).
'''
    },

    "retrieval": {
        "default": '''You are an expert Relevant Context Retriever.
You will receive an instance of {task_description}. Your task is to generate a new question and its corresponding answer, aiming to identify the relevant information from the given context necessary to solve the original question with the original answer. 
Your new question can be formulated in a variety of ways. Importantly, ensure that your new question contains all content of the original question, without omitting any details or "if" conditions.
Your answer must be exclusively from the given context, to contain all required information to solve the original question and cover the original answer. 

For example, given the following instance:
{demo_input}

An example question and answer can be generated:
{demo_output}

Please understand the following instance, first generate the new question in one newline (start with New Question:). Then generate the new answer in one newline (start with New Answer:).
'''
    },

    "knowledge": {
        "default": '''You are an expert Implicit Knowledge Inquirer.
You will receive an instance of {task_description}. Your task is to generate a new question and its corresponding answer, aiming to ask about the implicit knowledge (e.g., facts, rules, commonsense, ...) required to solve the original question. 
Your new question can be formulated in a variety of ways. Importantly, ensure that your new question contains all content of the original question, without omitting any details or "if" conditions.
Your new answer should directly list all required implicit knowledge for the question.

For example, given the following instance:
{demo_input}

An example question and answer can be generated:
{demo_output}

Please understand the following instance, first generate the new question in one newline (start with New Question:). Then generate the new answer in one newline (start with New Answer:).
'''
    }
}

Verifier_prompt = {
    "default": '''You are an expert Question-Answer Validator.
You will receive an instance of {task_description}. Your task is to validate whether the answer is correct to solve the question given the context. 
Please think step-by-step in one line to analyze whether the answer is correct for the question and the context. Then give your final judgement with Yes or No in a newline.
'''
}

Option_generator_prompt = {
    "default": '''You are an expert Candidate Option Generator.
You will receive an instance of {task_description}. Your task is to modify the provided answer to generate a candidate option that wrongly answer the question given the context.
''',
    "boolq": '''You are an expert Candidate Option Generator.
You will receive an instance of {task_description}. Your primary objective is to modify the given answer to generate a candidate option that wrongly answer the question given the context. The incorrect option should appear correct to respondents. Achieve this by strategically omitting crucial information, adding irrelevant details, or making other slight changes. It is essential to ensure that the altered option is still wrong.''',
}

prompt_hub = {
    'generator': Generator_prompts,
    'verifier': Verifier_prompt,
    'option_generator': Option_generator_prompt
}
