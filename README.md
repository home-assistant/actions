# actions

GitHub Actions for Home Assistant workflows

## JQ

`home-assistant/actions/jq@master`


## Tox

- `home-assistant/actions/py37-tox@master`
- `home-assistant/actions/py36-tox@master`
- `home-assistant/actions/py35-tox@master`

## hassfest

_Run hassfest to validate standalone integration repositories._

**action**: `home-assistant/actions/hassfest@master`

example implementation:

```yaml
name: Validate with hassfest

on:
  push:
  pull_request:
  schedule:
    - cron:  '0 0 * * *'

jobs:
  validate:
    runs-on: "ubuntu-latest"
    steps:
        - uses: "actions/checkout@v2"
        - uses: home-assistant/actions/hassfest@master
```

This will run the `hassfest` action on every push and pull request to all branches, as well as every midnight.
