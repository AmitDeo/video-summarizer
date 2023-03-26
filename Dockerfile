ARG IMAGE=python:3.11-slim

ARG POETRY_VERSION=1.3.2

FROM $IMAGE as base

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6 libx264-dev libavcodec-extra ffmpeg && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y \
        bash \
        build-essential \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*


# ==================================================================
FROM base as build
WORKDIR /video_summarizer
ENV \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=$POETRY_VERSION \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_EXPERIMENTAL_NEW_INSTALLER=false

RUN apt-get update && \
    apt-get install -y \
        curl \
        gcc \
        musl-dev \
        libffi-dev && \
        curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python


# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
ENV PATH="$POETRY_HOME/bin:$PATH"

COPY ./poetry.lock ./pyproject.toml ./

# Install only the production dependencies
RUN poetry install --only main --no-root

COPY ./src/ ./src/
COPY ./streamlit/ ./streamlit/
COPY ./README.md .
COPY ./docker-entrypoint.sh .

# Install root project
RUN poetry install --only-root

# ==================================================================
FROM base as production
WORKDIR /video_summarizer

# Create user with the name amit
RUN addgroup --system --gid 1001 amit && \
    adduser --system --uid 1001 amit

COPY --from=build /video_summarizer ./

RUN mkdir -p /var/log/video_summarizer/ \
    && mkdir -p /var/run/video_summarizer/ \
    && chown -R amit:amit /video_summarizer \
    && chown -R amit:amit /var/log/video_summarizer \
    && chown -R amit:amit /var/run/video_summarizer/ \
    && chmod +x ./docker-entrypoint.sh

USER amit

ENV PYTHONPATH="${PYTHONPATH}:/video_summarizer/.venv"
ENV PATH="${PYTHONPATH}/bin:${PATH}"

EXPOSE 8000

ENTRYPOINT ./docker-entrypoint.sh $0 $@
CMD ["streamlit", "run", "src/summarizer_app.py", "--server.port", "8000"]