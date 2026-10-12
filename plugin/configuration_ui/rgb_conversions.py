def hexadecimal_digit_to_decimal(digit):
    if digit.isdigit():
        return int(digit)
    return ord(digit.lower()) - ord("a") + 10


def parse_rgb_from_string(color):
    result = []
    for i in range(0, len(color), 2):
        value = hexadecimal_digit_to_decimal(
            color[i]
        ) * 16 + hexadecimal_digit_to_decimal(color[i + 1])
        result.append(value)
    return result


def convert_number_to_hexadecimal_digit(number: int):
    if number < 10:
        return str(number)
    return chr(number - 10 + ord("a"))


def convert_number_to_hexadecimal_string(number: int) -> str:
    """Assumes the number is between 0 and 255"""
    last_place = number % 16
    first_place = number // 16
    return f"{convert_number_to_hexadecimal_digit(first_place)}{convert_number_to_hexadecimal_digit(last_place)}"


def convert_rgb_to_string(rgb):
    hexadecimal_digits = [convert_number_to_hexadecimal_string(round(n)) for n in rgb]
    return "".join(hexadecimal_digits)


def is_valid_hexadecimal_digit(c):
    if c.isdigit():
        return True
    if not c.isalpha():
        return False
    character_number = ord(c.lower())
    return character_number >= ord("a") and character_number <= ord("f")


def is_valid_hexadecimal_rgb(text):
    return len(text) == 6 and all(is_valid_hexadecimal_digit(c) for c in text)