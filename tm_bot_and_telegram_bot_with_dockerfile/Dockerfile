FROM ubuntu:22.04


RUN apt-get update && \
    apt-get upgrade && \
    apt-get install -y python3.10 && \
    apt-get install nano && \
    apt-get install -y python3-pip && \
    apt-get install -y git


RUN mkdir /home/TM_bot_json

WORKDIR /home/TM_bot_json

RUN git clone https://github.com/zbr0ya/tm_json_bot.git

WORKDIR /home/TM_bot_json/tm_json_bot

COPY telegram_token.py .

RUN pip install -r requirements.txt