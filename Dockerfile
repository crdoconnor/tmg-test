FROM --platform=linux/amd64 python:3.11-slim as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# # Install pipenv 
COPY . /code
WORKDIR /code
RUN pip install -r requirements.txt


EXPOSE 8080

CMD ["uvicorn", "main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "8080"]
