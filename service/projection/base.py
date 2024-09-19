from input.drafted_kkupfl import KKUPFL_DRAFTED
from input.drafted_pa import PA_DRAFTED
from model.league import League


class ProjectionService:
    
    def __init__(self, league: str = None):
        self.league = League[league] if league is not None else None

    def get_excluded_for_league(self):
        if self.league == League.KKUPFL:
            return KKUPFL_DRAFTED
        elif self.league == League.PUCKIN_AROUND:
            return PA_DRAFTED

    def get_excluded(self, cli_rgxs: list[str] = None) -> list[str]:
        """Get list of players to exclude from results
    
        Args:
            league (str): Fantasy league
            cli_rgxs (list[str]): Regexes of players to exclude passed via CLI
    
        Returns:
            list[str]: List of players to exclude
        """
        excluded = list()
    
        if cli_rgxs is not None:
            excluded.extend(cli_rgxs)
        
        if self.league is not None:
            excluded.extend(self.get_excluded_for_league())
        
        return excluded