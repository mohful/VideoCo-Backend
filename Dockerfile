FROM python

WORKDIR /python-backend

ENV FLASK_APP=app.py

ENV FLASK_ENV=development

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]