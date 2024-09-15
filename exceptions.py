"""Module for custom exceptions"""


class FantasyProjectionsError(Exception):
    pass


class UnrecognizedPlayerError(FantasyProjectionsError):
    def __init__(self, player: str, reader_file: str, message: str = "Unrecognized player"):
        self.player = player
        self.reader_file = reader_file
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"\nUnrecognized player '{self.player}' in {self.reader_file}.\nConsider updating FantasyConfig.normalized_player_names."


#class AlreadyAddedError(YahooFantasyError):
#    def __init__(self, player: str, message: str = "Already added player"):
#        self.player = player
#        self.message = message
#        super().__init__(self.message)
#
#    def __str__(self):
#        return f'Player "{self.player}" is already added to roster.'
