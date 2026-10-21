# Correct standard Inno Setup registry discovery

## Goal

Remove three stray spaces in the standard uninstall registry key used by
`get_path_from_registry`. Add a regression through the existing
`InnosetupCompiler` default factory in tests/test_basic.py. Expected change:
one source line and approximately 25 test lines. No real registry/compiler action.

## State

Exact origin: `git@github.com:accessibleapps/innosetup_builder.git`. Branch
`modernize/task6-innosetup_builder` is in the isolated task-6 worktree. Current
base is `5e4c0f2d565a7e0a063a15248c266615126ed532`, containing merged baseline
PR #2. Open draft PR #1 is https://github.com/accessibleapps/innosetup_builder/pull/1 .
Its reviewed source/test head is `8d50a01e02a1cfbd18157321cdb1aed4f74e18fb`.
Hosted pull_request run 39517006176 passed all 70 tests and the package build
on Windows Python 3.13.16. `.github/workflows/test.yml` supplies that gate.
Canonical tracked files and untracked docs/history/CLAUDE/lock are preserved;
the feature worktree's untracked uv.lock is excluded. Both pre-rebase backup
refs remain at `d844bfa1d73ed0d7c93b7d477b23b575db5fe819`.

## Decisions and why

Read global instructions, canonical untracked CLAUDE, README, pyproject, single
source module and existing basic/advanced tests. Version 0.2.3 supports >=3.8.6;
no dependency/support change. Standard key has `CurrentVersion   \\Uninstall`,
while fallback uses `CurrentVersion\\Uninstall`. The actual compiler default
factory calls this function, so a standard installation can be missed before the
unrelated WOW64 fallback. Use fake winreg at this external boundary, invoking the
real constructor; require the exact standard key and successful base_path.

The initial full-test authority question was settled by the coordinator. The
baseline now runs the full existing pytest suite and nonpublishing Python
package build in hosted CI. No real compiler, signing or registry mutation is
part of this regression or gate.

## Surprises

Canonical CLAUDE and uv.lock are untracked user files; preserve both. Baseline
PR #2 fixed the Windows path assertions and isolated render-only tests from
installed Inno Setup. Those changes remain inherited from the current base.

## Historical verification

Initial regression before fix, on original base
`d2e5a19773286c13b27949209a2554c83a822eff`: `uv run pytest tests/test_basic.py -k
default_compiler_finds_standard_registry_install` failed (1 failed, 11
deselected) with `FileNotFoundError: Inno Setup 6 is not installed`; fake standard
registry rejected the malformed CurrentVersion key and WOW64 fallback.

Same focused command after one-line source fix: 1 passed, 11 deselected, 0.41 s.
The fake registry attribute is installed with raising=False so the test also
works where optional winreg is absent; no real registry access occurs.

The initially authorized full `uv run pytest tests` reported 69 passed, 1 failed,
2.60 s, Python 3.13.15/pytest 9.1.1. At that original base,
`test_compiler_paths_with_base` compared native Windows Path output
`\\test\\path\\Languages` to `/test/path/Languages`. The source fix touches only a
registry key; the failing test supplies explicit base_path and bypasses registry.
That failure was unchanged by the registry fix and was reported privately.
It was subsequently repaired in baseline PR #2 with exact Path assertions;
the current hosted suite is green, as recorded in State.

There was no manifest change or tracked lock; resolver-created isolated
uv.lock/caches were excluded from the original source commit.

Final fake-registry run after portable monkeypatch: 1 passed, 11 deselected,
0.42 s. The then-failing base assertion bypassed the changed registry path.
No hooksPath or active hooks were found in the initial implementation.
Ordinary `git diff --check` treated the existing CRLF lines as trailing
whitespace. The CRLF-aware `git -c core.whitespace=cr-at-eol diff --check` passes;
line endings were preserved. The original final-newline hunk in test_basic.py
was absorbed by baseline PR #2 and is no longer part of the feature diff.
The reviewed source/test diff contains no secrets, user samples, generated
fixtures, unrelated source or resolver outputs.

## Next step

Actual Claude review accepted the registry source/test change at 8d50a01e and
requested only this note's current-state correction. Return the local note-only
commit/diff for coordinator approval before publication. Then obtain actual
Claude follow-up and green hosted checks for the final published head before
any ready/merge action. Keep source, tests, manifests, workflow and backup refs
unchanged; do not rerun local CI for this note-only correction.
