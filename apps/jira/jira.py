from talon import Context, Module

mod = Module()

mod.list("jira_epics", desc="list of jira epics")
mod.list("jira_fix_versions", desc="list of jira fix versions")
mod.list("jira_components", desc="list of jira fix components")
mod.list("jira_alias", desc="list of jira user aliases")
mod.list("jira_labels", desc="list of jira user labels")
mod.list("jira_projects", desc="list of jira project keys")
mod.list("jira_types", desc="list of jira types")
mod.tag(
    "jira",
    desc="tag used to enable jira commands",
)

@mod.action_class
class Actions:
    def jira_assign(employee: str):
        """assigns the task to the desired employee in jira"""
    
    def jira_label(labels: str):
        """Adds the desired labels to the jira task"""
    
    def jira_epics(epics: str):
        """Add the desired epics to the jira task"""
    
    def jira_fix_versions(versions: str):
        """Adds the desired fixed versions to the jira task"""
    
    def jira_components(components: str):
        """Adds the desired components to the jira task"""
        
       
        