# Correct standard Inno Setup registry discovery

## Goal

Remove three stray spaces in the standard uninstall registry key used by
`get_path_from_registry`. Add a regression through the existing
`InnosetupCompiler` default factory in tests/test_basic.py. Expected change:
one source line and approximately 25 test lines. No real registry/compiler action.

## State

Worker thread `01a15b4c-eda9-7420-bdff-05199b061038`; exact origin
`git@github.com:accessibleapps/innosetup_builder.git`. Fresh master base
`d2e5a19773286c13b27949209a2554c83a822eff`. Branch
`modernize/task6-innosetup_builder` created directly under task-6 worktrees after
checking absence. Canonical tracked clean; 541 untracked docs/history/lock files
preserved. No open PRs or hosted workflows.

## Decisions and why

Read global instructions, canonical untracked CLAUDE, README, pyproject, single
source module and existing basic/advanced tests. Version 0.2.3 supports >=3.8.6;
no dependency/support change. Standard key has `CurrentVersion   \\Uninstall`,
while fallback uses `CurrentVersion\\Uninstall`. The actual compiler default
factory calls this function, so a standard installation can be missed before the
unrelated WOW64 fallback. Use fake winreg at this external boundary, invoking the
real constructor; require the exact standard key and successful base_path.

Focused actively authored tests/test_basic.py may run under global instructions.
No full test command is documented despite six pytest files and test/dev
dependencies; coordinator was asked to settle full test authority. Never replace
it with a real compiler/build action.

## Surprises

Canonical CLAUDE and uv.lock are untracked user files; preserve both. Tests
contain path-string assumptions that may differ on Windows; do not silently fix
unrelated failures.

## Next step

Regression before fix: `uv run pytest tests/test_basic.py -k
default_compiler_finds_standard_registry_install` failed (1 failed, 11
deselected) with `FileNotFoundError: Inno Setup 6 is not installed`; fake standard
registry rejected the malformed CurrentVersion key and WOW64 fallback.

Same focused command after one-line source fix: 1 passed, 11 deselected, 0.41 s.
The fake registry attribute is installed with raising=False so the test also
works where optional winreg is absent; no real registry access occurs.

Coordinator explicitly authorized all six existing pytest files as the full
intended check derived from existing test/dev dependencies and source files.
`uv run pytest tests`: 69 passed, 1 failed, 2.60 s, Python 3.13.15/pytest 9.1.1.
Existing `test_compiler_paths_with_base` compares native Windows Path output
`\\test\\path\\Languages` to `/test/path/Languages`. The source fix touches only a
registry key; the failing test supplies explicit base_path and bypasses registry.
Its assertions and path properties are unchanged from the fresh base. Do not
alter the unrelated assertion. Coordinator authorized committing this coherent
fix with the full-check limitation reported privately.

No manifest change or tracked lock; resolver-created isolated uv.lock/caches are
excluded from the source commit. Commit source, test and this note only after
diff/hook review; return exact patch and concise proposed PR before publication.

Final fake-registry run after portable monkeypatch: 1 passed, 11 deselected,
0.42 s. Unrelated base assertion was inspected with git show and is identical;
it bypasses the changed registry path. No hooksPath or active hooks found.
Ordinary `git diff --check` treated the existing CRLF lines as trailing
whitespace. The CRLF-aware `git -c core.whitespace=cr-at-eol diff --check` passes;
line endings are preserved. apply_patch also supplies the missing final newline
in test_basic.py. Reviewed diff contains no secrets, user samples, generated
fixtures or unrelated source. No resolver outputs are staged.
