tag: browser
tag: user.jira
-
assign {user.jira_alias}:
    key(a)
    insert(jira_alias)

ping {user.jira_alias}:
    # alias = "@{jira_alias}"
    # insert("@")
    # sleep(250ms)
    # insert("{jira_alias}")
    user.paste("{jira_alias}")
    sleep(250ms)
    key(space)
    # sleep(500ms)
    # key(enter)
    # sleep(500ms)
    # key(space)

label {user.jira_labels}:
    insert(jira_labels)

fix {user.jira_fix_versions}:
    # user.jira_fix_versions(jira_fix_versions)
    insert(jira_fix_versions)
    sleep(100ms)
    key(enter)

epic {user.jira_epics}:
    insert(jira_epics)
    sleep(100ms)
    key(enter)
    
create issue:
    key(c)

go dashboard:
    key(g d)

go project:
    key(g p)

go issue navigator: 
    key(g i)
