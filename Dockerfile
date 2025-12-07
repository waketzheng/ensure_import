FROM python:3.12-slim

ENV PATH="$PATH:/root/.local/bin"
# Change pip mirror
RUN pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple/
RUN pip install --upgrade pip pipx && \
  pipx install pip-conf-mirror && \
  pipx install pdm && \
  pipx install uv && \
  pip-conf-mirror --uv tx

WORKDIR /app
COPY README.md .
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --all-groups --all-extras --no-install-project --frozen

COPY tests tests
COPY ensure_import ensure_import
COPY LICENSE .

ENV PATH="$PATH:.venv/bin"
RUN coverage run --source=ensure_import -m pytest && \
  coverage report -m
