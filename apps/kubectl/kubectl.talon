tag: terminal
-
cube [control]: insert(user.kubectl())

cube create: insert(user.kubectl_create())
cube expose: insert(user.kubectl_expose())
cube run: insert(user.kubectl_run())
cube set: insert(user.kubectl_set())

cube explain: insert(user.kubectl_explain())
cube get: insert(user.kubectl_get())
cube edit: insert(user.kubectl_edit())
cube delete: insert(user.kubectl_delete())

cube rollout: insert(user.kubectl_rollout())
cube scale: insert(user.kubectl_scale())
cube auto scale: insert(user.kubectl_autoscale())

cube certificate: insert(user.kubectl_certificate())
cube cluster (info | information): insert(user.kubectl_cluster_info())
cube top: insert(user.kubectl_top())
cube (cord | cordon): insert(user.kubectl_cordon())
cube (uncord | uncordon): insert(user.kubectl_uncordon())
cube drain: insert(user.kubectl_drain())
cube taint: insert(user.kubectl_taint())

cube describe: insert(user.kubectl_describe())
cube logs: insert(user.kubectl_logs())
cube attach: insert(user.kubectl_attach())
cube exec: insert(user.kubectl_exec())
cube port forward: insert(user.kubectl_port_forward())
cube proxy: insert(user.kubectl_proxy())
cube copy: insert(user.kubectl_cp())
cube auth: insert(user.kubectl_auth())

cube diff: insert(user.kubectl_diff())
cube apply: insert(user.kubectl_apply())
cube patch: insert(user.kubectl_patch())
cube replace: insert(user.kubectl_replace())
cube wait: insert(user.kubectl_wait())
cube convert: insert(user.kubectl_convert())
cube customize: insert(user.kubectl_kustomize())

cube label: insert(user.kubectl_label())
cube annotate: insert(user.kubectl_annotate())
cube completion: insert(user.kubectl_completion())

cube interface resources: insert(user.kubectl_api_resources())
cube interface versions: insert(user.kubectl_api_versions())
cube config: insert(user.kubectl_config())
cube plugin: insert(user.kubectl_plugin())
cube version: insert(user.kubectl_version())

cube {user.kubectl_action} {user.kubectl_object}: "kubectl {kubectl_action} {kubectl_object}"

cube detach:
    key("ctrl-p")
    key("ctrl-q")
cube shell:
    insert("kubectl exec -it  -- /bin/bash")
    key("left")
    key("left")
    key("left")
    key("left")
    key("left")
    key("left")
    key("left")
    key("left")
    key("left")
    key("left")
    key("left")
    key("left")
    key("left")