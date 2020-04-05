from itertools import islice
import re
import os
selection_numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty',]

MAX = 100

pattern = re.compile(r"[A-Z][a-z]*|[a-z]+|\d")
def create_spoken_forms(symbols, max_len=10):
    return [' '.join(list(islice(pattern.findall(s), max_len))) for s in symbols]

def get_directory_map(current_path):
    directories = [f.name for f in os.scandir(current_path) if f.is_dir()]
    print(len(directories))
    spoken_forms = create_spoken_forms(directories)
    return dict(zip(spoken_forms, directories))

def get_file_map(current_path):
    files = [f.name for f in os.scandir(current_path) if f.is_file()]
    spoken_forms = create_spoken_forms([p for p in files])
    return dict(zip(spoken_forms, [f for f in files]))