from dataclasses import dataclass


@dataclass
class windows_shortcut:
    display_name: str
    full_path: str
    target_path: str
    arguments: str

    def __str__(self) -> str:
        return f"{self.display_name} {self.full_path} {self.target_path} {self.arguments}"