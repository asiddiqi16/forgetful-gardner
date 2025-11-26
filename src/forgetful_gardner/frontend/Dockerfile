# forgetul_gardner_frontend/Dockerfile

FROM python:3.12-slim

RUN apt-get update && \
    apt-get upgrade --yes

# Install OS-level dependencies OpenCV needs
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home forgetful_gardner
USER forgetful_gardner
WORKDIR /home/forgetful_gardner

ENV VIRTUALENV=/home/forgetful_gardner/venv
RUN python3 -m venv $VIRTUALENV
ENV PATH="$VIRTUALENV/bin:$PATH"

COPY --chown=forgetful_gardner ./pyproject.toml ./
RUN python -m pip install --upgrade pip setuptools

COPY --chown=forgetful_gardner ./src/ src/
RUN python -m pip install .

EXPOSE 8000
CMD ["sh", "src/entrypoint.sh"]