
from transformers import *
from tensorflow import keras       

nlp = None
isGlobalVariableReady = False

nlp = pipeline(
        'question-answering',
        model='mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es',
        tokenizer=(
        'mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es',
        {"use_fast": False}
        )
)
isGlobalVariableReady = True