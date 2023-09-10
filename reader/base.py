from pathlib import Path

import pandas

PROJECTIONS_DIR = Path(__file__).parent.parent / "projections"


class BaseReader:
    def __init__(self, filename):
        self.df = pandas.read_excel(PROJECTIONS_DIR / filename)
