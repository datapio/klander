FROM python:3.9-slim-buster AS builder

RUN set -ex && \
    apt update && \
    apt install --no-install-recommends -y build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install poetry

ADD . /workspace
WORKDIR /workspace

RUN set -ex && \
    poetry install && \
    poetry run pyinstaller --onefile src/klander.py

FROM debian:stable-slim AS runtime

ARG KUBECTL_VERSION "v1.21.1"
ARG KUBECTL_URL "https://storage.googleapis.com/kubernetes-release/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl"

COPY --from=builder /workspace/dist/klander /usr/local/bin/klander
ADD ${KUBECTL_URL} /usr/local/bin/kubectl
RUN chmod a+x /usr/local/bin/kubectl /usr/local/bin/klander

RUN useradd -m -s /bin/bash -d /workspace klander
USER klander
WORKDIR /workspace

CMD ["klander"]
