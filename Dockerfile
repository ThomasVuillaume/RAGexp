# Inspired from : https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0

# Tested on Python 3.11.6 only
FROM python:3.11.6 as builder
# Pin Poetry version to avoid breaking changes
RUN pip install poetry==1.7.0

# Setting a few Poetry environment variables
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

ENV HOST=0.0.0.0
ENV LISTEN_PORT 8000
EXPOSE 8000

WORKDIR /app

COPY README.md pyproject.toml poetry.lock ./

# > When removing the cache folder make sure this is done in the same RUN command.
# If it’s done in a separate RUN command the cache will still be part of the 
# previous Docker layer, effectively rendering your optimization useless.
# > We can achieve this with the --no-root option, which instructs Poetry to
# avoid installing the current project into the virtual environment.
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11.6-slim as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY RAGexp ./RAGexp

ENTRYPOINT ["python", "-m", "RAGexp"]