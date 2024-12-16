class Application:
    """Class for tracking application information for launching, switching etc"""
    path: str
    display_name: str
    unique_identifier: str
    executable_name: str
    exclude: bool 
    spoken_forms: list[str]
    application_group: str
    is_default_for_application_group: False

    def __init__(self, 
                 path:str, 
                 display_name: str, 
                 unique_identifier: str, 
                 executable_name: str, 
                 exclude: bool, 
                 spoken_form: list[str],
                 application_group: str = None,
                 is_default_for_application_group = False):
        self.path = path
        self.display_name = display_name
        self.executable_name = executable_name 
        self.unique_identifier = unique_identifier
        self.exclude = exclude
        self.spoken_forms = spoken_form
        self.application_group = application_group
        self.is_default_for_application_group = is_default_for_application_group

    def __str__(self) -> str:
        spoken_form = None
        if self.spoken_forms:
            spoken_form = ";".join(self.spoken_forms)

        if self.application_group:
            return f"{self.display_name},{spoken_form},{self.exclude},{self.unique_identifier},{self.path},{self.executable_name},{self.application_group},{self.is_default_for_application_group}"
        
        return f"{self.display_name},{spoken_form},{self.exclude},{self.unique_identifier},{self.path},{self.executable_name}"

class ApplicationGroup:
    """Class for tracking an application group"""
    group_name: str
    path: str
    executable_name: str
    unique_id: str
    group_spoken_forms: list[str]

    #window title to spoken form
    spoken_forms: dict[str, str] = {}

    def __str__(self) -> str:
        return f"{self.group_name}\n\t{self.group_spoken_forms}\n\t{self.path}\n\t{self.unique_id},\n\t{self.path},\n\t{self.executable_name},\n\t{self.spoken_forms}"