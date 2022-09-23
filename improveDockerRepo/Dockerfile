FROM  mikeruano3/tfm_unir:tfm

RUN pip install waitress 
RUN mkdir -p /root/.cache/huggingface/transformers
COPY ../infrastructure/transformers /root/.cache/huggingface/transformers
