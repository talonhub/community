import math

class Number:
    number: int
    spoken_forms: list[str]

    def __init__(self, number: int, spoken_form: str | list[str]):
        self.number = number
        self.spoken_forms = (
            [spoken_form] if isinstance(spoken_form, str) else spoken_form
        )

# digits: 1 through 9 
digits = [
    Number(0, ["zero", "oh"]), 
    Number(1, "one"), 
    Number(2, "two"), 
    Number(3, "three"), 
    Number(4, "four"), 
    Number(5, "five"), 
    Number(6, "six"), 
    Number(7, "seven"), 
    Number(8, "eight"), 
    Number(9, "nine"), 
]

# teens: 10 through 19 
teens = [
    Number(10, "ten"), 
    Number(11, "eleven"), 
    Number(12, "twelve"), 
    Number(13, "thirteen"), 
    Number(14, "fourteen"), 
    Number(15, "fifteen"), 
    Number(16, "sixteen"), 
    Number(17, "seventeen"), 
    Number(18, "eighteen"), 
    Number(19, "nineteen"),
]

# tens: increments of 10 in the range [20, 90]
tens = [
    Number(20, "twenty"), 
    Number(30, "thirty"), 
    Number(40, "forty"), 
    Number(50, "fifty"), 
    Number(60, "sixty"), 
    Number(70, "seventy"), 
    Number(80, "eighty"), 
    Number(90, "ninety"), 
]

scales = [
    Number(100, "hundred"), 
    Number(1000, "thousand"), 
    Number(1000000, "million"), 
    Number(1000000000, "billion"), 
    Number(1000000000000, "trillion"), 
    Number(1000000000000000, "quadrillion"), 
    Number(1000000000000000000, "quintillion"),
    Number(1000000000000000000000, "sextillion"),
    Number(1000000000000000000000000, "septillion"),
    Number(1000000000000000000000000000, "octillion"),
    Number(1000000000000000000000000000000, "nonillion"),
    Number(1000000000000000000000000000000000, "decillion"),
]

# scales = "hundred thousand million billion trillion quadrillion quintillion sextillion septillion octillion nonillion decillion".split()

digit_list = [number.spoken_forms for i, number in enumerate(digits)]
teens_list = [number.spoken_forms for i, number in enumerate(teens)]
tens_list = [number.spoken_forms for i, number in enumerate(tens)]

# Maps spoken form to number 
digits_map = {
    spoken_form: number.number
    for number in digits
    for spoken_form in number.spoken_forms
}

teens_map = {
    spoken_form: number.number
    for number in teens
    for spoken_form in number.spoken_forms
}

tens_map = {
    spoken_form: number.number
    for number in tens
    for spoken_form in number.spoken_forms
}

scales_map = {
    spoken_form: number.number
    for number in scales
    for spoken_form in number.spoken_forms
}

# Maps number words to integers values that are used to compute numeric values.
numbers_map = digits_map.copy()
numbers_map.update(teens_map)
numbers_map.update(tens_map)
numbers_map.update(scales_map)

def get_spoken_form_under_one_hundred(
    start,
    end,
    include_oh_variant_for_single_digits,
    include_default_variant_for_single_digits,
    include_double_digits,
):
    """Helper function to get dictionary of spoken forms for non-negative numbers in the range [start, end] under 100"""

    result = {}

    for value in range(start, end + 1):
        digit_index = value % 10
        leading_digit_index = math.floor(value / 10) 
        digit_spoken_forms = digit_list[digit_index]
        leading_index_spoken_forms = digit_list[leading_digit_index]
        if value < 10:
            if include_oh_variant_for_single_digits:
                for digit_spoken_form in digit_spoken_forms:
                    result[f"oh {digit_spoken_form}"] = f"0{value}"
            if include_default_variant_for_single_digits:
                for digit_spoken_form in digit_spoken_forms:
                    result[f"{digit_spoken_form}"] = f"{value}"
        elif value < 20:
            teens_index = value - 10
            teens_spoken_forms = teens[teens_index].spoken_forms
            for spoken_form in teens_spoken_forms:
                result[f"{spoken_form}"] = f"{value}"
        elif value < 100:
            tens_index = math.floor(value / 10) - 2
            tens_spoken_forms = tens_list[tens_index]
            if digit_index > 0:
                for tens_spoken_form in tens_spoken_forms:
                    for digit_spoken_form in digit_spoken_forms:
                        spoken_form = f"{tens_spoken_form} {digit_spoken_form}"
                        result[spoken_form] = f"{value}"

            else:
                for tens_spoken_form in tens_spoken_forms:
                    result[f"{tens_spoken_form}"] = f"{value}"

        if include_double_digits and leading_digit_index > 1:
            for leading_index_spoken_form in leading_index_spoken_forms:
                for digit_spoken_form in digit_spoken_forms:
                    spoken_form = f"{leading_index_spoken_form} {digit_spoken_form}"
                    result[spoken_form] = f"{value}"
    return result
