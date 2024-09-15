import os

class ProjectionFiles:
    BLAKE_KKUPFL = 'Blake-Reddit-KKUPFL.xlsx'
    BLAKE_PA = 'Blake-Reddit-PA.xlsx'
    DOM_KKUPFL = 'Dom-KKUPFL.xlsx'
    DOM_PA = 'Dom-PA.xlsx'
    ELITE_PROSPECTS = 'Elite-Prospects.xlsx'
    KKUPFL_ADP = 'KKUPFL-Mock-ADP.xlsx'
    KKUPFL_SCORING = 'KKUPFL-Scoring.xlsx'
    NHL = 'NHL-Dot-Com-projections.xlsx'
    STEVE_LAIDLAW = 'Steve-Laidlaw.xlsx'


class FantasyConfig:

    normalized_player_names = {
        # "ANOMOLY": "NORMALIZED"
        "ALEXANDER OVECHKIN": "Alex Ovechkin",
        "CAUL CAUFIELD": "COLE CAUFIELD",
        "DANIIL TARASOV (G)": "Daniil ",
        "ERIK GUSTAFSSON (D)": "Erik Gustafsson",
        "FREDERIK ANDERSON": "Frederik Andersen",
        "JOEL ERIKSSON-EK": "Joel Eriksson Ek",
        "JT MILLER": "J.T. Miller",
        "MATTHEW BOLDY": "Matt Boldy",
        "MATHEW BARZAL": "Matt Barzal",
        "MAT BARZAL": "Matt Barzal",
        "MICHAEL MATHESON": "Mike Matheson",
        "MITCHELL MARNER": "Mitch Marner",
        "PHOENIX COPLEY": "Pheonix Copley",
        "PILLIPP GRUBAUER": "Philipp Grubauer",
        "VITEK VANICEK": "Vitek Vanecek"
    }

    projection_files = ProjectionFiles

    schedule_file = 'Jeff-Mai-Schedule.xlsx'

    season = os.getenv('SEASON', '24-25')

    