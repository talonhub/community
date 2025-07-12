code.language: sql
-
tag(): user.code_operators_math
tag(): user.code_comment_line
tag(): user.code_comment_block_c_like
tag(): user.code_data_null
tag(): user.code_functions_common

{user.sql_select}:
    insert(sql_select)

from <user.sql_table_with_alias>:
    user.sql_insert(" from ")
    insert(sql_table_with_alias)

with: user.insert_snippet_by_name("withStatement")

{user.sql_join} [<user.sql_table_with_alias>]:
    user.sql_insert(sql_join)
    insert(" ")
    insert(sql_table_with_alias)

on <user.sql_field>:
    user.sql_insert("on ")
    insert(sql_field)

on <user.sql_field_equals>:
    user.sql_insert("on ")
    insert(sql_field_equals)

equals <user.sql_field>:
    user.sql_insert("= ")
    insert(sql_field)

where <user.sql_field>:
    user.sql_insert("where ")
    insert(sql_field)

and <user.sql_field>:
    user.sql_insert("and ")
    insert(sql_field)

or <user.sql_field>:
    user.sql_insert("or ")
    insert(sql_field)
