from reader.kkupfl import KKUPFLAdpReader


if __name__ == '__main__':
    kkupfl = KKUPFLAdpReader('KKUPFL_2023_2024_Mock_ADP.xlsx')
    mcdavid = kkupfl.get_player("Connor McDavid")
    players = kkupfl.get_players(["Rob", "Tim"])
    import ipdb; ipdb.set_trace()
