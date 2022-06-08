from talon import Context, Module

mod = Module()
mod.tag("kubectl", desc="tag for enabling kubectl commands in your terminal")
kubectl = "kubectl"

ctx = Context()
ctx.matches = r"""
tag: user.kubectl
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
