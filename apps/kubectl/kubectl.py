from talon import Context, Module

mod = Module()
mod.tag("kubectl", desc="tag for enabling kubectl commands in your terminal")
kubectl = "kubectl"

ctx = Context()
ctx.matches = r"""
tag: user.kubectl
"""

mod.list("kubectl_action", desc="actions performed by kubectl")

mod.list("kubectl_object", desc="objects performed by kubectl")
ctx.lists["user.kubectl_object"] = (
    "nodes",
    "jobs",
    "pods",
    "namespaces",
    "services",
    "events",
    "deployments",
    "replicasets",
    "daemonsets",
    "configmaps",
    "secrets",
    "endpoints",
    "ingress",
    "persistentvolumes",
    "persistentvolumeclaims",
)

mod.list("kubectl_output_format_object", desc="-o parameters, so output formatters")
