#!/bin/sh
# Download the unmodified Hermes Agent v0.22.7 files the tests load.
# Every file must match its SHA-256 pin, or nothing is written.
# Output goes to tests/.hermes-src, which git ignores.
#
# The tag v0.22.7 points at commit b200f5bc60e31588ba2cb60e288029c4a54ba5fa.
# The pins were taken from the files at the tag on 2026-11-19.
# They match the copy fetched for the 0.1.0 tests on 2026-11-04.
# That fetch also kept the main branch copy of plugin-catalog/README.md.
# It was identical to the tag copy, and only the tag copy is fetched here.

set -eu

base=https://raw.githubusercontent.com/NousResearch/hermes-agent/refs/tags/v0.22.7
dest=$(cd "$(dirname "$0")" && pwd)/.hermes-src

# SHA-256, local file name, path in the upstream repository.
pins='08731e1f0f932edda7e74af4bae4c2f16870ade04b8fc31173380544bc42baf8 plugins_discovery.py hermes_cli/plugins_discovery.py
89b30e679247a628c7dad93c573afa9f3f22529015b26397de24f5067ff7fc06 plugins_manifest.py hermes_cli/plugins_manifest.py
91a93ed1ad73a146d9a5f32c659ea481260fcf173f01c175f7aea6c781c07ca8 plugins_loader.py hermes_cli/plugins_loader.py
3d2a8cfa5c2e574e8a8e11c320be7a860b4dacb06d87055ad36ae86b1ec97cef agent_plugins.py hermes_cli/agent_plugins.py
f9bccfcfcdf37c5068590c0f7cf24304dd854fec5e2130c1faba1ad2b07518be plugin_validate.py hermes_cli/plugin_validate.py
44b0d33c9b86535dda3b5bde20cc06b33991ec926e293979c670105ed6dc5b5b validate_plugin_catalog.py scripts/validate_plugin_catalog.py
529a1e0e89135d0edbd1024c20655586e52a7915c6dc83bd49e7573614d7aa8f mcp_tool_config.py tools/mcp_tool_config.py
50fb0d704de1f1a1306b55f8db3d7a6a0d97f1343865d5c227069593ec6e2f19 catalog-submission.md website/docs/developer-guide/plugins/catalog-submission.md
5d9ab744164bfc1c48c99d0f3051e4cc9d203cebf355287727eebe7fb176a5f3 catalog-README-v0.22.7.md plugin-catalog/README.md'

if command -v sha256sum >/dev/null 2>&1; then
  sha256() { sha256sum "$1" | cut -d ' ' -f 1; }
elif command -v shasum >/dev/null 2>&1; then
  sha256() { shasum -a 256 "$1" | cut -d ' ' -f 1; }
else
  echo "fetch-hermes: sha256sum or shasum is required" >&2
  exit 1
fi

# Downloads wait beside the destination until every pin has passed.
work=$(mktemp -d "$dest.XXXXXX")
trap 'rm -rf "$work"' EXIT
trap 'exit 1' HUP INT TERM

failed=0
count=0
while read -r pin name path; do
  if ! curl -fsSL --proto '=https' --retry 5 --max-time 60 -o "$work/$name" "$base/$path"; then
    echo "fetch-hermes: download failed: $base/$path" >&2
    exit 1
  fi
  count=$((count + 1))
  actual=$(sha256 "$work/$name")
  if [ "$actual" = "$pin" ]; then
    echo "ok        $actual  $name"
  else
    echo "MISMATCH  $name: expected $pin, got $actual" >&2
    failed=1
  fi
done <<EOF
$pins
EOF

if [ "$failed" -ne 0 ]; then
  echo "fetch-hermes: checksum mismatch, $dest was not changed" >&2
  exit 1
fi

rm -rf "$dest"
mv "$work" "$dest"
echo "fetch-hermes: $count files verified in $dest"
