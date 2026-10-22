from talon import Module, actions

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
        # Convert to integer
        newValue = int(value) / int(divide)
        return str(newValue)

