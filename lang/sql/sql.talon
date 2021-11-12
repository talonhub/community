mode: command
and mode: user.sql
mode: command
and mode: user.auto_lang
and code.language: sql
-
tag(): user.code_generic
tag(): user.code_operators

# Some commands have spaces around them to avoid having to continually say 'space'.
# The ones that don't have an initial space are expected to be at the start of a new line.
# This could probably be done in a better way.
select: "SELECT "
star: "* "
distinct: "DISTINCT "
from: "FROM "
case: "CASE"
when: "WHEN "
then: "THEN "
else: "ELSE "
end: "END"
as: " AS "
where: "WHERE "
between: " BETWEEN "
and: "AND "
or: "OR "
is: "IS "
not: "NOT "
in: "IN "
group by: "GROUP BY "
having: "HAVING "
order by: "ORDER BY "
descending: "DESC"
ascending: "ASC"
limit: "LIMIT "

{user.sql_join_types} join:
    user.join_tables("{sql_join_types}")