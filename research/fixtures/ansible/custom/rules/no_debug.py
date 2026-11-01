"""Fixture rule: flag debug tasks."""

from ansiblelint.rules import AnsibleLintRule


class NoDebugRule(AnsibleLintRule):
    """debug tasks are not allowed in this fixture."""

    id = "no-debug"
    description = "debug tasks are not allowed"
    severity = "HIGH"
    tags = ["custom"]
    version_changed = "1.0.0"

    def matchtask(self, task, file=None):
        module = task["action"].get("__ansible_module__", "")
        if module in {"debug", "ansible.builtin.debug"}:
            return "debug is not allowed"
        return False
