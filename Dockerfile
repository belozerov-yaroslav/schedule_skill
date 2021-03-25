FROM python:3.8.7

WORKDIR /app
COPY . /app

EXPOSE 5000

RUN pip install -r requirements.txt
CMD FLASK_APP=controllers\AliceSkill.py flask run --host="::"
