FROM python:3.11.0-bullseye as base

WORKDIR /code

RUN apt-get update -y

COPY ./requirements.txt /code/requirements.txt

RUN apt install -y cmake

# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install --upgrade pip

RUN pip install cmake

RUN apt install -y curl git

RUN git clone https://github.com/davisking/dlib.git
RUN cd dlib && \
    mkdir build; cd build; cmake ..; cmake --build . && \
    cd .. && python setup.py install

FROM base AS runtime

# Expose port
EXPOSE 80

RUN pip install -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]