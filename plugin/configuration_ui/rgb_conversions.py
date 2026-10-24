ACCEPTED_RGB_STRING_LENGTH = 6


def parse_rgb_from_string(color):
    if len(color) != ACCEPTED_RGB_STRING_LENGTH:
        raise ValueError(
            f"RGB string {color} was not length {ACCEPTED_RGB_STRING_LENGTH}"
        )
    return [int("".join(channel), base=16) for channel in itertools.batched(color, 2)]


def convert_rgb_to_string(rgb):
    return "".join([f"{round(n):02x}" for n in rgb])
