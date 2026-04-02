# Home Assistant Helper: Info

Extracts build metadata (supported architectures, Docker image, and version) from configuration files.

## Inputs

| Input  | Required | Default | Description                                        |
|--------|----------|---------|----------------------------------------------------|
| `path` | no       | `.`     | Relative directory path to the configuration files |

## Outputs

| Output          | Description                                      |
|-----------------|--------------------------------------------------|
| `architectures` | JSON array of supported architectures            |
| `image`         | Docker image from app config file (if any)       |
| `version`       | Version from app config file (required)          |
| `name`          | Name from app config file (required)             |
| `slug`          | Slug from app config file (required)             |
| `description`   | Description from app config file (required)      |
| `url`           | URL from app config file (if any)                |

## Configuration File Resolution

The action searches for files in the given `path`, checking extensions in order: `json`, `yml`, `yaml`. The **first match wins**.

### Architectures

Resolved from the first file found:

| Priority | File         | Source               | Description                                                                           |
|----------|--------------|----------------------|---------------------------------------------------------------------------------------|
| 1        | `build.*`    | `.build_from` (keys) | **Deprecated** — base image, build arguments and labels should be moved to Dockerfile |
| 2        | `config.*`   | `.arch`              | App configuration — architectures listed directly in the `arch` field                 |

If neither file exists, `architectures` defaults to `[]`.

### App Metadata

Resolved from `config.*` (app configuration, first matching extension):

| Key            | Required | Example output                                 |
|----------------|----------|------------------------------------------------|
| `.name`        | yes      | `"Example App"`                                |
| `.version`     | yes      | `"2024.12.1"`                                  |
| `.slug`        | yes      | `"example_app"`                                |
| `.description` | yes      | `"An example Home Assistant app"`              |
| `.arch`        | yes      | `["amd64","aarch64"]`                          |
| `.image`       | no       | `"ghcr.io/home-assistant/{arch}-app-example"`  |
| `.url`         | no       | `"https://github.com/home-assistant/example"`  |

A warning is emitted for each required option that is missing or null. See [App Configuration](https://developers.home-assistant.io/docs/apps/configuration) for full documentation.

If no config file exists, all values default to `""`.

## Example Usage

```yaml
- uses: home-assistant/actions/helpers/info@master
  id: info
  with:
    path: my-app

- run: |
    echo "Architectures: ${{ steps.info.outputs.architectures }}"
    echo "Image: ${{ steps.info.outputs.image }}"
    echo "Version: ${{ steps.info.outputs.version }}"
    echo "Name: ${{ steps.info.outputs.name }}"
    echo "Slug: ${{ steps.info.outputs.slug }}"
    echo "Description: ${{ steps.info.outputs.description }}"
    echo "URL: ${{ steps.info.outputs.url }}"
```
