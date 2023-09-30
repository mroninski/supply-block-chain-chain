# Initial argument determines the micro service to be deployed
ARG PYTHON_VERSION=3.11

FROM tiangolo/uvicorn-gunicorn-fastapi:python${PYTHON_VERSION}

WORKDIR /code

ARG REQUIREMENTS_FILENAME=requirements.txt

COPY ./${REQUIREMENTS_FILENAME} /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./api /code/app

# Initiate the application on port 80
CMD uvicorn api.main:app --workers 1 --port 80 --host 0.0.0.0
