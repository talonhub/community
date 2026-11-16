import talon

if hasattr(talon, "test_mode"):
    from core.numbers.numbers import (
        parse_number,
        parse_scale,
        scales,
        scan_small_numbers,
    )

    def _assert_expected_matches_number_parse(expected, string):
        print("testing:", string)
        l = list(scan_small_numbers(string.split()))
        print("  scan --->", l)
        for scale in scales:
            old = l
            l = parse_scale(scale, l)
            if scale in old:
                print("  parse -->", l)
            else:
                assert old == l, (
                    "parse_scale should do nothing if the scale does not occur in the list"
                )
        result = "".join(str(n) for n in l)
        assert result == parse_number(string.split())
        assert str(expected) == result, (
            f"parsing {string!r}, expected {expected}, got {result}"
        )

    def test_single_and():
        _assert_expected_matches_number_parse(105000, "one hundred and five thousand")

    def test_repeating_a_scale():
        _assert_expected_matches_number_parse(1000000, "one thousand thousand")

    def test_using_several_scales_with_numbers():
        _assert_expected_matches_number_parse(
            1501000, "one million five hundred one thousand"
        )

    def test_using_many_scales_with_numeric_modifiers_and_multiple_ands():
        _assert_expected_matches_number_parse(
            1501106, "one million five hundred and one thousand one hundred and six"
        )

    def test_single_digits():
        _assert_expected_matches_number_parse(123, "one two three")

    def test_single_digit_followed_by_two_digit_number():
        _assert_expected_matches_number_parse(123, "one twenty three")

    def test_two_digit_number_followed_by_a_single_digit():
        _assert_expected_matches_number_parse(
            104, "ten four"
        )  # borderline, but valid in some dialects

    def test_two_consecutive_two_digit_numbers():
        _assert_expected_matches_number_parse(
            1066, "ten sixty six"
        )  # a common way of saying years

    def test_oh_for_zero():
        _assert_expected_matches_number_parse(1906, "nineteen oh six")  # year

    def test_year_in_the_two_thousands():
        _assert_expected_matches_number_parse(2001, "twenty oh one")  # year

    def test_two_digit_year_in_the_two_thousands():
        _assert_expected_matches_number_parse(2020, "twenty twenty")

    def test_single_digit_year_in_the_one_thousands():
        _assert_expected_matches_number_parse(1001, "one thousand one")

    def test_two_digit_year_in_the_one_thousands():
        _assert_expected_matches_number_parse(1010, "one thousand ten")

    def test_using_scales_for_six_digits_with_and():
        _assert_expected_matches_number_parse(
            123456,
            "one hundred and twenty three thousand and four hundred and fifty six",
        )

    def test_using_scales_for_six_digits_without_and():
        _assert_expected_matches_number_parse(
            123456, "one twenty three thousand four fifty six"
        )
