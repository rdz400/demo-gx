FROM python:3.11

COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt

RUN pip3 install -r requirements-dev.txt
RUN pip3 install -r requirements.txt

CMD ["bash"]