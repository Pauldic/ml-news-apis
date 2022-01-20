FROM python:3.7
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ./api .
COPY start-server.sh .
CMD ["sh","start-server.sh"]
