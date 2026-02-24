FROM python:3-slim

ENV RABBITMQ_HOST=host.docker.internal

WORKDIR /build
COPY pyproject.toml .
COPY LICENSE .
COPY *.md .
COPY src/ src/
RUN --mount=type=cache,target=/root/.cache/pip pip install -e . && pip install hatch

WORKDIR /app

RUN echo "PS1='\[\033[01;32m\]c2_treatment_nonmaleficence_valuator@dev\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\] \$ '" >> /root/.bashrc
RUN echo "alias run=\"python -m  c2_treatment_nonmaleficence_valuator\"" >> /root/.bashrc
RUN echo "alias testAll=\"hatch clean;hatch test\"" >> /root/.bashrc
RUN echo "alias test=\"hatch clean;hatch test -vv \"" >> /root/.bashrc
RUN echo "alias coverage=\"hatch clean;hatch test --cover\"" >> /root/.bashrc
RUN echo "alias fmt=\"hatch fmt --unsafe-fixes\"" >> /root/.bashrc
