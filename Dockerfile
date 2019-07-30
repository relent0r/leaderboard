FROM python:3
MAINTAINER dwtaylornz@gmail.com

WORKDIR /usr/src/app

COPY *.py ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]
