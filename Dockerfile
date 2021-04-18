FROM python:3.8.7

WORKDIR /app
COPY . /app

EXPOSE 5000

RUN pip install -r requirements.txt
CMD ['python3', 'controllers/AliceSkill.py']
