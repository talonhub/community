from talon import Context, Module, actions, settings
import re

mod = Module()

ctx = Context()
ctx.matches = r"""
tag: user.cplusplus
"""

ctx.lists["self.cpp_pointers"] = {
    "pointer": "*",
    "reference": "&",
    "R value reference": "&&",
    "universal reference": "&&",
    "forwarding reference": "&&",
    # C++/CLI extensions:
    "managed pointer": "^",
    "tracking reference": "%",
}

# Type modifiers and qualifiers
ctx.lists["self.cpp_type_sign_modifiers"] = {
    "signed": "signed",
    "unsigned": "unsigned",
}
ctx.lists["self.cpp_type_qualifiers"] = {
    "const": "const",
    "volatile": "volatile",
}
ctx.lists["self.cpp_type_bit_width"] = {
    "eight": "8",
    "sixteen": "16",
    "thirty two": "32",
    "sixty four": "64",
}

ctx.lists["self.cpp_simple_types"] = {
    "auto": "auto",
    "character": "char",
    "char": "char",
    "wide char": "wchar_t",
    "char eight": "char8_t",
    "char sixteen": "char16_t",
    "char thirty two": "char32_t",
    "short": "short",
    "long": "long",
    "long long": "long long",
    "int": "int",
    "integer": "int",
    "void": "void",
    "double": "double",
    "long double": "long double",
    "struct": "struct",
    "struck": "struct",
    "num": "enum",
    "union": "union",
    "float": "float",
    "size T": "size_t",
    "size type": "size_t",
    "bool": "bool",
    "boolean": "bool",
    "typename": "typename",
}

# Words that trigger the standard namespace logic
ctx.lists["self.cpp_standard"] = {
    "standard": "std",
    "stood": "std",
}

# Types in std namespace
ctx.lists["self.cpp_standard_types"] = {
    # Language Support / Utility Library
    ## Type support
    "size T": "size_t",
    "size type": "size_t",
    "pointer diff": "ptrdiff_t",
    "pointer diff T": "ptrdiff_t",
    "pointer diff type": "ptrdiff_t",
    "null pointer T": "nullptr_t",
    "null pointer type": "nullptr_t",
    "max align T": "max_align_t",
    "max align type": "max_align_t",
    "byte": "byte",
    "numeric limits": "numeric_limits<>",
    "type info": "type_info",
    "bad type I D": "bad_typeid",
    "bad cast": "bad_cast",
    "type index": "type_index",
    ## Dynamic memory management
    "unique pointer": "unique_ptr<>",
    "shared pointer": "shared_ptr<>",
    "weak pointer": "weak_ptr<>",
    "owner less": "owner_less<>",
    "enable shared from this": "enable_shared_from_this<>",
    "allocator": "allocator<>",
    ## Error handling
    "exception": "exception",
    "exception pointer": "exception_ptr",
    "terminate handler": "terminate_handler",
    "bad exception": "bad_exception",
    "logic error": "logic_error",
    "invalid argument": "invalid_argument",
    "domain error": "domain_error",
    "length error": "length_error",
    "out of range": "out_of_range",
    "runtime error": "runtime_error",
    "range error": "range_error",
    "overflow error": "overflow_error",
    "underflow error": "underflow_error",
    "error category": "underflow_error",
    "error category": "error_category",
    "generic category": "generic_category",
    "system category": "system_category",
    "error condition": "error_condition",
    "err C": "errc",
    "error code": "error_code",
    "system error": "system_error",
    ## Source code information capture
    "source location": "source_location",
    "stack trace entry": "stacktrace_entry",
    ## Initializer lists
    "initializer list": "initializer_list",
    ## Three-way comparison
    "partial ordering": "partial_ordering",
    "weak ordering": "weak_ordering",
    "strong ordering": "strong_ordering",
    ## Coroutine support
    "coroutine traits": "coroutine_traits<>",
    "coroutine handle": "coroutine_handle<>",
    ## Pairs and tuples
    "pair": "pair<>",
    "tuple": "tuple<>",
    ## Optional, variant and any
    "optional": "optional<>",
    "variant": "variant<>",
    "any": "any<>",
    ## Bitset
    "bit set": "bitset<>",
    ## Function objects
    "function": "function<>",
    ## Hash support
    "hash": "hash<>",
    ## Formatting library
    "formatter": "formatter<>",
    "format error": "format_error",
    # Strings library
    "string": "string",
    "wide string": "wstring",
    "string view": "string_view",
    "wide string view": "wstring_view",
    "char traits": "char_traits",
    # Containers library
    ## Sequence Containers
    "array": "array<>",
    "vector": "vector<>",
    "deck": "deque<>",
    "forward list": "forward_list<>",
    "list": "list<>",
    ## Associative Containers
    "set": "set<>",
    "map": "map<>",
    "multiset": "multiset<>",
    "multimap": "multimap<>",
    ## Unordered associative Containers
    "unordered set": "set<>",
    "unordered map": "map<>",
    "unordered multiset": "multiset<>",
    "unordered multimap": "multimap<>",
    ## Container adaptors
    "stack": "stack<>",
    "queue": "queue<>",
    "priority queue": "priority_queue<>",
    ## span
    "span": "span<>",
    # Numerics library
    "complex": "complex",
    "ratio": "ratio<>",
    "endian": "endian",
    # Input/output library
    "eye os": "ios",
    "I O S": "ios",
    "wide eye os": "wios",
    "wide I O S": "wios",
    "stream buf": "streambuf",
    "wide stream buf": "wstreambuf",
    "file buf": "filebuf",
    "wide file buf": "wfilebuf",
    "string buf": "stringbuf",
    "wide string buf": "wstringbuf",
    "input stream": "istream",
    "wide input stream": "wistream",
    "output stream": "ostream",
    "wide output stream": "wostream",
    "input output stream": "iostream",
    "wide input output stream": "wiostream",
    "input file stream": "ifstream",
    "wide input file stream": "wifstream",
    "output file stream": "ofstream",
    "wide output file stream": "wofstream",
    "file stream": "fstream",
    "wide file stream": "wfstream",
    "input string stream": "istringstream",
    "wide input string stream": "wistringstream",
    "output string stream": "ostringstream",
    "wide output string stream": "wostringstream",
    "string stream": "stringstream",
    "wide string stream": "wstringstream",
    "stream off": "streamoff",
    "stream size": "streamsize",
    "stream pos": "streampos",
    "wide stream pos": "wstreampos",
    # File system library
    "file system path": "filesystem::path",
    # Regular expressions library
    "reg ex": "regex",
    "wide reg ex": "wregex",
    "sub match": "sub_match",
    "match results": "match_results",
    "reg ex iterator": "regex_iterator",
    "reg ex token iterator": "regex_token_iterator",
    "reg ex error": "regex_error",
    # Atomic operations library
    "atomic": "atomic<>",
    "memory order": "memory_order",
    # Thread support library
    "thread": "thread",
    "join thread": "jthread",
    "mutex": "mutex",
    "timed mutex": "timed_mutex",
    "recursive mutex": "recursive_mutex",
    "recursive timed mutex": "recursive_timed_mutex",
    "shared mutex": "shared_mutex",
    "shared timed mutex": "shared_timed_mutex",
    "lock guard": "lock_guard",
    "scoped lock": "scoped_lock<>",
    "unique lock": "unique_lock<>",
    "shared lock": "shared_lock<>",
    "once flag": "once_flag",
    "condition variable": "condition_variable",
    "condition variable any": "condition_variable_any",
    "cv status": "cv_status",
    "counting semaphore": "counting_semaphore",
    "binary semaphore": "binary_semaphore",
    "latch": "latch",
    "barrier": "barrier",
    "promise": "promise<>",
    "packaged task": "packaged_task<>",
    "future": "future<>",
    "shared future": "shared_future<>",
    "future status": "future_status",
    "future error": "future_error",
    "future category": "future_category",
    "future error code": "future_errc",
}

ctx.lists["user.code_libraries"] = {
    "concepts": "concepts",
    "coroutine": "coroutine",
    "any": "any",
    "bitset": "bitset",
    "chrono": "chrono",
    "C set jump": "csetjmp",
    "C signal": "csignal",
    "C standard arg": "cstdarg",
    "C standard def": "cstddef",
    "C standard lib": "cstdlib",
    "C ctime": "ctime",
    "functional": "functional",
    "initializer list": "initializer_list",
    "optional": "optional",
    "source location": "source_location",
    "tuple": "tuple",
    "type traits": "type_traits",
    "type index": "typeindex",
    "type info": "typeinfo",
    "utility": "utility",
    "variant": "variant",
    "version": "version",
    "memory": "memory",
    "memory resource": "memory_resource",
    "new": "new",
    "scoped allocator": "scoped_allocator",
    "C float": "cfloat",
    "C int types": "cinttypes",
    "C limits": "climits",
    "C standard int": "cstdint",
    "limits": "limits",
    "C assert": "cassert",
    "C errno": "cerrno",
    "exception": "exception",
    "standard except": "stdexcept",
    "system error": "system_error",
    "stacktrace": "stacktrace",
    "C C type": "cctype",
    "char conv": "charconv",
    "C string": "cstring",
    "C U char": "cuchar",
    "C W char": "cwchar",
    "C W C type": "cwctype",
    "format": "format",
    "string": "string",
    "string view": "string_view",
    "array": "array",
    "deck": "deque",
    "forward list": "forward_list",
    "list": "list",
    "map": "map",
    "queue": "queue",
    "set": "set",
    "span": "span",
    "stack": "stack",
    "unordered map": "unordered_map",
    "unordered set": "unordered_set",
    "vector": "vector",
    "iterator": "iterator",
    "ranges": "ranges",
    "algorithm": "algorithm",
    "execution": "execution",
    "bit": "bit",
    "C floating env": "cfenv",
    "C math": "cmath",
    "complex": "complex",
    "number": "number",
    "numeric": "numeric",
    "random": "random",
    "ratio": "ratio",
    "val array": "valarray",
    "C local": "clocal",
    "code convert": "codecvt",
    "locale": "locale",
    "C standard I O": "cstdio",
    "file stream": "fstream",
    "I O manip": "iomanip",
    "I O S": "ios",
    "I os": "ios",
    "I O S forward": "iosfwd",
    "I os forward": "iosfwd",
    "I O stream": "iostream",
    "input output stream": "iostream",
    "I stream": "istream",
    "input stream": "istream",
    "O stream": "ostream",
    "output stream": "ostream",
    "span stream": "spanstream",
    "string stream": "sstream",
    "stream buf": "streambuf",
    "sync stream": "syncstream",
    "file system": "filesystem",
    "regex": "regex",
    "atomic": "atomic",
    "barrier": "barrier",
    "condition variable": "condition_variable",
    "future": "future",
    "latch": "latch",
    "mutex": "mutex",
    "semaphore": "semaphore",
    "shared mutex": "shared_mutex",
    "stop token": "stop_token",
    "thread": "thread",
}

ctx.lists["user.code_functions"] = {
    "mem copy": "memcpy",
    "mem set": "memset",
    "mem comp": "memcmp",
    "string cat": "strcat",
    "stir cat": "strcat",
    "stir en cat": "strncat",
    "stir elle cat": "strlcat",
    "stir copy": "strcpy",
    "stir en copy": "strncpy",
    "stir elle copy": "strlcpy",
    "string char": "strchr",
    "string dupe": "strdup",
    "stir dupe": "strdup",
    "stir comp": "strcmp",
    "stir en comp": "strncmp",
    "string len": "strlen",
    "stir len": "strlen",
    "is digit": "isdigit",
    "get char": "getchar",
    "print eff": "printf",
    "es print eff": "sprintf",
    "es en print eff": "sprintf",
    "stir to int": "strtoint",
    "stir to unsigned int": "strtouint",
    "ay to eye": "atoi",
    "em map": "mmap",
    "ma map": "mmap",
    "em un map": "munmap",
    "size of": "sizeof",
    "ef open": "fopen",
    "ef write": "fwrite",
    "ef read": "fread",
    "ef close": "fclose",
    "exit": "exit",
    "signal": "signal",
    "set jump": "setjmp",
    "get op": "getopt",
    "malloc": "malloc",
    "see alloc": "calloc",
    "alloc ah": "alloca",
    "re alloc": "realloc",
    "free": "free",
    "offset of": "offsetof",
}

ctx.lists["user.cpp_standard_functions"] = {
    "is constant evaluated": "is_constant_evaluated",
    # Program support utilities
    "abort": "abort",
    "exit": "exit",
    "quick exit": "quick_exit",
    "at exit": "atexit",
    "at quick exit": "at_quick_exit",
    "system": "system",
    "get env": "getenv",
    # Object access
    "launder": "launder",
    # Error handling
    "uncaught exceptions": "uncaught_exceptions",
    "make exception pointer": "make_exception_ptr",
    "current exception": "current_exception",
    "rethrow exception": "rethrow_exception",
    "nested exception": "nested_exception",
    "throw with nested": "throw_with_nested",
    "rethrow if nested": "rethrow_if_nested",
    "terminate": "terminate",
    "get terminate": "get_terminate",
    "set terminate": "set_terminate",
    "assert": "assert",
    # Coroutine support
    "no op coroutine": "noop_coroutine",
    # Swap and type operations
    "swap": "swap",
    "exchange": "exchange",
    "forward": "forward<>",
    # "move": "move", # also appears in <algorithm>
    "move if no except": "move_if_noexcept",
    "as const": "as_const",
    "declval": "declval<>",
    "to underlying": "to_underlying",
    # Funtional
    "apply": "apply",
    "bind": "bind",
    # Formatting
    "to chars": "to_chars",
    "from chars": "from_chars",
    "format": "format",
    "format to": "format_to",
    "format to n": "format_to_n",
    "formatted size": "formatted_size",
    # Algorithms (excluding those duplicated for ranges)
    "ranges starts with": "ranges::starts_with",
    "ranges ends with": "ranges::ends_with",
    # Bit manipulation
    "bit cast": "bit_cast",
    "byte swap": "byteswap",
    "has single bit": "has_single_bit",
    "bit ceil": "bit_ceil",
    "bit floor": "bit_floor",
    "bit width": "bit_width",
    "rotate left": "rotl",
    "rotate right": "rotr",
    "count left zero": "countl_zero",
    "count left one": "countl_one",
    "count right zero": "countr_zero",
    "count right one": "countr_one",
    "pop count": "popcount",
    # Other
    "mem copy": "memcpy",
    "mem set": "memset",
    "mem comp": "memcmp",
    "to string": "to_string",
    "make unique": "make_unique<>",
    "make shared": "make_shared<>",
}

ctx.lists["user.cpp_standard_range_algorithms"] = {
    "all of": "all_of",
    "any of": "any_of",
    "none of": "none_of",
    "for each": "for_each",
    "for each n": "for_each_n",
    "count": "count",
    "count if": "count_if",
    "mismatch": "mismatch",
    "find": "find",
    "find if": "find_if",
    "find if not": "find_if_not",
    "find end": "find_end",
    "find first of": "find_first_of",
    "adjacent find": "adjacent_find",
    "search": "search",
    "search n": "search_n",
    "copy": "copy",
    "copy if": "copy_if",
    "copy n": "copy_n",
    "copy backward": "copy_backward",
    "move": "move",
    "move backward": "move_backward",
    "fill": "fill",
    "fill n": "fill_n",
    "transform": "transform",
    "generate": "generate",
    "generate n": "generate_n",
    "remove": "remove",
    "remove if": "remove_if",
    "remove copy": "remove_copy",
    "remove copy if": "remove_copy_if",
    "replace": "replace",
    "replace if": "replace_if",
    "replace copy": "replace_copy",
    "replace copy if": "replace_copy_if",
    "swap ranges": "swap_ranges",
    "reverse": "reverse",
    "reverse copy": "reverse_copy",
    "rotate": "rotate",
    "rotate copy": "rotate_copy",
    "shuffle": "shuffle",
    "sample": "sample",
    "unique": "unique",
    "unique copy": "unique_copy",
    "is partitioned": "is_partitioned",
    "partition": "partition",
    "partition copy": "partition_copy",
    "stable partition": "stable_partition",
    "partition point": "partition_point",
    "is sorted": "is_sorted",
    "is sorted until": "is_sorted_until",
    "sort": "sort",
    "partial sort": "partial_sort",
    "partial sort copy": "partial_sort_copy",
    "stable sort": "stable_sort",
    "nth element": "nth_element",
    "lower bound": "lower_bound",
    "upper bound": "upper_bound",
    "binary search": "binary_search",
    "equal range": "equal_range",
    "merge": "merge",
    "inplace merge": "inplace_merge",
    "includes": "includes",
    "set difference": "set_difference",
    "set intersection": "set_intersection",
    "set symmetric difference": "set_symmetric_difference",
    "set union": "set_union",
    "is heap": "is_heap",
    "is heap until": "is_heap_until",
    "make heap": "make_heap",
    "push heap": "push_heap",
    "pop heap": "pop_heap",
    "sort heap": "sort_heap",
    "max": "max",
    "max element": "max_element",
    "min": "min",
    "min element": "min_element",
    "minmax": "minmax",
    "clamp": "clamp",
    "equal": "equal",
    "lexicographical compare": "lexicographical_compare",
    "lexicographical compare three way": "lexicographical_compare_three_way",
    "is permutation": "is_permutation",
    "next permutation": "next_permutation",
    "prev permutation": "prev_permutation",
}

ctx.lists["user.cpp_standard_objects"] = {
    "see out": "cout",
    "see error": "cerr",
    "see in": "cin",
    "flush": "flush",
    "end line": "endl",
    "null opt": "nullopt",
}

ctx.lists["user.cpp_cast_style"] = {
    "see cast": "(TYPE)VAL",
    "static cast": "static_cast<TYPE>(VAL)",
    "dynamic cast": "dynamic_cast<TYPE>(VAL)",
    "reinterpret cast": "reinterpret_cast<TYPE>(VAL)",
}

ctx.lists["user.cpp_access_specifiers"] = {
    "public": "public",
    "private": "private",
    "protected": "protected",
}

ctx.lists["user.cpp_declaration_specifiers"] = {
    "type deaf": "typedef",
    "inline": "inline",
    "virtual": "virtual",
    "explicit": "explicit",
    "friend": "friend",
    "const expr": "constexpr",
    "const eval": "consteval",
    "const init": "constinit",
    "friend": "friend",
    "static": "static",
    "thread local": "thread_local",
    "extern": "extern",
    "mutable": "mutable",
    "no except": "noexcept",
}

mod.list("cpp_pointers", desc="C++ pointer/reference types")
mod.list("cpp_type_sign_modifiers", desc="C++ type sign modifiers")
mod.list("cpp_type_qualifiers", desc="C++ type qualifiers")
mod.list(
    "cpp_type_bit_width", desc="Typical bit-width of C++ fixed width integer types"
)
mod.list("cpp_simple_types", desc="Common C/C++ types")
mod.list("cpp_standard", desc="Words that trigger the standard namespace logic")
mod.list("cpp_standard_types", desc="C++ types in namespace std")
mod.list(
    "cpp_user_types",
    desc="Additional C++ types (intended to be redefined with project-specific names)",
)
mod.list("cpp_standard_functions", desc="C++ functions in namespace std")
mod.list(
    "cpp_standard_range_algorithms",
    desc="Functions that appear both in namespace std and std::ranges",
)
mod.list(
    "cpp_user_functions",
    desc="Additional C++ functions (intended to be redefined with project-specific names)",
)
mod.list(
    "cpp_user_libraries",
    desc="Additional C++ headers (intended to be redefined with project-specific names)",
)
mod.list("cpp_standard_objects", desc="C++ objects in namespace std")
mod.list("cpp_cast_style", desc="C++ cast operators")
mod.list("cpp_access_specifiers", desc="C++ access specifiers")
mod.list("cpp_declaration_specifiers", desc="C++ declaration specifiers")


def rm_newlines(txt):
    return txt.replace("\r", "").replace("\n", "")


@mod.capture(
    rule=rm_newlines(
        """
            [ {self.cpp_type_sign_modifiers} | U ]
            (int | integer)
            [fast | least]
            ( {self.cpp_type_bit_width} [T | type]
            | pointer (T | type)
            )
        """
    )
)
def cpp_fixed_width_integer_type(m) -> str:
    "Returns a string"
    replacements = {
        "signed": "",
        "unsigned": "u",
        "integer": "int",
        "fast": "_fast",
        "least": "_least",
        "pointer": "ptr",
        "t": "",
        "type": "",
    }
    return "".join(replacements.get(word, word) for word in m) + "_t"


@mod.capture(
    rule=rm_newlines(
        """
            [{self.cpp_type_sign_modifiers}] {self.cpp_simple_types}
          | {self.cpp_standard} {self.cpp_standard_types}
          | {self.cpp_standard} <self.cpp_fixed_width_integer_type>
          | {self.cpp_user_types}
          | <self.cpp_fixed_width_integer_type>
        """
    )
)
def cpp_simple_type(m) -> str:
    "Returns a string"
    if m[0] == "std":
        return "std::" + m[1]
    else:
        return " ".join(list(m))


@mod.capture(
    rule="{self.cpp_type_qualifiers} | {self.cpp_pointers} to | array of | function returning"
)
def cpp_type_prefix(m) -> str:
    """Handles a type prefix, translating from prefix syntax to suffix syntax.
    e.g. "pointer to" becomes "*"
    The suffix syntax then will be handled by cpp_raw_type().
    """
    if m[0] == 'array':
        return '[]'
    elif m[0] == 'function':
        return '()'   
    else:
        return m[0]

def parse_prefixed_type(m, pos=0):
    # Parse logic for "<self.cpp_type_prefix>* <self.cpp_simple_type>"
    west_cv = []
    prefixes = []
    while pos < len(m):
        if m[pos] == '*':
            # For pointers, move cv-qualifiers to the pointer type.
            prefixes.extend(west_cv)
            west_cv.clear()
            if m[pos] not in ("&", "&&", "%"):
                prefixes.extend(west_cv)
                west_cv.clear()
            prefixes.append(m[pos])
            pos += 1
        elif m[pos] in ("&", "&&", "%"):
            # But references can't be const, so keep their cv-qualifiers west.
            prefixes.append(m[pos])
            pos += 1
        elif m[pos] in ("[]", "()"):
            prefixes.append(m[pos])
            pos += 1
        elif m[pos] in ('const', 'volatile'):
            west_cv.append(m[pos])
            pos += 1
        else:
            break
    ty = " ".join(west_cv + [m[pos]])
    pos += 1
    return prefixes, ty, pos


generic_connectors = {"of", "to"}
generic_connector_regex = "(" + "|".join(generic_connectors) + ")"


@mod.capture(
    rule=rm_newlines(
        f"""
          <self.cpp_type_prefix>* <self.cpp_simple_type>
          ( {{self.cpp_pointers}}
          | {{self.cpp_type_qualifiers}}
          | array
          | function
          | ({generic_connector_regex}) <self.cpp_type_prefix>* <self.cpp_simple_type>
          )*
        """
    )
)
def cpp_raw_type(m) -> list:
    """Handles the full general type.
    Returns "raw" the form with $ placeholder for the declarator"""
    return list(m)

def parse_type(m, pos=0):
    # In the fully general form, we allow saying types like
    #   standard vector of pointer to const char = "std::vector<const char*>"
    prefixes, ty, pos = parse_prefixed_type(m, pos)
    ty += "$"  # placeholder indicating where we'll insert the variable name
    # While suffixes we encounter after an "of" apply to the nested type argument,
    # prefixes always apply to the outer type. So we need to pop the generic stack
    # between the suffixes and the prefixes.
    # print(f'm={m!r}')
    while pos < len(m):
        suffix = m[pos]
        # print(f"ty={ty!r}; m[{pos!r}]={suffix!r}")
        pos += 1
        if suffix in generic_connectors:
            element_type = parse_type(m, pos)
            element_type = build_declarator(element_type)
            if "<>$" in ty:
                ty = ty.replace("<>$", f"<{element_type}>$")
            else:
                ty = ty.replace("$", f"<{element_type}>$")
            # Remainder of m was handled by the recursive call
            # and is part of the element_type
            break
        elif suffix == 'array':
            ty = build_type(ty, '[]')
        elif suffix == 'function':
            ty = build_type(ty, '()')
        else:
            # east cv-qualifier or pointer (decl prefix)
            ty = build_type(ty, suffix)
    for prefix in reversed(prefixes):
        ty = build_type(ty, prefix)
    return ty


def build_type(ty: str, qual: str) -> str:
    # Given a type with a $ placeholder, returns the type with `qual`
    # added, where `qual` can be (), [], *, &, &&, % or a cv-qualifier.
    if qual.startswith(('(', '[')):
        return ty.replace("$",  "$" + qual)
    else:
        can_move_cv_qualifier_into_array = False
        if qual[0].isalpha():
            qual = f" {qual}"
            can_move_cv_qualifier_into_array = ty.rstrip("[]").endswith("$")
        if not ty.endswith("$") and "$)" not in ty and not can_move_cv_qualifier_into_array:
            ty = ty.replace("$", "($)")
        return ty.replace("$", qual + "$")


def build_declarator(ty: str, var_name: str="") -> str:
    # Given a type with a $ placeholder, substitutes the var_name for the placeholder.
    if var_name:
        var_name = f" {var_name}"
    return ty.replace("$", var_name)


@mod.capture(rule="<self.cpp_raw_type>")
def cpp_type(m) -> str:
    "Handles fully general C++ type names"
    return build_declarator(parse_type(m.cpp_raw_type))


@mod.capture(
    rule=f"( {{self.cpp_standard_types}} [{generic_connector_regex} <self.cpp_type>] | <self.cpp_fixed_width_integer_type>)"
)
def cpp_unqualified_standard_generic_type(m) -> str:
    "Returns a string"
    if len(m) > 1:
        ty = m[0]
        if "<>" in ty:
            return ty.replace("<>", f"<{m[-1]}>")
        else:
            return ty + f"<{m[-1]}>"
    else:
        return m[0]


@ctx.capture(
    "user.code_functions",
    rule=rm_newlines(
        """
        {user.code_functions}
        | {user.cpp_standard} {user.cpp_standard_functions}
        | {user.cpp_standard} {user.cpp_standard_range_algorithms}
        | {user.cpp_standard} ranges {user.cpp_standard_range_algorithms}
        | {user.cpp_user_functions}
        """
    ),
)
def code_functions(m) -> str:
    """Returns a function name"""
    if m[0] == "std":
        if m[1] == "ranges":
            return "std::ranges" + m[2]
        else:
            return "std::" + m[1]
    else:
        return m[0]


@ctx.capture(
    "user.code_libraries",
    rule="{user.code_libraries} | {user.cpp_user_libraries}",
)
def code_libraries(m) -> str:
    """Returns a function name"""
    if m[0] in ctx.lists["user.code_libraries"].values():
        return f"<{m[0]}>"
    else:
        return f'"{m[0]}"'


@ctx.action_class("user")
class UserActions:
    def code_operator_indirection():
        actions.auto_insert("*")

    def code_operator_address_of():
        actions.auto_insert("&")

    def code_operator_structure_dereference():
        actions.auto_insert("->")

    def code_operator_subscript():
        actions.insert("[]")
        actions.key("left")

    def code_operator_assignment():
        actions.auto_insert(" = ")

    def code_operator_subtraction():
        actions.auto_insert(" - ")

    def code_operator_subtraction_assignment():
        actions.auto_insert(" -= ")

    def code_operator_addition():
        actions.auto_insert(" + ")

    def code_operator_addition_assignment():
        actions.auto_insert(" += ")

    def code_operator_multiplication():
        actions.auto_insert(" * ")

    def code_operator_multiplication_assignment():
        actions.auto_insert(" *= ")

    # action(user.code_operator_exponent): " ** "
    def code_operator_division():
        actions.auto_insert(" / ")

    def code_operator_division_assignment():
        actions.auto_insert(" /= ")

    def code_operator_modulo():
        actions.auto_insert(" % ")

    def code_operator_modulo_assignment():
        actions.auto_insert(" %= ")

    def code_operator_equal():
        actions.auto_insert(" == ")

    def code_operator_not_equal():
        actions.auto_insert(" != ")

    def code_operator_greater_than():
        actions.auto_insert(" > ")

    def code_operator_greater_than_or_equal_to():
        actions.auto_insert(" >= ")

    def code_operator_less_than():
        actions.auto_insert(" < ")

    def code_operator_less_than_or_equal_to():
        actions.auto_insert(" <= ")

    def code_operator_and():
        actions.auto_insert(" && ")

    def code_operator_or():
        actions.auto_insert(" || ")

    def code_operator_bitwise_and():
        actions.auto_insert(" & ")

    def code_operator_bitwise_and_assignment():
        actions.auto_insert(" &= ")

    def code_operator_bitwise_or():
        actions.auto_insert(" | ")

    def code_operator_bitwise_or_assignment():
        actions.auto_insert(" |= ")

    def code_operator_bitwise_exclusive_or():
        actions.auto_insert(" ^ ")

    def code_operator_bitwise_exclusive_or_assignment():
        actions.auto_insert(" ^= ")

    def code_operator_bitwise_left_shift():
        actions.auto_insert(" << ")

    def code_operator_bitwise_left_shift_assignment():
        actions.auto_insert(" <<= ")

    def code_operator_bitwise_right_shift():
        actions.auto_insert(" >> ")

    def code_operator_bitwise_right_shift_assignment():
        actions.auto_insert(" >>= ")

    def code_operator_lambda():
        actions.insert("[](){}")
        actions.key("left")
        actions.sleep(0.1)
        actions.key("enter")

    def code_insert_null():
        actions.user.paste("nullptr")

    def code_insert_is_null():
        actions.user.paste(" == nullptr")

    def code_insert_is_not_null():
        actions.user.paste(" != nullptr")

    def code_state_if():
        actions.insert("if ()\n{}\n")
        actions.key("up end left:1 enter up:2 end left:1")

    def code_state_else_if():
        actions.insert("else if ()\n{}\n")
        actions.key("up end left:1 enter up:2 end left:1")

    def code_state_else():
        actions.insert("else\n{\n}\n")
        actions.key("up:2 end")

    def code_state_switch():
        actions.insert("switch ()")
        actions.edit.left()

    def code_state_case():
        actions.insert("case :")
        actions.edit.left()

    def code_state_for():
        actions.insert("for ()\n{}\n")
        actions.key("up end left:1 enter up:2 end left:1")

    def code_state_go_to():
        actions.auto_insert("goto ")

    def code_state_while():
        actions.insert("while ()")
        actions.edit.left()

    def code_state_return():
        actions.insert("return ;")
        actions.edit.left()

    def code_break():
        actions.auto_insert("break;")

    def code_next():
        actions.auto_insert("continue;")

    def code_insert_true():
        actions.user.paste("true")

    def code_insert_false():
        actions.user.paste("false")

    def code_comment_line_prefix():
        actions.auto_insert("//")

    def code_insert_function(text: str, selection: str):
        if selection:
            text = text + "({})".format(selection)
        else:
            text = text + "()"

        actions.user.paste(text)
        actions.edit.left()

    # TODO - it would be nice that you integrate that types from c_cast
    # instead of defaulting to void
    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_private_static_function(text: str):
        """Inserts private static function"""
        result = "static void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_insert_library(text: str, selection: str):
        actions.edit.file_end()
        actions.user.select_previous_occurrence("#include")
        actions.sleep("200ms")
        actions.edit.line_insert_down()
        actions.insert(f"#include {text}")

    def code_block():
        # First delete existing selection, if any
        actions.insert(" ")
        actions.key("backspace")
        actions.insert("{}")
        actions.edit.left()
        actions.sleep(0.1)
        actions.key("enter")

    def code_self():
        actions.insert("this")

    def code_define_class():
        actions.insert("class  {};")
        actions.edit.left()
        actions.edit.left()
        actions.edit.left()
        actions.edit.left()


@mod.action_class
class cpp_actions:
    def cpp_insert_cast(cast: str, target_type: str):
        """Insert a cast operator. If some text is selected, the cast is wrapped around the selected code."""
        expr = actions.edit.selected_text()
        if target_type:
            cast = cast.replace("TYPE", target_type)
            pos = cast.index("VAL")
        else:
            pos = cast.index("TYPE")
            cast = cast.replace("TYPE", "")
        if any(not c.isspace() for c in expr):
            cast = cast.replace("VAL", expr)
        else:
            cast = cast.replace("VAL", "")
        actions.insert(cast)
        for _ in cast[pos:]:
            actions.edit.left()

    def cpp_insert_call(function_name: str):
        """Inserts a function call. If some text is selected, the call is wrapped around the selected code."""
        expr = actions.edit.selected_text()
        if "<>" in function_name:
            generic_pos = function_name.index("<>") + 1
        else:
            generic_pos = None
        code = f"{function_name}({expr})"
        actions.insert(code)
        if generic_pos is not None:  # put cursor between <>
            for _ in code[generic_pos:]:
                actions.edit.left()
        else:  # re-select the argument expression
            actions.edit.left()
            for _ in range(len(function_name) + 1, len(code) - 1):
                actions.edit.extend_left()

    def cpp_build_declarator_with_prefix(prefix: str, raw_type: list, var_name: str) -> str:
        """Build a declarator from a raw type with an added prefix."""
        return build_declarator(parse_type([prefix] + raw_type), var_name)

    def cpp_build_declarator(raw_type: list, var_name: str) -> str:
        """Build a declarator from a raw type."""
        return build_declarator(parse_type(raw_type), var_name)
