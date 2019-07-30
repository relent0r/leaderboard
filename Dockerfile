FROM python:3
LABEL authors="relent0r, dwtaylornz"

WORKDIR /usr/src/app

COPY *.py ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]
