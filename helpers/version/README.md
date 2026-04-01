# Home Assistant Helper: Version

Determines **version**, **stability**, **channel**, and **publish** status for Home Assistant builds based on the build type and GitHub event trigger.

## Inputs

| Input  | Required | Default   | Description                                              |
|--------|----------|-----------|----------------------------------------------------------|
| `type` | no       | `generic` | Target type: `core`, `supervisor`, `plugin`, or `generic` |

## Outputs

| Output    | Description                                          |
|-----------|------------------------------------------------------|
| `version` | Resolved version string                              |
| `stable`  | `"true"` if stable build, else `"false"`             |
| `channel` | Suggested update channel (`dev`, `beta`, or `stable`) |
| `publish` | `"true"` if artifacts should be published            |

## Manual Overrides (workflow_dispatch)

All outputs can be overridden via `github.event.inputs`:

| Input                           | Overrides |
|---------------------------------|-----------|
| `github.event.inputs.version`   | `version` |
| `github.event.inputs.stable`    | `stable`  |
| `github.event.inputs.channel`   | `channel` |
| `github.event.inputs.publish`   | `publish` |

When any of these are set, they take **absolute precedence** over all computed values below.

---

## Build Types: `plugin` / `supervisor`

These two types produce identical outputs.

| Trigger              | version                          | stable  | channel | publish |
|----------------------|----------------------------------|---------|---------|---------|
| **Pull Request**     | `<commit SHA>`                   | `false` | `dev`   | `false` |
| **Push to master**   | CalVer dev `YYYY.MM.X.devDDNN`   | `false` | `dev`   | `true`  |
| **Release (tag)**    | Tag name (e.g. `2024.12.1`)     | `true`  | `beta`  | `true`  |
| **Push to tag**      | Tag name                         | `false` | `dev`   | `true`  |
| **workflow_dispatch** | From inputs or ref              | From inputs or `false` | From inputs or computed | From inputs or `false` |

### Notes
- **PR builds are never published.** The presence of `github.head_ref` (set on PRs) forces `publish=false`.
- **Push to master** generates a [CalVer](https://calver.org/) dev version: base is `YYYY.MM.N` (incrementing from the latest matching tag), suffixed with `.devDDNN` where `DD` is the UTC day and `NN` is the zero-padded commit count since UTC midnight.
- **Stable releases** get channel `beta` (not `stable`) — this is by design for plugin/supervisor types.
- **Note:** `supervisor` previously had a side-effect of patching `SUPERVISOR_VERSION` in `supervisor/const.py` after version resolution. This has been removed.

---

## Build Type: `core`

| Trigger              | version                          | stable  | channel | publish |
|----------------------|----------------------------------|---------|---------|---------|
| **Pull Request**     | `merge` (literal ref tail)       | `false` | _(unset)_ | `false` |
| **Push to `dev` branch** | Nightly bump (via `version_bump.py`) | `false` | `dev` | `false` |
| **Release (tag `X.Y.Z`)** | `X.Y.Z`                     | `true`  | `stable` | `true`  |
| **Release (tag `X.Y.ZbN`)** | `X.Y.ZbN`                 | `true`  | `beta`  | `true`  |
| **Push to tag `X.Y.ZdevN`** | `X.Y.ZdevN`               | `false` | `dev`   | `false` |
| **workflow_dispatch** | From inputs or ref              | From inputs or `false` | From inputs or computed | From inputs or `false` |

### Notes
- **Channel is derived from the version string itself:**
  - Contains `dev` → `dev`
  - Contains `b` → `beta`
  - Otherwise → `stable`
- **Only releases are published** (`event_name == release`). Pushes, PRs, and other events all produce `publish=false`.
- **Nightly dev builds** are triggered by a push to the `dev` branch, which installs the package via `uv` and runs `script/version_bump.py nightly` to compute the next dev version from `pyproject.toml`.
- The CalVer dev versioning used by plugin/supervisor/generic does **not** apply to core.

---

## Build Type: `generic`

| Trigger              | version                          | stable  | channel | publish |
|----------------------|----------------------------------|---------|---------|---------|
| **Pull Request**     | `<commit SHA>`                   | `false` | _(unset)_ | _(unset)_ |
| **Push to master**   | CalVer dev `YYYY.MM.X.devDDNN`   | `false` | _(unset)_ | _(unset)_ |
| **Release (tag)**    | Tag name                         | `true`  | _(unset)_ | _(unset)_ |
| **Push to tag**      | Tag name                         | `false` | _(unset)_ | _(unset)_ |
| **workflow_dispatch** | From inputs or ref              | From inputs or `false` | From inputs or _(unset)_ | From inputs or _(unset)_ |

### Notes
- **Channel and publish are only set if manually provided** via `workflow_dispatch` inputs. The action does not compute these for `generic` type.
- Version computation on master/main uses the same CalVer dev scheme as plugin/supervisor.
- PR builds resolve to the commit SHA (same as plugin/supervisor).

---

## Version Resolution Flowchart

```
github.event.inputs.version set?
├─ YES → use that value
└─ NO
   ├─ ref is master/main AND type is supervisor/plugin/generic?
   │  └─ YES → CalVer dev: YYYY.MM.X.devDDNN
   ├─ ref is "merge" AND type is supervisor/plugin/generic?
   │  └─ YES → commit SHA
   ├─ ref is "dev" AND type is core?
   │  └─ YES → nightly bump via version_bump.py
   └─ otherwise → extract version from ref (last path segment)
```

## CalVer Dev Version Format

Used by `supervisor`, `plugin`, and `generic` on pushes to master/main:

```
YYYY.MM.N.devDDNN
│    │  │     │ └─ zero-padded commit count since UTC midnight
│    │  │     └─── UTC day of month
│    │  └───────── patch number (incremented from latest matching tag, or 0)
│    └──────────── month
└───────────────── year
```

Example: `2024.12.3.dev1405` = December 2024, patch 3, 14th day, 5 commits since midnight UTC.
