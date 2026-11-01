# ansible-lint

Reviewed 2026-11-01. **Add ansible-lint** as the Ansible gate, in a new Ansible category. It checks playbook practices and exits non-zero on violations. Molecule stays out: it runs tests. ansible-review does not start against current ansible-lint. Steampunk Spotter stays out: a scan needs their API.

## Currency

Checked against GitHub, GitLab and PyPI on 2026-11-01.

- [ansible-lint v26.10.0](https://github.com/ansible/ansible-lint/releases/tag/v26.10.0) was published 2026-10-12, and [v26.10.1](https://github.com/ansible/ansible-lint/releases/tag/v26.10.1) the next day (a cryptography pin). [PyPI 26.10.1](https://pypi.org/project/ansible-lint/26.10.1/) matches. The repository is not archived. Licence file is [GPL-3.0](https://github.com/ansible/ansible-lint/blob/v26.10.1/COPYING).
- Latest commit on that date: [67a4871784](https://github.com/ansible/ansible-lint/commit/67a4871784) (2026-10-30), a stderr-color fix. The contributors API lists `ssbarnea` first. The v26.10.1 release was published by `shvenkat-rh`.
- The repository API reported 3933 stars and 120 open issues. A search for the open `critical` label returned 0. The [security advisories](https://github.com/ansible/ansible-lint/security) list was empty. Open bugs that matter to a gate include [CodeClimate severity for load-failure](https://github.com/ansible/ansible-lint/issues/5226), [duplicate filters ignored](https://github.com/ansible/ansible-lint/issues/5199), and a [possible `latest[git]` false positive](https://github.com/ansible/ansible-lint/issues/5217). None of these were reproduced here.

## Alternatives

| Tool | What it is | Decision |
|---|---|---|
| [ansible-lint](https://docs.ansible.com/projects/lint/) | Playbook, role and collection practices. Default run fails on violations. JSON, SARIF, `--fix`. | Add. Roles and collections are from the docs; the run below is playbooks and one extra YAML file. |
| [ansible-review](https://github.com/willthames/ansible-review) | Older review wrapper around ansible-lint. PyPI [0.13.9](https://pypi.org/project/ansible-review/0.13.9/) uploaded 2018-11-25. Last push 2021-04-01. 226 stars, MIT, not archived. | Reject. `pip install ansible-review==0.13.9` on 2026-11-01 pulled ansible-lint 26.10.1, then `ansible-review --help` exited 1: `ImportError: cannot import name 'default_rulesdir'`. |
| [Steampunk Spotter](https://gitlab.com/xlab-steampunk/steampunk-spotter-client/spotter-cli) | Hosted scanner. CLI [6.6.0](https://pypi.org/project/steampunk-spotter/6.6.0/) uploaded 2026-10-14. Public GitLab project, Apache-2.0, 6 stars, last activity 2026-10-29. | Reject as this gate. Not run: [the CLI docs](https://spotter.steampunk.si/docs/cli/) send the scan to their API and the GitHub Action takes an API token. [Their comparison](https://steampunk.si/spotter/blog/why-use-steampunk-spotter-when-we-have-ansible-lint/) says Spotter does not check style and that ansible-lint should run first. |
| [Molecule](https://github.com/ansible/molecule) | Test runner. [v26.10.0](https://github.com/ansible/molecule/releases/tag/v26.10.0) published 2026-10-12. MIT, 4162 stars, last push 2026-10-31. | Leave out. Not a linter. Not run. |

`ansible-playbook --syntax-check` was not run separately. The `min` profile printed by `ansible-lint -P` already lists `syntax-check`.

## What was run

ansible-lint 26.10.1 (`ansible-lint --version` also printed ansible-core 2.21.5 and ansible-compat 26.10.0) on 2026-11-01. Every lint invocation used `--offline`. A run without `--offline` was not made: the help text says that mode installs `requirements.yml` and refreshes schemas. Fixtures are in [fixtures/ansible](fixtures/ansible/). Nothing here is deployed.

[The runner](fixtures/ansible/run.py) copies the fixtures, then checks the exit codes below. It needs both binaries on `PATH`:

```sh
python3 research/fixtures/ansible/run.py /tmp/ansible-lint-results
```

| Case | Command | Exit |
|---|---|---|
| Named play, `ansible.builtin.debug` | `ansible-lint --offline playbook.yml` | 0. stderr: production profile passed |
| Unnamed play, `shell` and `command` without `changed_when` | same | 2. Rules included `name`, `command-instead-of-shell`, `fqcn`, `no-changed-when` |
| Same broken playbook | `--profile min` | 0. stderr said the production profile passed. `--profile basic` on the same file exited 2. The summary is wrong for a gate: read from installed `app.py`, a profile with no counted failures becomes `passed_profile`, and `--profile min` does not report the basic rules |
| `debug:` instead of the fully qualified name | `--fix` | 8, file rewritten to `ansible.builtin.debug`, and a later run exited 0. Installed `constants.py` names 8 `FIXED_VIOLATIONS` |
| Directory with a valid playbook and `notes.yaml` (duplicate key, line longer than 160) | `ansible-lint --offline` with no paths | 2, both findings in `notes.yaml` (`yaml[key-duplicates]`, `yaml[line-length]`) |
| Same `notes.yaml` | `yamllint` 1.38.0, which pip installed as a dependency of ansible-lint | 1, `key-duplicates` |
| Custom rule in `rules/no_debug.py` | `--offline -r rules` | 2, `no-debug` |
| `.ansible-lint` with `skip_list: 12` | `ansible-lint --offline` | 3, invalid configuration |
| `.ansible-lint` that is not valid YAML | same | 1, traceback |
| Missing path | `ansible-lint --offline /tmp/.../no-such.yml` | 2, `load-failure` |
| Broken playbook | `--offline -f json` | 2, stdout is a JSON list |

The `yaml` rule imports yamllint (read from installed `rules/yaml_rule.py`). With no paths, ansible-lint walked a YAML file that is not a playbook and failed it. That overlaps yamllint, which is still under review and is not a recommendation here. It does not overlap Hadolint, TFLint, Kubeconform or check-jsonschema: those look at different files. Do not add a second yamllint on the YAML ansible-lint already walks.

`--strict` is documented as failing on warnings, and the installed tag list says `experimental` rules warn by default. This run did not produce a warning-only match, so that flag was not shown to change an exit code.

## Decision

Add ansible-lint. The gate is `ansible-lint --offline` with no `--fix` and no `--profile min`: violations exit 2, `--fix` exits 8 after rewriting, and `--profile min` exited 0 on a playbook the default run rejects. GPL-3.0. Python, not a native binary. Pin the version; the package installs ansible-core.
