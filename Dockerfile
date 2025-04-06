FROM python:3.11-slim

# Change pip mirror
RUN pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple/

WORKDIR /app
COPY tests tests
COPY ensure_import ensure_import
COPY pyproject.toml .
COPY poetry.lock .

RUN pip install --upgrade pip pipx && \
  pipx install poetry && \
  pipx inject poetry-plugin-export && \
  poetry export --with=dev --without-hashes -o requirements.txt && \
  pip install -r requirements.txt && \
  coverage run --source=ensure_import -m pytest && \
  coverage report -m
