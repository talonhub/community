from typing import Dict, Optional
import webbrowser
from talon import ctrl, ui, Module, Context, actions, clip, app
from dataclasses import dataclass
from things3.things3 import Things3
import io
import csv

ctx = Context()
mod = Module()
apps = mod.apps
apps.things3 = """
app.name: Things
"""
ctx.matches = r"""
app: things3
"""

mod.list("things_tag", desc="Tags in Things")
mod.list("things_tag_with_shortcut", desc="Tags in Things within an assigned shortcut")
mod.list("things_project", desc="Areas and projects in Things")

things = Things3()


@dataclass
class Tag:
    uuid: str
    title: str
    shortcut: Optional[str]


@dataclass
class Project:
    uuid: str
    title: str


raw_areas = things.get_areas()
raw_projects = things.get_projects()
sql_query = f"""
SELECT TAG.title, TAG.shortcut, TAG.uuid
FROM {things.TABLE_TAG} AS TAG
"""
tags = [Tag(**raw_tag) for raw_tag in things.execute_query(sql_query)]
projects = [
    Project(uuid=raw_project["uuid"], title=raw_project["title"])
    for raw_project in raw_areas + raw_projects
]

tag_map: Dict[str, Tag] = {tag.uuid: tag for tag in tags}
project_map = {project.uuid: project for project in projects}


def on_ready():
    ctx.lists["self.things_tag"] = actions.user.create_spoken_forms_from_map(
        {tag.title: tag.uuid for tag in tags}
    )
    ctx.lists[
        "self.things_tag_with_shortcut"
    ] = actions.user.create_spoken_forms_from_map(
        {tag.title: tag.uuid for tag in tags if tag.shortcut is not None}
    )
    ctx.lists["self.things_project"] = actions.user.create_spoken_forms_from_map(
        {project.title: project.uuid for project in projects}
    )


# NOTE: please update this from "launch" to "ready" in Talon v0.1.5
app.register("ready", on_ready)


@mod.action_class
class Actions:
    def tag_todo(things_tags: str):
        """Tag todo with a list of tags"""
        tag_list = [tag_map[tag_uuid] for tag_uuid in things_tags.split(",")]
        tags_with_shortcuts = [tag for tag in tag_list if tag.shortcut is not None]
        tags_without_shortcuts = [tag for tag in tag_list if tag.shortcut is None]

        for tag in tags_with_shortcuts:
            actions.key(f"ctrl-{tag.shortcut}")

        for tag in tags_without_shortcuts:
            actions.key(f"cmd-shift-t")
            actions.insert(tag.title)
            actions.key("enter")

    def filter_by_tag(things_tags: str):
        """Tag todo with a list of tags"""
        tag_list = [tag_map[tag_uuid] for tag_uuid in things_tags.split(",")]

        for tag in tag_list:
            if tag.shortcut is None:
                raise Exception("Can only filter by tags with assigned shortcuts")
            actions.key(f"ctrl-alt-{tag.shortcut}")

    def show_tag(things_tag: str):
        """Show a particular tag in things"""
        tag = tag_map[things_tag]
        webbrowser.open(f"things:///show?id={tag.uuid}")

    def show_things_list(things_project: str):
        """Show a list in things"""
        project = project_map[things_project]
        webbrowser.open(f"things:///show?id={project.uuid}")

    def move_todo(project: str):
        """Move todo to a particular list"""
        try:
            project = project_map[project].title
        except KeyError:
            pass
        actions.key("cmd-shift-m")
        actions.insert(project)
        actions.key("enter")


@mod.capture(rule="{self.things_tag}+")
def things_tags(m) -> str:
    "One or more Things tags"
    return ",".join(m.things_tag_list)


@mod.capture(rule="{self.things_tag_with_shortcut}+")
def things_tags_with_shortcut(m) -> str:
    "One or more Things tags"
    return ",".join(m.things_tag_with_shortcut_list)


@mod.capture(rule="{self.things_project}+")
def things_projects(m) -> str:
    "One or more Things projects"
    return to_csv_row_string(m.things_project_list)


def to_csv_row_string(row_elements: str) -> str:
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(row_elements)
    return output.getvalue()
