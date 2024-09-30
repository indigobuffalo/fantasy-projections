# fantasy-projections

Scripts for comparing and averaging fantasy rankings.

## Converting between Numbers and Excel

Microsoft Excel requires a paid subscription to save files.  To get around this, open in Numbers, make your edits, then export back to Excel.

Note: Don't include summary page when exporting to Excel.

# Usage

## Specifying Players to Search

See the lists under input/player_rgxs.py.
- QUICK_COMPARE: will be used if it's non-empty. Use it when you want to quickly compare a couple players, empty it otherwise.
- [KKUPFL|PA]_PLAYERS: self-explanatory

### Excluding Players

### Specifiying Regex on CLI
```
➜  python main.py kkupfl --position SKT -r 'M.*Reily,E.*Karl,Mik.*Serg'
```
### Filtering by Position
```
➜  python main.py kkupfl --position SKT
```

### Filtering by Position
```
➜  python main.py kkupfl --position SKT
```

### Limiting Results

```
➜  python main.py kkupfl --position SKT --count 10

==========
KKUPFL ADP
==========
(10 players)
 Full MOCK ADP            Player   POS POS Rank  Count  Min  Max  Variance
           47.0   Mika Zibanejad     C      C21   54.0 33.0 63.0      30.0
           49.5   Travis Konecny LW,RW      W31   53.0 33.0 66.0      33.0

...
```

## Projection Sources

- KKUPFL ADP: (KKUPFL Discord channel)
- KKUPFL Scoring (KKUPFL Discord channel)
- Steve Laidlaw (he shared for free via Twitter @SteveLaidlaw)
- Dom Luszczyszyn (from the Athletic)

## TODOs

- Scrub excel column names before putting them in.  This would be simplify the code as less normalization needed.
- Make the historic points reader display last 3 years plus average
  - Pandas probs has a good way to do this - https://stackoverflow.com/a/25058102 ?
- Refactor to move logic out of main.py and into controller
  - Consider service layer between controller and readers (DAOs)
- Scripts
  - Convert fantrax live drafted list into python list for pasting undeder KKUPFL_DRAFTED_PLAYERS
  - Translate positions 
