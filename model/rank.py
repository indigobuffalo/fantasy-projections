class Rank:
    def __init__(self, name: str, rank: float, source: str, weight):
        self.name = name
        self.rank = rank
        self.source = source
        self.weight = weight

    def __str__(self):
        return f"{self.source}: {round(self.rank, 2)}"
