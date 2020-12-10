from pathlib import Path


def mkdirs(directories: list):
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
