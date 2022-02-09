import talon

if hasattr(talon, "test_mode"):
    # Only include this when we're running tests

    from knausj_talon_pkg.lang.cplusplus import cplusplus

    def apply_lists(text: str):
        text = cplusplus.ctx.lists["self.cpp_pointers"].get(text, text)
        text = cplusplus.ctx.lists["self.cpp_type_sign_modifiers"].get(text, text)
        text = cplusplus.ctx.lists["self.cpp_type_qualifiers"].get(text, text)
        return text

    def build_declarator(spoken: str, *, var_name: str = "") -> str:
        # Simulate talon's `cpp_type_prefix` parsing:
        spoken = spoken.replace('array of', '[]')
        spoken = spoken.replace('function returning', '()')
        for spoken_pointer, pointer_symbol in cplusplus.ctx.lists["self.cpp_pointers"].items():
            spoken = spoken.replace(f'{spoken_pointer} to', pointer_symbol)
        m = [apply_lists(txt) for txt in spoken.split()]
        ty = cplusplus.parse_type(m)
        result = cplusplus.build_declarator(ty, var_name)
        return result

    def test_qualifiers():
        assert build_declarator("const int") == "const int"
        assert build_declarator("int const") == "int const"
        assert build_declarator("int const", var_name="v") == "int const v"

    def test_pointer_types():
        assert build_declarator("pointer to int") == "int*"
        assert build_declarator("pointer to int", var_name="v") == "int* v"
        assert build_declarator("pointer to int const", var_name="v") == "int const* v"
        assert build_declarator("const int pointer") == "const int*"
        assert build_declarator("const pointer to int") == "int* const"
        assert build_declarator("const reference to int") == "const int&"
        assert build_declarator("pointer to const int") == "const int*"
        assert (
            build_declarator("const pointer to volatile int") == "volatile int* const"
        )
        assert (
            build_declarator("const pointer to int volatile") == "int volatile* const"
        )
        assert build_declarator("int volatile pointer const") == "int volatile* const"
        assert build_declarator("volatile int pointer const") == "volatile int* const"
        assert (
            build_declarator("volatile int pointer const", var_name="v")
            == "volatile int* const v"
        )

    def test_array_types():
        assert build_declarator("array of int") == "int[]"
        assert build_declarator("array of int", var_name="v") == "int v[]"
        assert build_declarator("int array") == "int[]"
        assert build_declarator("int array", var_name="v") == "int v[]"
        assert build_declarator("array of const int") == "const int[]"
        assert build_declarator("const array of int") == "const int[]"
        assert build_declarator("array of int const") == "int const[]"
        assert build_declarator("int array const") == "int const[]"
        assert build_declarator("int array const reference") == "int const(&)[]"
        assert build_declarator("pointer to array of pointer to void") == "void*(*)[]"

    def test_function_types():
        assert build_declarator("function returning int") == "int()"
        assert build_declarator("function returning int", var_name="f") == "int f()"
        assert build_declarator("int function") == "int()"
        assert build_declarator("int function", var_name="f") == "int f()"
        assert build_declarator("int pointer function", var_name="f") == "int* f()"
        assert build_declarator("int function pointer", var_name="p") == "int(* p)()"
        assert build_declarator("int function pointer const",var_name="p") == "int(* const p)()"
        assert build_declarator("int pointer function reference") == "int*(&)()"
        assert build_declarator("function returning int pointer") == "int*()"
        assert (
            build_declarator("int function pointer array", var_name="vtbl")
            == "int(* vtbl[])()"
        )

    def test_generic_types():
        assert (
            build_declarator("std::vector of int", var_name="v") == "std::vector<int> v"
        )
        assert (
            build_declarator("reference to const std::vector of pointer to const char")
            == "const std::vector<const char*>&"
        )
        assert (
            build_declarator("reference to const std::vector of char const pointer")
            == "const std::vector<char const*>&"
        )

    def test_complex_generic_type():
        assert (
            build_declarator(
                "reference to std::unique_ptr of pointer to std::vector of char pointer"
            )
            == "std::unique_ptr<std::vector<char*>*>&"
        )

    def test_lists():
        for listname in [
            "self.cpp_standard_types",
            "user.cpp_standard_functions",
            "user.cpp_standard_objects",
            "user.code_libraries",
        ]:
            for key in cplusplus.ctx.lists[listname].keys():
                assert "_" not in key
