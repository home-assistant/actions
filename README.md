# actions

GitHub Actions and helper for Home Assistant workflows

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
        - uses: "actions/checkout@v4"
        - uses: "home-assistant/actions/hassfest@master"
```

This will run the `hassfest` action on every push and pull request to all branches, as well as every midnight.


## Helpers

_A collection of GitHub Action helpers, these are considered internal to the Home Assistant organization on GitHub and will change without warning._

- [git-init](./helpers/git-init/action.yml)
- [info](./helpers/info/action.yml)
- [jq](./helpers/jq/action.yml)
- [verify-version](./helpers/verify-version/action.yml)
- [version](./helpers/version/action.yml)
- [version-push](./helpers/version-push/action.yml)
