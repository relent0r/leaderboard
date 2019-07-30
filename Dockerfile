FROM python:3
LABEL authors="relent0r, dwtaylornz"

WORKDIR /usr/src/app

COPY *.py ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py" "(u) ","(p)","(t)"]
