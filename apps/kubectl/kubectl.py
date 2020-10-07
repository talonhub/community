from talon import Module, Context

mod = Module()

kubectl = "kubectl"


ctx = Context()
ctx.matches = r"""
tag: terminal
"""

mod.list("kubectl_action", desc="actions performed by kubectl")
ctx.lists["self.kubectl_action"] = ("get", "delete", "describe", "label")

mod.list("kubectl_object", desc="objects performed by kubectl")
ctx.lists["self.kubectl_object"] = (
    "nodes",
    "jobs",
    "pods",
    "namespaces",
    "services",
    "events",
    "deployments",
    "replicasets",
    "daemonsets",
)
