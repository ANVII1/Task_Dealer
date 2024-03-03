FROM python:bookworm
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

COPY requirements.txt .

COPY ssl_keys .

RUN python3 -m ensurepip &&\
    python3 -m pip install -r requirements.txt

RUN rm -rf requirements.txt

#RUN useradd iskra

#RUN chown -R iskra:iskra /app

#USER iskra

COPY src .

CMD [ "python3","run.py" ]
