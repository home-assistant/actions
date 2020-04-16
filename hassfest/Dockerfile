FROM python:3-alpine

COPY entrypoint.sh /entrypoint.sh

RUN \
    apk add --no-cache \
        python3-dev \
        bash \
        git \
        gcc \
        libc-dev \
        libffi-dev \
        openssl-dev \
    \
    && rm -rf /var/cache/apk/* \
    \
    && git clone --depth 1 https://github.com/home-assistant/core.git /core \
    \
    && python3 -m pip install --no-cache-dir -e /core \
    \
    && chmod +x /entrypoint.sh

WORKDIR "/github/workspace"
ENTRYPOINT ["/entrypoint.sh"]

LABEL "name"="hassfest"
LABEL "maintainer"="Home Assistant <hello@home-assistant.io>"
LABEL "version"="1.0"

LABEL "com.github.actions.name"="hassfest"
LABEL "com.github.actions.description"="Run hassfest to validate standalone integration repositories"
LABEL "com.github.actions.icon"="terminal"
LABEL "com.github.actions.color"="gray-dark"