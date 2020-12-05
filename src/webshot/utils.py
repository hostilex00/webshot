from pathlib import Path


def mkdirs(directories: []):
    """

    :return:
    """
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
