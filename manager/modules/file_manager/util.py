import os


def is_file(file: str) -> bool:
    return os.path.isfile(file)

def is_folder(folder: str) -> bool:
    return os.path.isdir(folder)
