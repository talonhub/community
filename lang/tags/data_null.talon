tag: user.code_data_null
-
state {user.code_data_null}: insert(code_data_null)
is not (none | null): user.code_insert_is_not_null()
is (none | null): user.code_insert_is_null()
