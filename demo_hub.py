gsm8k_demo = {
    'context': "Janet's ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg.",
    'question': "How much in dollars does she make every day at the farmers' market?",
    'answer': "Janet sells 16 - 3 - 4 = 9 duck eggs a day.She makes 9 * 2 = 18 every day at the farmer's market.\n#### 18"
}

strategyqa_demo = {
    'question': "Are flag of Gabon colors found in rainbow?",
    'answer': "Rainbows contain the following colors:  red, orange, yellow, green, blue, indigo and violet. The flag of Gabon is green, yellow, and blue. Therefore the answer is yes",
}

clutrr_demo = {
    'context': "[Craig] was angry with his brother [John] for forgetting to pick him up from school. [Marian] drove her son [Craig] to his soccer game. [Molly] was so happy when her grandson [John] was born.",
    'question': "What is Molly's role in Marian's life?",
    'answer': "Mother",
}

boolq_demo = {
    "context": "Closing (real estate) Closing (also referred to as completion or settlement) is the final step in executing a real estate transaction.", 
    "question": "is closing date the same as settlement date", 
    "answer": 'Yes'
}

Generator_demos = {
    'paraphrase': {
        'gsm8k': [
            (
                f"""Context: {gsm8k_demo['context']}\nQuestion: {gsm8k_demo['question']}""",
                """New Context: Janet's daily egg production from her ducks is 16. Each morning, she consumes three eggs for breakfast and uses four more to bake muffins for her friends. The remaining eggs are then sold at the farmers' market for $2 each."""
            )
        ],
        'strategyqa': [],
        'clutrr': [
            (
                f"""Context: {clutrr_demo['context']}\nQuestion: {clutrr_demo['question']}\nAnswer: {clutrr_demo['answer']}""",
                """New Context: [Craig] felt upset because his brother [John] didn't remember to give him a ride home from school. [Marian], [Craig]'s mother, took him to his soccer match. [Molly] was overjoyed at the birth of her grandson [John]."""
            )
        ],
        'boolq': [
            (
                f"""Context: {boolq_demo['context']}\nQuestion: {boolq_demo['question']}\nAnswer: {boolq_demo['answer']}""",
                f"""New Context: In real estate, the process known as closing, alternatively called settlement or completion, marks the conclusive phase of a property deal."""
            )
        ]
    },
    'addnoise': {
        'gsm8k': [
            (
                f"""Context: {gsm8k_demo['context']}\nQuestion: {gsm8k_demo['question']}""",
                '''New Context: Janet's ducks lay 16 eggs per day and her cows product 4L milk per day. She eats three eggs and 1L milk for breakfast every morning and bakes muffins for her friends every day with four eggs. She keeps the remainder milk for herself and only sells the remainder eggs at the farmers' market daily for $2 per fresh duck egg.'''
            )
        ],
        'strategyqa': [],
        "clutrr": [
            (
                f"""Context: {clutrr_demo['context']}\nQuestion: {clutrr_demo['question']}\nAnswer: {clutrr_demo['answer']}""",
                """New Context: [Craig] was angry with his brother [John] for forgetting to pick him up from school. [Ronald] visited his son, [John] for lunch. [Marian] drove her son [Craig] to his soccer game. [Molly] was so happy when her grandson [John] was born. [Demetra] wanted to get her daughter [Stephen] a car for her 16th birthday."""
            )
        ],
        'boolq': [
            (
                f"""Context: {boolq_demo['context']} Question: {boolq_demo['question']}\nAnswer: {boolq_demo['answer']}""",
                f"""New Context: Closing (real estate) - A Brief Insight. Closing, often punctuated by the celebratory uncorking of a carefully selected vintage champagne, which may be a 1988 Dom Perignon or a more modest but equally satisfying local sparkling wine, and also known as completion or settlement, is the final step in executing a real estate transaction."""
            )

        ]
    },
    'reversepolar': {
        'gsm8k': [
            (
                f"""Context: {gsm8k_demo['context']}\nQuestion: {gsm8k_demo['question']}\nQuestion: {gsm8k_demo['question']}\nAnswer: {gsm8k_demo['answer']}""",
                '''New Context: Janet's ducks lay 20 eggs per day. She eats Five for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2.5 per fresh duck egg.
Analysis: Janet sells 20 - 5 - 4 = 11 duck eggs a day.She makes 11 * 2.5 = 27.5 every day at the farmer's market.
New Answer: 27.5'''
            )
        ],
        'strategyqa': [],
        'clutrr': [
            (
                f"""Context: {clutrr_demo['context']}\nQuestion: {clutrr_demo['question']}\nAnswer: {clutrr_demo['answer']}""",
                """New Context: [Craig] was angry with his brother [John] for forgetting to pick him up from school. [Marian] drove her son [Craig] to his soccer game. [Molly] was so happy when her brother [John] was born.
Analysis: Molly is the sister of John, and John is the brother of Craig. Therefore, Molly is the sister of Craig. Marian is the mother of Craig. The question asks for Molly's role. Therefore, Molly is the daughter of Marian.
New Answer: Daughter"""
            )
        ],
        'boolq': [
            (
                f"""Context: FIFA World Cup qualification\nThe hosts of the World Cup receive an automatic berth. Unlike many other sports, results of the previous World Cups or of the continental championships are not taken into account. Until 2002, the defending champions also received an automatic berth, but starting from the 2006 World Cup this is no longer the case.\nOriginal Question: do you qualify for the world cup if you host it?\nOriginal Answer: Yes""",
                """New Context: FIFA World Cup qualification. The hosts of the World Cup can't receive an automatic berth. Unlike many other sports, results of the previous World Cups or of the continental championships are not taken into account. Until 2002, the defending champions also received an automatic berth, but starting from the 2006 World Cup this is no longer the case.
Analysis: The hosts of the World Cup can't receive an automatic berth. Therefore, the answer is no.
New Answer: No"""
            )
        ]
    },
    'alternative': {
        'gsm8k': [
            (
                f"""Context: {gsm8k_demo['context']}\nOriginal Question: {gsm8k_demo['question']}\nOriginal Answer: {gsm8k_demo['answer']}""",
                '''Alternative Question: If Janet decides to use 2 of her daily eggs to make a special omelette for dinner each day, how much will she earn at the farmers' market in a week?
Analysis: Then Janet sells 16 - 3 - 4 - 2 = <<16-3-4-2=7>>7 duck eggs a day. She makes 7 * 2 = $<<7*2=14>>14 every day and therefore earns 14 * 7 = $<<14*7=98>>98 a week at the farmer's market.
Alternative Answer: $98'''
            ),
        ],
        'strategyqa': [
            (
                f"""Original Question: {strategyqa_demo['question']}\nOriginal Answer: {strategyqa_demo['answer']}""",
                """Alternative Question:  Does the flag of Gabon contain a color that is not typically seen in a rainbow?
Analysis: Rainbows contain the colors including red, orange, yellow, green, blue, indigo and violet. The flag of Gabon is green, yellow, and blue."
Alternative Answer: No"""
            )
        ],
        "clutrr": [
            (
                f"""Context: {clutrr_demo['context']}\nOriginal Question: {clutrr_demo['question']}\nOriginal Answer: {clutrr_demo['answer']}""",
                """Alternative Question: What is Marian's role in Molly's life?
Analysis: From the original question and answer, we know Molly is the mother of Marian, and Marian is female. The question asks for Marian's role. Therefore, Marian is the daughter of Molly.
Alternative Answer: Daughter"""
            )
        ],
        'boolq': [
            (
                f"""Context: FIFA World Cup qualification\nThe hosts of the World Cup receive an automatic berth. Unlike many other sports, results of the previous World Cups or of the continental championships are not taken into account. Until 2002, the defending champions also received an automatic berth, but starting from the 2006 World Cup this is no longer the case.\nOriginal Question: do you qualify for the world cup if you host it?\nOriginal Answer: Yes""",
                """Alternative Question: Is a country's performance in previous World Cup events considered for automatic qualification in the next tournament?
Alternative Answer: No"""
            )
        ]
    },
    'complex': {
        'gsm8k': [
            (
                f"""Context: {gsm8k_demo['context']}\nOriginal Question: {gsm8k_demo['question']}\nOriginal Answer: {gsm8k_demo['answer']}""",
                '''Complex Question: How many days will it take for Janet to save $100 from her earnings at the farmers' market?
Analysis: From the original question and answer, we know that Janet earns $18 from selling duck eggs per day. It will take Janet 100 / 18 = <<100/18=5.555555555555555>>5.56 days to save $100. Since Janet cannot work a fraction of a day, she would need to work 6 days.
Complex Answer: 6 days'''
            ),
        ],
        'strategyqa': [
            (
                f"""Original Question: {strategyqa_demo['question']}\nOriginal Answer: {strategyqa_demo['answer']}""",
                '''Complex Question: Are the colors of the flag of a country whose capital is Libreville not found in the phenomenon created when sunlight shines through water droplets in the atmosphere?
Analysis: The country whose capital is Libreville is Gabon. And the phenomenon is rainbow. Based on the original question and answer, we know the answer is yes.
Complex Answer: Yes'''
            ),
        ],
        "clutrr": [
            (
                f"""Context: {clutrr_demo['context']}\nOriginal Question: {clutrr_demo['question']}\nOriginal Answer: {clutrr_demo['answer']}""",
                '''Complex Question: If Marian'father is Tom, what is Molly's role in Tom's life?
Analysis: Molly is the mother of Marian, and Marian is the daughter of Tom. The question asks for Molly's role. Therefore, Molly is the wife of Tom.
Complex Answer: Wife'''
            )
        ],
        'boolq': [
            (
                f"""Context:FIFA World Cup qualification\nThe hosts of the World Cup receive an automatic berth. Unlike many other sports, results of the previous World Cups or of the continental championships are not taken into account. Until 2002, the defending champions also received an automatic berth, but starting from the 2006 World Cup this is no longer the case.""",
                '''Complex Question: If a country hosted the World Cup in 2002 and won, but failed to qualify in the subsequent tournament through regular qualifiers, would they still compete in the 2006 World Cup based on their previous achievements?
Analysis: As the results of the previous World Cups are not taken into account, and it is not the host of the 2006 World Cup, the answer is no.
Complex Answer: No'''
            )
        ]
    },
    'knowledge': {
        'strategyqa': [
            (
                f"""Original Question: Could the members of The Police perform lawful arrests?\nOriginal Answer: false""",
                f'''New Question: What are the implicit knowledge required to determine whether the members of The Police can perform lawful arrests?
New Answer: The members of The Police were musicians, not law enforcement officers. Only law enforcement officers can perform lawful arrests.'''
            )
        ],
        'clutrr': [
            (
                f"""Context: {clutrr_demo['context']}\nOriginal Question: {clutrr_demo['question']}\nOriginal Answer: {clutrr_demo['answer']}""",
                '''New Question: What are the necessary and useful implicit relationship rules we should know in order to determine what Molly's role is in Marian's life?
New Answer: One's brother's mother is also his mother. One's grandmother is the mother of his mother.'''
            )
        ]
    },
    "planning": {
        "gsm8k": [
            (
                f"""Context: {gsm8k_demo['context']}\nOriginal Question: {gsm8k_demo['question']}\nOriginal Answer: {gsm8k_demo['answer']}""",
                f"""New Question: What are the detailed reasoning steps required to calculate how much in dollars Janet makes every day at the farmers' market?
New Answer: The solution involves 2 reasoning steps. [Step 1] calculates the number of eggs can be sold. [Step 2] calculate the money she earns.""",
                f"""New Question: What is the first reasoning step to calculate how much in dollars Janet makes every day at the farmers' market?
New Answer: The first reasoning step is to calculate the number of eggs can be sold per day."""
                f"""New Question: What is the second reasoning step to calculate how much in dollars Janet makes every day at the farmers' market?
New Answer: The second reasoning step is to calculate the money she earns."""
            )
        ],
        'strategyqa': [
            (
                f"""Original Question: {strategyqa_demo['question']}\nOriginal Answer: {strategyqa_demo['answer']}""",
                f"""New Question: What are the detailed reasoning steps required to determine whether the flag of Gabon colors are found in rainbow?
New Answer: The solution involves 3 reasoning steps. [Step 1] Find the colors of the flag of Gabon. [Step 2] Find the colors of rainbow. [Step 3] Determine whether the colors of the flag of Gabon are found in rainbow.""",
                f"""New Question: What is the first reasoning step to determine whether the flag of Gabon colors are found in rainbow?
New Answer: The first reasoning step is to find the colors of the flag of Gabon.""",
                f"""New Question: What is the second reasoning step to determine whether the flag of Gabon colors are found in rainbow?
New Answer: The second reasoning step is to find the colors of rainbow.""",
            ),
        ],
        'clutrr': [
            (
                f"""Context: {clutrr_demo['context']}\nOriginal Question: {clutrr_demo['question']}\nOriginal Answer: {clutrr_demo['answer']}""",
                f"""New Question: What are the detailed reasoning steps required to determine what Molly's role is in Marian's life?
New Answer: The solution involves 2 reasoning steps. [Step 1] identify the relationship between John and Craig'mother Marian. [Step 2] Determine what Molly's role is in Marian's life with the relationship between John and Molly.""",
                f"""New Question: What is the first reasoning step to determine who Molly is to Marian?
New Answer: The first reasoning step is to identify the relationship between John and Craig'mother Marian.""",
                f"""New Question: What is the second reasoning step to determine who Molly is to Marian?
New Answer: The second reasoning step is to determine who Molly is to Marian with the relationship between John and Molly.""",
            ),
        ]
    },
    "retrieval": {
        'clutrr': [
            (
                f"""Context: [Marie] went to the lake for a picnic with her sisters [Harriett] and [Liana]. [Liana] invited her grandfather [Stephen] to join them, but he could n't join them. [Marie] 'son-in-law, [Craig], helped pay off his debts.
Original Question: What is Harriett's role in Stephen's life?
Original Answer: granddaughter""",
                f"""New Question: What relationships in the given context are required to determine What Harriett's role is in Stephen's life?
New Answer: Marie is the sister of Harriett. Liana is the sister of Marie. Stephen is the grandfather of Liana.""",
            )
        ],
        'boolq': [
            (
                f"""Context: FIFA World Cup qualification\nThe hosts of the World Cup receive an automatic berth. Unlike many other sports, results of the previous World Cups or of the continental championships are not taken into account. Until 2002, the defending champions also received an automatic berth, but starting from the 2006 World Cup this is no longer the case.\nOriginal Question: do you qualify for the world cup if you host it?\nOriginal Answer: Yes""",
                """New Question: What facts in the given context are required to determine whether the country qualifies for the 2002 World Cup if it got the championship in the last World Cup?
New Answer: Until 2002, the defending champions also received an automatic berth."""
            )
        ]
    },
}

Verifier_demos = {
    "origin": {
        "gsm8k": [
            (
                f"""Context: {gsm8k_demo['context']}\nQuestion: If Janet decides to use 2 of her daily eggs to make a special omelette for dinner each day, how much will she earn at the farmers' market in a week?\nAnswer: $98""",
                f"""Analysis: If Janet earns $98 a week, she makes 98 / 7 = $<<98/7=14>>14 every day by selling 14 / 2 = $<<14/2=7>>7 duck eggs. This matches the context and question that 16 - 3 - 4 -2 = $<<16-3-4-2=7>>7 duck eggs would be left a day for selling. Therefore, the answer is correct.
Judgement: Yes."""
            ),
            (
                f"""Context: {gsm8k_demo['context']}\nQuestion: How many days will it take for Janet to save $100 from her earnings at the farmers' market?\nAnswer: 5 days""",
                """Analysis: If Janet can save $100 in 5 days, she ned to make at least 100 / 5 = $<<100/5=20>>20 every day by selling 20 / 2 = $<<20/2=10>>10 duck eggs. This contradicts to the context that only 16 - 3 - 4 = $<<16-3-4=9>>9 duck eggs would be left a day for selling. Therefore, the answer is not correct.
Judgement: No."""
            )
        ],
        "strategyqa": [
            (
                f"""Question: {strategyqa_demo['question']}\nAnswer: {strategyqa_demo['answer']}""",
                """Analysis: If the flag of Gabon colors are found in rainbow, then green, yellow, and blue are included in the colors of the rainbow. The colors of the rainbow include red, orange, yellow, green, blue, indigo and violet. The answer says yes. Therefore, the answer is correct.
Judgement: Yes."""
            ),
            (
                f"""Question: Are the colors of the flag of a country whose capital is Libreville not found in rainbow?\nAnswer: Yes""",
                """Analysis: The country whose capital is Libreville is Gabon. If Gabon's flag colors are not found in rainbow, then green, yellow, and blue are not included in the colors of the rainbow. The colors of the rainbow include red, orange, yellow, green, blue, indigo and violet. The answer says yes. Therefore, the answer is not correct.
Judgement: No"""
            )
        ],
        'clutrr': [
            (
                f"""Context: {clutrr_demo['context']}\nQuestion: {clutrr_demo['question']}\nAnswer: {clutrr_demo['answer']}""",
                """Analysis: If Molly is the mother of Marian, then Molly is the grandmother of Craig. As John is the brother of Craig, then Molly is the grandmother of John. This matches the context and question. Therefore, the answer is correct.
Judgement: Yes."""
            ),
            (
                f"""Context: {clutrr_demo['context']}\nQuestion: If Marian'father is Tom, what is Molly's role in Tom's life?\nAnswer: Mother""",
                """Analysis: If Molly is Tom's mother, then Molly is the grandmother of Marian. As Marian is the mother of Craig, then Molly is the great-grandmother of Craig. This contradicts to the context and question. Therefore, the answer is not correct.
Judgement: No."""
            )
        ],
        'boolq': [
            (
                f"""Context: FIFA World Cup qualification\nThe hosts of the World Cup receive an automatic berth. Unlike many other sports, results of the previous World Cups or of the continental championships are not taken into account. Until 2002, the defending champions also received an automatic berth, but starting from the 2006 World Cup this is no longer the case.\nQuestion: If you are the defending champion of the FIFA World Cup, do you receive an automatic berth for the next World Cup?\nAnswer: No""",
                """Analysis: Defending champions do not receive an automatic berth for the next World Cup starting from the 2006 World Cup. The answer says no. Therefore, the answer is correct.
Judgement: Yes."""
            ),
            (
                f"""Context: {boolq_demo['context']}\nQuestion: {boolq_demo['question']}\nAnswer: No""",
                """Analysis: Closing also refers to settlement. The answer says no. Therefore, the answer is incorrect.
Judgement: No."""
            ),
        ]
    },
    'knowledge': {
        'strategyqa': [
            (
                f"""Question: What are the implicit knowledge required to determine whether the members of The Police can perform lawful arrests?
Answer: The members of The Police were musicians, not law enforcement officers. Only law enforcement officers can perform lawful arrests.""",
                f'''Analysis: given the answer (implicit knowledge) we know that "The Police" refers to a music band and can not perform lawful arrests. Therefore, the answer is correct.
Judgement: Yes.'''
            ),
            (
                f"""Context: 
Question: What are the implicit facts required to determine whether shrimp scampi is definitely free of plastic?
Answer: Shrimp scampi is a dish made with shrimp. Microplastics are plastic material.
""",
                f'''Analysis: based on the answer (implicit knowledge) we still do not know whether shrimp scampi contains microplastics or other plastic meterial. The answer is insufficient to determine whether shrimp scampi is definitely free of plastic. Therefore, the answer is not correct.
Judgement: No.
'''
            ),
        ],
        'clutrr': [
            (
                f"""Context: {clutrr_demo['context']}\nQuestion: What are the necessary and useful implicit relationship rules we should know in order to determine who Molly is to Marian?
Answer: One's brother's mother is also his mother. One's grandmother is the mother of his mother.""",
                f'''Analysis: Given the context, we know John'brother Craig is the son of Marian. Therefore, the rule 'One's brother's mother is also his mother' is necessary. And Molly is John's grandmother, so the rule 'One's grandmother is the mother of his mother' is useful. Therefore, the answer is correct.
Judgement: Yes.'''
            ),
            (
                f"""Context: {clutrr_demo['context']}\nQuestion: What are the implicit relationship rules we should know in order to determine who Molly is to Marian?
Answer: One's mother's brother is his uncle. One's mother is the daughter of his grandmother.""",
                f'''Analysis: Marian is the mother of Craig, but there is no mention about the brother of Marian. Therefore, the rule 'One's mother's brother is his uncle' is not necessary. Therefore, the answer is not correct.
Judgement: No.'''
            )
        ],
    },
    'planning': {
        'gsm8k': [
            (
                f"""Context: {gsm8k_demo['context']}
Question: How many reasoning steps are required to calculate how much Janet make every day at the farmers' market?
Answer: The solution involves 2 reasoning steps. [Step 1] calculates the number of eggs can be sold. [Step 2] calculate the money she earns.
""",
                f'''Analysis: calculating how much Janet make every day involves two steps, respectively for egg number can be sold and the money she can earn. Therefore, the answer is correct.
Judgement: Yes.
'''
            ),
            (
                f"""Context: {gsm8k_demo['context']}
Question: What is the second reasoning step to calculate how much Janet make every day at the farmers' market?
Answer: The second reasoning step is to calculate the number of eggs can be sold per day.
""",
                f'''Analysis: calculating the number of eggs can be sold per day is the first reasoning step. Therefore, the answer is not correct.
Judgement: No.
'''
            )
        ],
        'strategyqa': [
            (
                f"""Question: What are the detailed reasoning steps required to determine whether the flag of Gabon colors are found in rainbow?
Answer: The solution involves 3 reasoning steps. [Step 1] Find the colors of the flag of Gabon. [Step 2] Find the colors of rainbow. [Step 3] Determine whether the colors of the flag of Gabon are found in rainbow.""",
                f'''Analysis: To determine whether the flag of Gabon colors are found in rainbow, we should first find the colors of the flag of Gabon and then we can find the colors of rainbow. Finally, we can determine whether the colors of the flag of Gabon are found in rainbow. Therefore, the answer is correct.
Judgement: Yes.
'''
            ),
            (
                f"""Question: What is the last reasoning step to determine whether the flag of Gabon colors are found in rainbow?
Answer: The last reasoning step is to find the colors of rainbow.""",
                f'''Analysis: Find the colors of rainbow is the second reasoning step. The last reasoning step is to determine whether the colors of the flag of Gabon are found in rainbow. Therefore, the answer is not correct.
Judgement: No.
'''
            ),
        ],
        'clutrr': [
            (
                f"""Context: {clutrr_demo['context']}
Question: What are the detailed reasoning steps required to determine who Molly is to Marian?
Answer: The solution involves 2 reasoning steps. [Step 1] identify the relationship between John and Craig'mother Marian. [Step 2] Determine who Molly is to Marian with the relationship between John and Molly.""",
                f'''Analysis: To determine who Molly is to Marian, we should first identify the relationship between John and Craig'mother Marian. Then we can determine who Molly is to Marian with the relationship between John and Molly. Therefore, the answer is correct.
Judgement: Yes.
'''
            ),
            (
                f"""Context: {clutrr_demo['context']}
Question: What is the first reasoning step to determine who Molly is to Marian?
Answer: The first reasoning step is to find the relationship between John and Craig.""",
                f'''Analysis: The relationship between John and Craig is already known. Therefore, the answer is not correct.
Judgement: No.
'''
            )
        ]
    },
    "retrieval": {
        'clutrr': [
            (
                f"""Context: [Marie] went to the lake for a picnic with her sisters [Harriett] and [Liana]. [Liana] invited her grandfather [Stephen] to join them, but he could n't join them. [Marie] 'son-in-law, [Craig], helped pay off his debts.
Question: What relationships in the given context are required to determine who Harriett is to Stephen?
Answer: Marie is the sister of Harriett. Liana is the sister of Marie. Stephen is the grandfather of Liana.""",
                f'''Analysis: To determine who Harriett is to Stephen, we should know the relationship between Marie and Harriett, the relationship between Liana and Marie, and the relationship between Stephen and Liana. Therefore, the answer is correct.
Judgement: Yes.
'''
            ),
            (
                f"""Context: [Marie] went to the lake for a picnic with her sisters [Harriett] and [Liana]. [Liana] invited her grandfather [Stephen] to join them, but he could n't join them. [Marie] 'son-in-law, [Craig], helped pay off his debts.
Question: What relationships in the given context are required to determine who Harriett is to Stephen?
Answer: Marie is the sister of Harriett. Stephen is the grandfather of Liana. Craig is the son-in-law of Marie.""",
                f'''Analysis: To determine who Harriett is to Stephen, we should also know the relationship between Liana and Marie. The relationship between Craig and Marie is not necessary. Therefore, the answer is not correct.
Judgement: No.
'''
            )
        ],
        "boolq": [
            (
                f"""Context: FIFA World Cup qualification\nThe hosts of the World Cup receive an automatic berth. Unlike many other sports, results of the previous World Cups or of the continental championships are not taken into account. Until 2002, the defending champions also received an automatic berth, but starting from the 2006 World Cup this is no longer the case.
Question: What facts in the given context are required to determine whether the country qualifies for the 2002 World Cup if it got the championship in the last World Cup?
Answer: The defending champions received an automatic berth until 2002.""",
                f'''Analysis: We just need to know the fact that the defending champions received an automatic berth until 2002. Therefore, the answer is correct.
Judgement: Yes.'''
            ),
            (
                f"""Context: FIFA World Cup qualification\nThe hosts of the World Cup receive an automatic berth. Unlike many other sports, results of the previous World Cups or of the continental championships are not taken into account. Until 2002, the defending champions also received an automatic berth, but starting from the 2006 World Cup this is no longer the case.
Question: What facts in the given context are required to determine whether the country qualifies for the 2002 World Cup if it got the championship in the last World Cup?
Answer: The defending champions received an automatic berth until 2002 and starting from the 2006 World Cup this is no longer the case.""",
                f'''Analysis: The fact that about 2006 is not relative to the question. Therefore, the answer is not correct.
Judgement: No.'''
            )
        ]
    },
}


OptionGenerator_demos = {
    "origin": {
        "gsm8k": [
            (
                f"""Context: {gsm8k_demo['context']}\nQuestion: If Janet decides to use 2 of her daily eggs to make a special omelette for dinner each day, how much will she earn at the farmers' market in a week?\nAnswer: $98""",
                '''Option: $100'''
            ),
        ]
    },
    "knowledge": {
        "strategyqa": [
            (
                f"""Context: 
Question: What are the implicit facts required to determine whether shrimp scampi is definitely free of plastic?
Answer: Shrimp scampi is a dish made with shrimp. Shrimp have been found to contain microplastics. Microplastics are plastic material.
""",
                f'''Option: Shrimp scampi is a dish made with shrimp. Microplastics are plastic material.'''
            )
        ],
        'clutrr': [
            (
                f"""Context: {clutrr_demo['context']}
Question: What are the necessary and useful implicit relationship rules we should know in order to determine who Molly is to Marian?
Answer: One's brother's mother is also his mother. One's grandmother is the mother of his mother.""",
                f'''Option: One's mother's brother is his uncle. One's mother is the daughter of his grandmother.'''
            ),
        ],
    },
    'planning': {
        "gsm8k": [
            (
                f"""Context: {gsm8k_demo['context']}
Question: What is the second reasoning step to calculate how much Janet make every day at the farmers' market?
Answer: The second reasoning step is to calculate the money she earns.
""",
                f'''Option: The second reasoning step is to calculate the number of eggs can be sold per day.'''
            )
        ],
        'strategyqa': [
            (
                f"""Question: What is the last reasoning step to determine whether the flag of Gabon colors are found in rainbow?
Answer: The last reasoning step is to determine whether the colors of the flag of Gabon are found in rainbow.""",
                f'''Option: The last reasoning step is to find the colors of rainbow.'''
            )
        ],
        'clutrr': [
            (
                f"""Context: {clutrr_demo['context']}
Question: What is the first reasoning step to determine who Molly is to Marian?
Answer: The first reasoning step is to identify the relationship between John and Craig' mother Marian.""",
                f'''Option: The first reasoning step is to find the relationship between John and Craig.'''
            )
        ]
    },
    'retrieval': {
        'clutrr': [
            (
                f"""Context: [Marie] went to the lake for a picnic with her sisters [Harriett] and [Liana]. [Liana] invited her grandfather [Stephen] to join them, but he could n't join them. [Marie] 'son-in-law, [Craig], helped pay off his debts.
Question: What relationships in the given context are required to determine who Harriett is to Stephen?
Answer: Marie is the sister of Harriett. Liana is the sister of Marie. Stephen is the grandfather of Liana.""",
                f'''Option: Marie is the sister of Harriett. Stephen is the grandfather of Liana. Craig is the son-in-law of Marie.'''
            )
        ],
        "boolq": [
            (
                f"""Context: FIFA World Cup qualification\nThe hosts of the World Cup receive an automatic berth. Unlike many other sports, results of the previous World Cups or of the continental championships are not taken into account. Until 2002, the defending champions also received an automatic berth, but starting from the 2006 World Cup this is no longer the case.
Question: What facts in the given context are required to determine whether the country qualifies for the 2002 World Cup if it got the championship in the last World Cup?
Answer: The defending champions received an automatic berth until 2002.""",
                f'''Option: The defending champions received an automatic berth until 2002 and starting from the 2006 World Cup this is no longer the case.'''
            )
        ]
    },
}

demo_hub = {
    'generator': Generator_demos,
    'verifier': Verifier_demos,
    'option_generator': OptionGenerator_demos
}