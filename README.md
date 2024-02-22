# Benchmark Self-Evolving: A Multi-Agent Framework for Dynamic LLM Evaluation [[Paper]](https://arxiv.org/abs/2402.11443)

<p align="center">
    <img src="https://nanshine-database-1314252170.cos.ap-shanghai.myqcloud.com/img/intro.jpg" width="400" />
</p>

This repository hosts the codes of our benchmark self-evolving framework. It includes support for a range of datasets and models, allowing for dataset self-evolving and model testing through a simple command-line interface.

## Getting Started

### Prerequisites

Before running the project, ensure you have Python and pip installed on your system. You will need Python 3.x for this project.

### Installation

1. **Install Dependencies**: To install the required libraries, navigate to the project's root directory and run:
   
   ```bash
   pip install -r requirements.txt
   ```
   
2. **Configure API Keys**: Fill in your `openai_api_key` and `zhipuai_api_key` in the `config.py` file. These keys are necessary for accessing certain models and APIs used in this project.

3. **Prepare Data(Optional)**: Prepare the `test.jsonl` file under `datasets/{dataset}` directory for each dataset you intend to use. The file should contain original examples in the following format:
   
   ```json
   {
     "context": "Your context here",
     "question": "Your question here",
     "answer": "Your answer here"
   }
   ```
   Each example must include the keys: `context`, `question`, and `answer`. The project currently supports the following datasets: GSM8K, Clutrr, StrategyQA, BoolQ.

## Running the Project

### Generating Evolving Datasets (Optional)

To generate an evolving dataset, use the `gen_dataset.py` script. This step can be skipped if you wish to use pre-evolved datasets already provided in the `datasets/{dataset}` directory.

#### Command:
```bash
python gen_dataset.py --dataset <dataset_name> --mode <evolution_mode> --data_num <number_of_data> [--debug]
```

#### Parameters:

| Parameter    | Description                                                  |
| ------------ | ------------------------------------------------------------ |
| `--dataset`  | Specifies the dataset to use: gsm8k, clutrr, strategyqa, boolq... |
| `--mode`     | Specifies the evolution mode: paraphrase, addnoise, reversepolar, alternative, complex, retrieval, planning, knowledge |
| `--data_num` | Specifies the number of data points to generate              |
| `--debug`    | Enables debug mode, displaying intermediate outputs in the terminal |

#### Example:
```bash
python gen_dataset.py --dataset gsm8k --mode paraphrase --data_num 100
```
This command generates an evolving dataset for the GSM8K dataset through context paraphrasing.

### Testing Models

To test models with the datasets, use the `test.py` script.

#### Command:
```bash
python test.py --dataset <dataset_name> --mode <test_mode> --model <model_name> --data_num <number_of_data> [--local_url <url>] [--debug]
```

#### Parameters:

| Parameter    | Description |
| ------------ | ----------- |
| `--dataset`  | Specifies the dataset to use: gsm8k, clutrr, strategyqa, boolq... |
| `--mode`     | Specifies the test mode: origin, paraphrase, addnoise, reversepolar, alternative, complex, retrieval, planning, knowledge, all |
| `--model`    | Specifies the model to test: gpt_4, chatgpt, chatglm_turbo... |
| `--local_url`| Specifies the URL of the local model |
| `--data_num` | Specifies the number of data points to test |
| `--debug`    | Enables debug mode |

#### Example:
```bash
python test.py --dataset gsm8k --mode paraphrase --model chatgpt
```
This command tests the ChatGPT model with the paraphrased version of the GSM8K dataset.

For custom-deployed models like LLama and Mistral, specify the `--local_url` parameter and implement the `invoke_local_model` method in `utils/call_llm.py`.



## Authors and Citation

This study was authored by Siyuan Wang, Zhuohan Long, Zhihao Fan, Zhongyu Wei and Xuanjing Huang. We encourage the use of our code and data in your research and kindly request citation of our paper as follows:

```bibtex
@article{wang2024benchmark,
title={Benchmark Self-Evolving: A Multi-Agent Framework for Dynamic LLM Evaluation},
author={Wang, Siyuan and Long, Zhuohan and Fan, Zhihao and Wei, Zhongyu and Huang, Xuanjing},
journal={arXiv preprint arXiv:2402.11443},
year={2024}
}
```
