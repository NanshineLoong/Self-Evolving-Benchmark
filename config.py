import warnings

class DefaultConfig(object):
    sub_ability_mode = ['planning', 'retrieval', 'knowledge']
    rewrite_mode = ['paraphrase', 'addnoise', 'reversepolar',  'alternative', 'complex']
    dataset_registry = ['gsm8k', 'strategyqa', 'clutrr', 'boolq']

    api_key = {
        "openai_api_key": "",
        "zhipuai_api_key": ""
    }

    def parse(self, kwargs):
        for k, v in kwargs.items():
            if not hasattr(self, k):
                warnings.warn("Warning: opt has not attribute %s" %k)
            setattr(self, k, v)

        print('user config:')
        for k, v in self.__class__.__dict__.items():
            if not k.startswith('__'):
                print(k, getattr(self, k))

opt = DefaultConfig()
