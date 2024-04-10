FROM ghcr.io/home-assistant/home-assistant:beta

COPY entrypoint.sh /entrypoint.sh
COPY requirements.txt .

RUN uv pip install -r requirements.txt

# Install requirements from core
RUN \
    curl -LJO https://raw.githubusercontent.com/home-assistant/core/rc/requirements_test.txt \
    && uv install $(grep -e "^pipdeptree" -e "^tqdm" requirements_test.txt) \
    && rm requirements_test.txt
RUN \
    curl -LJO https://raw.githubusercontent.com/home-assistant/core/rc/requirements_test_pre_commit.txt \
    && uv install $(grep -e "^ruff" requirements_test_pre_commit.txt) \
    && rm requirements_test_pre_commit.txt

WORKDIR "/github/workspace"
ENTRYPOINT ["/entrypoint.sh"]

LABEL "name"="hassfest"
LABEL "maintainer"="Home Assistant <hello@home-assistant.io>"
LABEL "version"="1.1"

LABEL "com.github.actions.name"="hassfest"
LABEL "com.github.actions.description"="Run hassfest to validate standalone integration repositories"
LABEL "com.github.actions.icon"="terminal"
LABEL "com.github.actions.color"="gray-dark"
