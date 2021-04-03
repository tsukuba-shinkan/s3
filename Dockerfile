FROM ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install python3-pip -y
RUN pip3 install beautifulsoup4==4.9.3 \
  certifi==2020.12.5 \
  chardet==4.0.0 \
  click==7.1.2 \
  fastapi==0.63.0 \
  h11==0.12.0 \
  idna==2.10 \
  mecab-python3==1.0.3 \
  pydantic==1.8.1 \
  requests==2.25.1 \
  soupsieve==2.2.1 \
  starlette==0.13.6 \
  typing-extensions==3.7.4.3 \
  unidic-lite==1.0.8 \
  urllib3==1.26.4 \
  uvicorn==0.13.4
ADD . /workdir
WORKDIR /workdir
RUN python3 download.py && python3 gen_wordtable.py && python3 gen_wordtable_event.py

EXPOSE 8000
CMD ["uvicorn","app:app","--host","0.0.0.0"]