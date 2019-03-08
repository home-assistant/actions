FROM python:3.5

LABEL "name"="py35-tox"
LABEL "maintainer"="Home Assistant <hello@home-assistant.io>"
LABEL "version"="1.0"

LABEL "com.github.actions.name"="Tox - Python 3.5 for GitHub Actions"
LABEL "com.github.actions.description"="Run tox on Python 3.5 in GitHub Actions"
LABEL "com.github.actions.icon"="terminal"
LABEL "com.github.actions.color"="gray-dark"

COPY entrypoint.sh /entrypoint.sh

RUN apt-get update \
    && apt-get install -y \
        libudev-dev libavformat-dev libavcodec-dev libavdevice-dev \
        libavutil-dev libswscale-dev libswresample-dev libavfilter-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --no-cache-dir tox

ENTRYPOINT ["/entrypoint.sh"]
