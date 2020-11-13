FROM python:3.8.3-alpine

RUN adduser -D i_man

WORKDIR /home/i_man

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY i_man.py config.py boot.sh ./
COPY venv/lib/python3.8/site-packages/flask_uploads.py ./venv/lib/python3.8/site-packages/
RUN chmod +x boot.sh

ENV FLASK_APP i_man.py

RUN chown -R i_man:i_man ./
USER i_man

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]