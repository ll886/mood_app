FROM python:3.8.3-alpine
# set working directory to /app
WORKDIR /app
# copy current directory content into container at /app
ADD . /app
ENV FLASK_APP run.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev 
# install dependencies
RUN pip install -r requirements.txt
COPY . .
# run app
CMD ["flask", "run"]
