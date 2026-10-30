from talon import Module

mod = Module()


@mod.action_class
class Actions:
    def calculate_minus(value: str, take_off: str) -> str:
        """Calculate Result"""
        # Convert to integer
        newValue = int(value) - int(take_off)
        return str(newValue)

    def calculate_plus(value: str, add: str) -> str:
        """Calculate Result"""
        # Convert to integer
        newValue = int(value) + int(add)
        return str(newValue)

    def calculate_multiply(value: str, multiply: str) -> str:
        """Calculate Result"""
        # Convert to integer
        newValue = int(value) * int(multiply)
        return str(newValue)

    def calculate_divide(value: str, divide: str) -> str:
        """Calculate Result"""
        number = int(value)
        divisor = int(divide)

        if divisor == 0:
            print("Division by zero attempted")
            return "0"

        if abs(number) > 1_000_000 or abs(divisor) > 1_000_000:
            print("Number or divisor too large")
            return "0"

        # Convert to integer
        newValue = number / divisor
        return str(newValue)
