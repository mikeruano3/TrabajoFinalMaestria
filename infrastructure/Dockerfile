FROM  mikeruano3/tfm_unir:tfm

ENV APP_HOME /app
WORKDIR ${APP_HOME}
RUN pip install waitress 
COPY ./flask_prod_app ./flask_prod_app
RUN mkdir -p /root/.cache/huggingface/transformers
COPY ./transformers /root/.cache/huggingface/transformers

ENTRYPOINT [ "python" ]

CMD ["flask_prod_app/flask_app.py" ]