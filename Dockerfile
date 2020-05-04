FROM tiangolo/uvicorn-gunicorn:python3.6-alpine3.8

# Install dependecies for building some python modules
RUN apk --update add \
    build-base \
    jpeg-dev \
    zlib-dev


# App user
RUN adduser -D appuser

# Work Directory
WORKDIR /home/thumbnailed
RUN mkdir -p /home/thumbnailed/app

# Copy python dependency list
COPY requirements.txt requirements.txt

# Install required dependecies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app files
COPY app/*.py ./app/
COPY api.py ./

RUN chown -R appuser:appuser ./

USER appuser
CMD uvicorn api:app --host 0.0.0.0 --port 5057