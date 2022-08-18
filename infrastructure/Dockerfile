FROM python:3.8.2-slim

ENV APP_HOME /app
WORKDIR ${APP_HOME}

COPY . ./

RUN pip install torch torchvision torchaudio
RUN pip install pip pipenv --upgrade
RUN pipenv install --skip-lock --system --dev
RUN pip install chromedriver-binary requests selenium==3.141.0 transformers keras==2.9.0 tensorflow==2.9.1 Flask
#RUN pip install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
RUN apt-get update && apt install -y chromium-driver
#RUN cp /usr/lib/chromium-browser/chromedriver /usr/bin

CMD ["./scripts/entrypoint.sh"]