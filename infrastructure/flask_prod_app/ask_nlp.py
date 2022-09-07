
from transformers import *
from tensorflow import keras       
from datetime import datetime

def initNlp():
    nlp = pipeline(
        'question-answering',
        model='mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es',
        tokenizer=(
        'mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es',
        {"use_fast": False}
        )
    )
    return nlp

def askQuestion(nlp, peopleList):
    for people in peopleList:
        for question_id in people['question_object']:
            question_text = people['question_object'][question_id]['question']
            question_response = nlp({
                'question': question_text,
                'context': people['full_text']
            })
            people['question_object'][question_id]['response'] = question_response
    respuesta = dict()
    respuesta['status'] = 200
    respuesta['data'] = peopleList
    return respuesta