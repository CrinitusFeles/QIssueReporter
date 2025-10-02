from pathlib import Path


def exe_cwd() -> Path:
    return Path(__file__).parent