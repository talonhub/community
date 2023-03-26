# Contributing

Anyone is welcome to submit PRs and report issues.

## Guidelines for contributions

### Grammar Guidelines

- Any addition to the global grammar will be scrutinized a bit more thoroughly. The more specific a new context, the less scrutiny that is typically applied.
- To reduce the chance of misrecognitions, is strongly preferred to either (1) match an existing command already in use elsewhere in the repository for consistency or (2) introduce a single command for new functionality.  
- New grammars should follow the [subject][verb] standard where-ever possible.
- Pull requests that mainly introduce alternative voice commands may be rejected. This is necessary to avoid introducing additional pain points for existing users of the repository; changing the grammar without any notice is likely to confusion
    - Exceptions to this policy include efforts to reduce common conflicts, and refactors to introduce common commands across multiple applications. In either case, the [deprecation system](https://github.com/knausj85/knausj_talon/blob/main/core/deprecations.py) should be used to warn existing users of the change. 
- For new web apps, ensure the domain is used to minimize potential mismatches; see
  https://github.com/knausj85/knausj_talon/blob/main/apps/README.md.
- New applications should use [tags](https://talon.wiki/unofficial_talon_docs/#tags) to support the appropriate generic command grammars where appropriate:  
```
core/windows_and_tabs/tabs.talon
tags/browser/
tags/find_and_replace/
tags/line_commands/
tags/multiple_cursors/
tags/snippets/
tags/splits/
tags/terminal/
```

- New programming languages should support the appropriate generic grammars where possible; see the `lang/tags/` directory.

- For Mac OS X, the bundle id should be used for defining app contexts, rather than the name.

- For Windows, both the friendly app name and exe name should be used for defining app contexts when they are different. For some people, the MUICache breaks.