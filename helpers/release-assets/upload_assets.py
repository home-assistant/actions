"""
Upload files as release assets.
"""
from __future__ import annotations

import fnmatch
import json
import re
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path
from shlex import quote
from typing import Any, NamedTuple


class Asset(NamedTuple):
    id: int
    name: str
    url: str


class File(NamedTuple):
    name: str
    path: Path
    content_type: str


def find_existing_assets(token: str, ctx: dict[str, Any]) -> list[Asset]:
    """
    Get a list of existing release assets.
    Used to delete them and to prevent name conflicts when uploading new ones.
    https://docs.github.com/en/rest/reference/releases#list-release-assets
    """
    print("-- Load list with existing assets")
    url = ctx["assets_url"]
    cmd = (
        "curl -sS "
        '-H "Accept: application/vnd.github.v3+json" '
        f'-H "Authorization: token {quote(token)}" '
        f"{quote(url)}"
    )
    p = subprocess.run(args=cmd, capture_output=True, check=False, shell=True)
    if p.returncode != 0:
        print(f"::error::{p.stderr.decode()}")
        sys.exit(1)

    data: list[dict[str, Any]] | dict[str, Any] = json.loads(p.stdout.decode())
    if isinstance(data, dict):
        print(f"::error::{p.stdout.decode()}")
        sys.exit(1)
    assets = [Asset(item["id"], item["name"], item["url"]) for item in data]
    for asset in assets:
        print(f"{asset.name} [{asset.id}]")
    return assets


def delete_assets(token: str, assets: list[Asset]) -> None:
    """
    Delete existing assets to upload new ones.
    https://docs.github.com/en/rest/reference/releases#delete-a-release-asset
    """
    print("-- Delete assets")
    for item in assets:
        cmd = (
            "curl -sS "
            "-X DELETE "
            '-H "Accept: application/vnd.github.v3+json" '
            f'-H "Authorization: token {quote(token)}" '
            f"{quote(item.url)}"
        )
        p = subprocess.run(args=cmd, capture_output=True, check=False, shell=True)
        if p.returncode != 0:
            print(f"::error::{p.stderr.decode()}")
            sys.exit(1)
        if output := p.stdout.decode().strip():
            print(f"::error::{output}")
            sys.exit(1)
        print(f"Delete asset with id {item.id}")
    assets.clear()


def find_files(paths: str, file_map: str) -> list[File]:
    """
    Find files to upload and filter list with provided patterns.
    Files are included as long as at least one pattern matches.
    """
    print("-- Find files")
    path_list: list[str] = [p for path in paths.split(",") if (p := path.strip())]
    print(f"Paths: {path_list}")
    file_list: list[Path] = []
    for path_name in path_list:
        path = Path(path_name)
        if path.is_file():
            file_list.append(path)
        elif path.is_dir():
            file_list.extend([p for p in path.iterdir() if p.is_file()])
        elif path.exists() is False:
            print(f"::error::Path '{path}' does not exist")
            sys.exit(1)

    file_content_types: dict[str, str] = {}
    invalid_mapping_found = False
    for item in file_map.split(","):
        fn_pattern, _, c_type = item.partition("=")
        fn_pattern = fn_pattern.strip()
        c_type = c_type.strip()
        if fn_pattern == "" or c_type == "":
            print(
                f"::error::Invalid pattern '{item}', use '<fn_pattern>=<content_type>'"
            )
            invalid_mapping_found = True
        file_content_types[fn_pattern] = c_type

    if invalid_mapping_found is True:
        sys.exit(1)
    print(f"File map: {file_content_types}")

    files: list[File] = []
    for path in file_list:
        for fn_pattern, c_type in file_content_types.items():
            if fnmatch.fnmatch(str(path), fn_pattern):
                files.append(File(path.name, path, c_type))
                print(f"Found '{path}' -> '{c_type}'")
                break

    if not files:
        print("::error::No files found")
        sys.exit(1)
    return files


def upload_assets(
    token: str, ctx: dict[str, Any], assets: list[Asset], files: list[File]
) -> None:
    """
    Upload files as release asset.
    https://docs.github.com/en/rest/reference/releases#upload-a-release-asset
    """
    print("-- Upload assets")
    url = re.sub(r"\{.*\}", "", ctx["upload_url"])
    asset_names = {asset.name for asset in assets}
    for file in files:
        if file.name in asset_names:
            print(f"Skip '{file.name}', asset name already exists")
            continue
        cmd = (
            "curl -sS -X POST "
            '-H "Accept: application/vnd.github.v3+json" '
            f'-H "Authorization: token {quote(token)}" '
            f'-H "Content-Type: {quote(file.content_type)}" '
            f"--data-binary {quote(f'@{file.path}')} "
            f"{quote(f'{url}?name={file.name}')}"
        )
        p = subprocess.run(args=cmd, capture_output=True, check=False, shell=True)
        if p.returncode != 0:
            print(p.stderr.decode())
            sys.exit(1)

        data: dict[str, Any] = json.loads(p.stdout.decode())
        if not data.get("id"):
            print(f"::error::{json.dumps(data, indent=2)}")
            sys.exit(1)
        print(f"Successfully uploaded '{file.name}'")


def main():
    parser = ArgumentParser()
    parser.add_argument("--token", required=True, help="GITHUB_TOKEN")
    parser.add_argument(
        "--release_ctx", required=True, help="GitHub Release context (json)"
    )
    parser.add_argument(
        "--file_map",
        required=True,
        help=(
            "Filter and map file names to content types. E.g. "
            "*.whl=application/zip, *.tar.gz=application/gzip"
        ),
    )
    parser.add_argument(
        "--delete_existing_assets", choices=["true", "false"], default="true"
    )
    parser.add_argument(
        "--paths", required=True, help="Comma-separated list of files and / or folders"
    )

    argv = sys.argv[1:]
    args = parser.parse_args(argv)

    token: str = args.token
    release_ctx: dict[str, Any] = json.loads(args.release_ctx)
    file_map: str = args.file_map
    delete_existing_assets = True if args.delete_existing_assets == "true" else False
    paths: str = args.paths

    assets = find_existing_assets(token, release_ctx)
    if delete_existing_assets:
        delete_assets(token, assets)

    files = find_files(paths, file_map)
    upload_assets(token, release_ctx, assets, files)


if __name__ == "__main__":
    main()
