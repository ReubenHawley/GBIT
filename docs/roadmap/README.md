# GBIT roadmap

Source of truth for planned work, derived from `docs/GBIT_Architecture_Proposal.html` (section 09 and the acceptance criteria).

| File | Contents |
|---|---|
| `epics.json` | 6 epics (E0 foundation, E1-E4 the proposal's four phases, E5 future platform) |
| `features.json` | Features, each linked to an epic and to acceptance criteria (AC-xx) |
| `tasks.json` | Tasks, each linked to a feature and epic; `status` is `Todo` or `Done` |

Hierarchy: epic `features[]` -> feature `tasks[]`; tasks carry `feature` and `epic` back-references.

## Import into GitHub

`import-github.sh` creates one issue per epic, feature and task (with labels), skipping tasks marked `Done`, and links each child to its parent in the issue body. Requires `gh` and `jq`.

```bash
gh auth login
./docs/roadmap/import-github.sh OWNER/REPO [PROJECT_NUMBER --owner OWNER]
```

Without a project number the issues are only created; with one, they are also added to that GitHub Project.

## Specs

`specs/<ID>.md` holds the full specification for every epic, feature and task (summary, requirements, acceptance criteria, test-first plan, dependencies, definition of done). They are the text of the corresponding GitHub issues. `issue-map.json` maps roadmap IDs to issue numbers.

To change a spec: edit the data in `specs/spec_*.py`, run `python3 -I docs/roadmap/specs/render.py docs/roadmap/issue-map.json`, then update the issue body with `gh issue edit <n> --body-file docs/roadmap/specs/<ID>.md`.
