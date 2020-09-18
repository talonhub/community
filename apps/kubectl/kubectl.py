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
    "",
)


@mod.action_class
class Actions:
    """Map the first level CLI for kubernetes ``kubectl --help``"""

    def kubectl() -> str:
        """Root command for kubernetes CLI"""
        return kubectl

    # Basic Commands (Beginner):

    def kubectl_create() -> str:
        """Create a resource from a file or from stdin."""
        return f"{kubectl} create "

    def kubectl_expose() -> str:
        """Take a replication controller, service, deployment or pod and expose it as a new Kubernetes Service"""
        return f"{kubectl} expose "

    def kubectl_run() -> str:
        """Run a particular image on the cluster"""
        return f"{kubectl} run "

    def kubectl_set() -> str:
        """Set specific features on objects"""
        return f"{kubectl} set "

    # Basic Commands (Intermediate):

    def kubectl_explain() -> str:
        """Documentation of resources"""
        return f"{kubectl} explain "

    def kubectl_get() -> str:
        """Display one or many resources"""
        return f"{kubectl} get "

    def kubectl_edit() -> str:
        """Edit a resource on the server"""
        return f"{kubectl} edit "

    def kubectl_delete() -> str:
        """Delete resources by filenames, stdin, resources and names, or by resources and label selector"""
        return f"{kubectl} delete "

    # Deploy Commands:

    def kubectl_rollout() -> str:
        """Manage the rollout of a resource"""
        return f"{kubectl} rollout "

    def kubectl_scale() -> str:
        """Set a new size for a Deployment, ReplicaSet, Replication Controller, or Job"""
        return f"{kubectl} scale "

    def kubectl_autoscale() -> str:
        """Auto-scale a Deployment, ReplicaSet, or ReplicationController"""
        return f"{kubectl} autoscale "

    # Cluster Management Commands:

    def kubectl_certificate() -> str:
        """Modify certificate resources."""
        return f"{kubectl} certificate "

    def kubectl_cluster_info() -> str:
        """Display cluster info"""
        return f"{kubectl} cluster-info "

    def kubectl_top() -> str:
        """Display Resource (CPU/Memory/Storage) usage."""
        return f"{kubectl} top "

    def kubectl_cordon() -> str:
        """Mark node as unschedulable"""
        return f"{kubectl} cordon "

    def kubectl_uncordon() -> str:
        """Mark node as schedulable"""
        return f"{kubectl} uncordon "

    def kubectl_drain() -> str:
        """Drain node in preparation for maintenance"""
        return f"{kubectl} drain "

    def kubectl_taint() -> str:
        """Update the taints on one or more nodes"""
        return f"{kubectl} taint "

    # Troubleshooting and Debugging Commands:

    def kubectl_describe() -> str:
        """Show details of a specific resource or group of resources"""
        return f"{kubectl} describe "

    def kubectl_logs() -> str:
        """Print the logs for a container in a pod"""
        return f"{kubectl} logs "

    def kubectl_attach() -> str:
        """Attach to a running container"""
        return f"{kubectl} attach "

    def kubectl_exec() -> str:
        """Execute a command in a container"""
        return f"{kubectl} exec "

    def kubectl_port_forward() -> str:
        """Forward one or more local ports to a pod"""
        return f"{kubectl} port-forward "

    def kubectl_proxy() -> str:
        """Run a proxy to the Kubernetes API server"""
        return f"{kubectl} proxy "

    def kubectl_cp() -> str:
        """Copy files and directories to and from containers."""
        return f"{kubectl} cp "

    def kubectl_auth() -> str:
        """Inspect authorization"""
        return f"{kubectl} auth "

    # Advanced Commands:

    def kubectl_diff() -> str:
        """Diff live version against would-be applied version"""
        return f"{kubectl} diff "

    def kubectl_apply() -> str:
        """Apply a configuration to a resource by filename or stdin"""
        return f"{kubectl} apply "

    def kubectl_patch() -> str:
        """Update field(s) of a resource using strategic merge patch"""
        return f"{kubectl} patch "

    def kubectl_replace() -> str:
        """Replace a resource by filename or stdin"""
        return f"{kubectl} replace "

    def kubectl_wait() -> str:
        """Experimental: Wait for a specific condition on one or many resources."""
        return f"{kubectl} wait "

    def kubectl_convert() -> str:
        """Convert config files between different API versions"""
        return f"{kubectl} convert "

    def kubectl_kustomize() -> str:
        """Build a kustomization target from a directory or a remote url."""
        return f"{kubectl} kustomize "

    # Settings Commands:

    def kubectl_label() -> str:
        """Update the labels on a resource"""
        return f"{kubectl} label "

    def kubectl_annotate() -> str:
        """Update the annotations on a resource"""
        return f"{kubectl} annotate "

    def kubectl_completion() -> str:
        """Output shell completion code for the specified shell (bash or zsh)"""
        return f"{kubectl} completion "

    # Other Commands:

    def kubectl_api_resources() -> str:
        """Print the supported API resources on the server"""
        return f"{kubectl} api-resources "

    def kubectl_api_versions() -> str:
        """Print the supported API versions on the server, in the form of 'group/version'"""
        return f"{kubectl} api-versions "

    def kubectl_config() -> str:
        """Modify kubeconfig files"""
        return f"{kubectl} config "

    def kubectl_plugin() -> str:
        """Provides utilities for interacting with plugins."""
        return f"{kubectl} plugin "

    def kubectl_version() -> str:
        """Print the client and server version information"""
        return f"{kubectl} version "
