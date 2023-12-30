from talon import Context, Module, actions, ui, app
import os

mod = Module()
mod.list("employee_names", desc="list of employee names")
mod.list("employee_perforce_aliases", desc="list of employee perforce aliases")
mod.list("employee_full_name", desc="list of employee full names")
mod.list("employee_emails", desc="list of employee emails")