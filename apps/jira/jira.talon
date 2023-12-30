tag: browser
browser.host: jira.com
-
assign {user.jira_alias}:
    key(a)
    insert(jira_alias)

label {user.jira_labels}:
    user.jira_label(jira_labels)

fix {user.jira_fix_versions}:
    user.jira_fix_versions(jira_fix_versions)

epic {user.jira_epics}:
    user.jira_epics(jira_epics)
    
create issue:
    key(c)

go dashboard:
    key(g d)

go project:
    key(g p)

go issue navigator: 
    key(g i)
