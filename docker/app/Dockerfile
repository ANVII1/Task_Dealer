FROM python:bookworm

ARG BOT_TOKEN
ARG WEBHOOK
ARG WEB_SERVER_HOST
ARG WEB_SERVER_PORT
ARG PATH_TO_PEM
ARG PATH_TO_KEY
ARG WEBHOOK_PATH

ARG DB_HOST

ENV BOT_TOKEN $BOT_TOKEN
ENV WEBHOOK $WEBHOOK
ENV WEB_SERVER_HOST $WEB_SERVER_HOST
ENV WEB_SERVER_PORT $WEB_SERVER_PORT
ENV PATH_TO_PEM $PATH_TO_PEM
ENV PATH_TO_KEY $PATH_TO_KEY
ENV WEBHOOK_PATH $WEBHOOK_PATH

ENV DB_HOST $DB_HOST



WORKDIR /app

RUN useradd dealer --create-home 

RUN chown -R dealer:dealer /app

USER dealer

RUN python3 -m venv venv

# enable venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .

RUN python3 -m ensurepip &&\
    python3 -m pip install -r requirements.txt

RUN rm -rf requirements.txt

COPY app .

CMD [ "python3","main.py" ]