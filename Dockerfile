FROM python:3.9-slim-buster AS builder

ARG NODE_VERSION="16.x"

ADD https://deb.nodesource.com/setup_${NODE_VERSION} /opt/node-setup.sh

RUN set -ex && \
    apt update && \
    bash /opt/node-setup.sh && \
    apt install --no-install-recommends -y build-essential nodejs && \
    rm -rf /var/lib/apt/lists/*

RUN set -ex && \
    pip install poetry && \
    npm install -g pyright

ADD . /workspace
WORKDIR /workspace

RUN make all

FROM debian:stable-slim AS runtime

ARG KUBECTL_VERSION="v1.21.1"
ARG KUBECTL_URL="https://storage.googleapis.com/kubernetes-release/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl"

COPY --from=builder /workspace/dist/klander /usr/local/bin/klander
ADD ${KUBECTL_URL} /usr/local/bin/kubectl
RUN chmod a+x /usr/local/bin/kubectl /usr/local/bin/klander

RUN useradd -m -s /bin/bash -d /workspace klander
USER klander
WORKDIR /workspace

CMD ["klander"]
