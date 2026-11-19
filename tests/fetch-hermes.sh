#!/bin/sh
# Download the unmodified Hermes Agent v0.22.7 files the tests load.
# tests/hermes-pins.txt lists each file with its SHA-256 pin.
# Every file must match its pin, or nothing is written.
# Output goes to tests/.hermes-src, which git ignores.

set -eu

base=https://raw.githubusercontent.com/NousResearch/hermes-agent/refs/tags/v0.22.7
here=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
pins_file=$here/hermes-pins.txt
dest=$here/.hermes-src

# Hash from stdin, so the path never reaches the output and needs no escaping.
if command -v sha256sum >/dev/null 2>&1; then
  sha256() { sha256sum < "$1" | cut -d ' ' -f 1; }
elif command -v shasum >/dev/null 2>&1; then
  sha256() { shasum -a 256 < "$1" | cut -d ' ' -f 1; }
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
  case $pin in '' | '#'*) continue ;; esac
  case $name in '' | */* | .*)
    echo "fetch-hermes: bad file name in $pins_file: $name" >&2
    exit 1
    ;;
  esac
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
done < "$pins_file"

if [ "$count" -eq 0 ]; then
  echo "fetch-hermes: no pins in $pins_file" >&2
  exit 1
fi
if [ "$failed" -ne 0 ]; then
  echo "fetch-hermes: checksum mismatch, $dest was not changed" >&2
  exit 1
fi

# Each rename swaps in one verified file. An interrupted or concurrent run
# never empties the folder or nests a download folder inside it.
mkdir -p "$dest"
for file in "$work"/*; do
  mv -f "$file" "$dest/"
done
echo "fetch-hermes: $count files verified in $dest"
