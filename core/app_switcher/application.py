class Application:
    """Class for tracking application information for launching, switching etc"""
    path: str
    display_name: str
    unique_identifier: str
    executable_name: str
    exclude: bool 
    spoken_forms: list[str]

    def __init__(self, path:str, display_name: str, unique_identifier: str, executable_name: str, exclude: bool, spoken_form: list[str]):
        self.path = path
        self.display_name = display_name
        self.executable_name = executable_name 
        self.unique_identifier = unique_identifier
        self.exclude = exclude
        self.spoken_forms = spoken_form  

    def __str__(self):
        spoken_form = None
        if self.spoken_forms:
            spoken_form = ";".join(self.spoken_forms)

        return f"{self.display_name},{spoken_form},{self.exclude},{self.unique_identifier},{self.path},{self.executable_name}"
