ACCEPTED_RGB_STRING_LENGTH = 6


def parse_rgb_from_string(color):
    if len(color) != ACCEPTED_RGB_STRING_LENGTH:
        raise ValueError(
            f"RGB string {color} was not length {ACCEPTED_RGB_STRING_LENGTH}"
        )
    return [
        int(color[i : i + 2], base=16)
        for i in range(0, len(color), 2)
    ]


def convert_number_to_two_digit_hexadecimal_string(number: int) -> str:
    if number == 0:
        return "00"
    return f"{number:x}"


def convert_rgb_to_string(rgb):
    hexadecimal_digits = [
        convert_number_to_two_digit_hexadecimal_string(round(n)) for n in rgb
    ]
    return "".join(hexadecimal_digits)
