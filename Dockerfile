FROM python:3.10-slim-buster
COPY . /app/ 
WORKDIR /app 
RUN apt-get -y update && apt-get install -y make && apt install -y ffmpeg
RUN touch config
RUN make install
CMD ["make", "run"]
