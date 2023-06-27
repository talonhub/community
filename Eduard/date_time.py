from datetime import date, timedelta
from talon import Module, Context, actions
from typing import Optional
import time

mod = Module()
mod.list("ampm", desc="AM or PM")

@mod.capture
def ampm(m) -> str:
	"AM or PM"

ctx = Context()
ctx.lists["self.ampm"] = {
	"AM": " AM",
	"PM": " PM",
	"A": " AM",
	"P": " PM"
}

@mod.capture(rule="{self.ampm}")
def ampm(m) -> str:
	return m.ampm

month_words = 'one two three four five six seven eight nine ten eleven twelve'.split()
months = {word: number for number, word in enumerate(month_words, 1)}

@mod.capture(rule=f'({"|".join(month_words)})')
def month(m) -> int:
	return months[m[0]]

@mod.capture(rule="<number_small> | (twenty | thirty [<digits>])")
def day(m) -> int:
	if hasattr(m, 'number_small'): return m.number_small
	day = getattr(m, 'digits', 0)
	if m[0] == 'twenty': day += 20
	elif m[0] == 'thirty': day += 30
	return day

@mod.capture(rule="<number_small> [<number_small> | hundred | thousand]")
def year(m) -> int:
	if len(m) == 1: return m[0]
	if m[1] == 'thousand': return m[0] * 1000
	if m[1] == 'hundred': return m[0] * 100
	return (m[0] * 100) + m[1]

@mod.action_class
class Actions:
	def insert_time_ampm():
		"""Inserts the current time in 12-hour format"""
		actions.insert(time.strftime('%-I:%M %p'))

	def insert_date(days: Optional[int] = 0, format: Optional[str] = '%x'):
		"""Inserts the date offset by the specified number of days"""
		actions.insert((date.today() + timedelta(days=days)).strftime(format))
