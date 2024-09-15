from service.projections import ProjectionsSvc


def write_consolidated_rankings(league: str, final_rankings: dict):
    controller = ProjectionsSvc(get_readers(league))
    write_consolidated_rankings(controller, league, averaged_rankings=averaged_rankings)