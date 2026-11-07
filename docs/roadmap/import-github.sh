#!/usr/bin/env bash
# Usage: import-github.sh OWNER/REPO [PROJECT_NUMBER OWNER]
set -euo pipefail
repo="${1:?usage: import-github.sh OWNER/REPO [PROJECT_NUMBER OWNER]}"
project="${2:-}"; powner="${3:-}"
dir="$(cd "$(dirname "$0")" && pwd)"
declare -A num

create() { # id title body labels...
  local id="$1" title="$2" body="$3"; shift 3
  local args=() l
  for l in "$@"; do gh label create "$l" --repo "$repo" --force </dev/null >/dev/null 2>&1 || true; args+=(--label "$l"); done
  local url; url=$(gh issue create --repo "$repo" --title "[$id] $title" --body "$body" "${args[@]}" </dev/null)
  num[$id]="${url##*/}"
  if [ -n "$project" ]; then gh project item-add "$project" --owner "$powner" --url "$url" </dev/null >/dev/null; fi
  echo "$id -> $url"
  sleep 1
}

jq -c '.[]' "$dir/epics.json" | while read -r e; do
  create "$(jq -r .id <<<"$e")" "$(jq -r .title <<<"$e")" \
    "$(jq -r '"**Phase:** \(.phase)\n\n\(.summary)\n\n**Exit criteria:** \(.exitCriteria)"' <<<"$e")" \
    $(jq -r '.labels[]' <<<"$e")
done
# Issue numbers do not survive the subshell above, so features/tasks reference parents by ID.
jq -c '.[]' "$dir/features.json" | while read -r f; do
  create "$(jq -r .id <<<"$f")" "$(jq -r .title <<<"$f")" \
    "$(jq -r '"Epic: \(.epic)\n\nAcceptance criteria: \(.acceptanceCriteria|join(", "))"' <<<"$f")" \
    $(jq -r '.labels[]' <<<"$f")
done
jq -c '.[] | select(.status != "Done")' "$dir/tasks.json" | while read -r t; do
  create "$(jq -r .id <<<"$t")" "$(jq -r .title <<<"$t")" \
    "$(jq -r '"Feature: \(.feature) · Epic: \(.epic)"' <<<"$t")" \
    $(jq -r '.labels[]' <<<"$t")
done
