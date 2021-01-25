#!/usr/bin/env bashio
declare -a integrations
declare integration_path

shopt -s globstar nullglob
for manifest in **/manifest.json; do
    integration_path=$(dirname "${manifest}")
    integrations+=(--integration-path "${integration_path}")
done

if [[ ${#integrations[@]} -eq 0 ]]; then
    bashio::exit.nok "No integrations found!"
fi

echo "* [WARNING] [TRANSLATIONS] Invalid switch.en.json: Device class need to start with 'test__'. Key string1 is invalid. See https://developers.home-assistant.io/docs/internationalization/core#stringssensorjson for dictionary value @ data['state']. Got {'string1': 'Value 1', 'string2': 'Value 2'}"
echo "* [ERROR] [MANIFEST] Invalid manifest: Documentation url is not prefixed with https for dictionary value @ data['documentation']. Got 'http://example.com'"

exec python3 -m script.hassfest --action validate "${integrations[@]}"