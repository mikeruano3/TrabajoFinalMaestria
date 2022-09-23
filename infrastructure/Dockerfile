FROM  mikeruano3/tfm_unir:v2

ENV APP_HOME /app
WORKDIR ${APP_HOME}
COPY ./flask_prod_app ./flask_prod_app

ENTRYPOINT [ "python" ]

CMD ["flask_prod_app/flask_app.py" ]