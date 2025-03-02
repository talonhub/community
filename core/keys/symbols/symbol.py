# define the spoken form for a single symbol
class Symbol:
    character: str
    spoken_forms: list[str] = None

    def __init__(self, character: str, spoken_forms):
        self.character = character

        if spoken_forms:
            self.spoken_forms = (
                [spoken_forms] if isinstance(spoken_forms, str) else spoken_forms
            )