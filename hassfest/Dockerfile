FROM homeassistant/home-assistant:beta

COPY entrypoint.sh /entrypoint.sh
COPY requirements.txt .

RUN pip3 install -r requirements.txt

WORKDIR "/github/workspace"
ENTRYPOINT ["/entrypoint.sh"]

LABEL "name"="hassfest"
LABEL "maintainer"="Home Assistant <hello@home-assistant.io>"
LABEL "version"="1.1"

LABEL "com.github.actions.name"="hassfest"
LABEL "com.github.actions.description"="Run hassfest to validate standalone integration repositories"
LABEL "com.github.actions.icon"="terminal"
LABEL "com.github.actions.color"="gray-dark"
