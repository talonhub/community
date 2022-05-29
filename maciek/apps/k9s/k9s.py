from talon import Context, Module

mod = Module()
mod.tag("k9s", desc=".")
mod.apps.k9s = """
win.title: /k9s/
"""
mod.list("k8s_resources", desc="")

k8s_resources = {
    "ingresses": "ingresses",
    "secrets": "secrets",
    "deployments": "deployments",
    "pods": "pods",
    "certs": "certificates",
    "certificates": "certificates",
    "services": "services",
    "configmaps": "configmap",
    "challenges": "challenges",
}

ctx = Context()
ctx.matches = r"""
app: k9s
"""


ctx.lists["self.k8s_resources"] = k8s_resources
