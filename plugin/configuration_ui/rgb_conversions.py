def parse_rgb_from_string(color):
    result = []
    for i in range(0, len(color), 2):
        result.append(int(color[i : i + 2], base=16))
    return result


def convert_number_to_two_digit_hexadecimal_string(number: int) -> str:
    if number == 0:
        return "00"
    return f"{number:x}"


def convert_rgb_to_string(rgb):
    hexadecimal_digits = [
        convert_number_to_two_digit_hexadecimal_string(round(n)) for n in rgb
    ]
    return "".join(hexadecimal_digits)


def is_valid_hexadecimal_rgb(text):
    if len(text) != 6:
        return False
    try:
        int(text, base=16)
        return True
    except ValueError:
        return False
