FROM python:3.9

EXPOSE 5001


RUN mkdir /app

COPY api /app
COPY pyproject.toml /app

WORKDIR /app

RUN pip3 install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev


CMD ["python", "server.py"]
