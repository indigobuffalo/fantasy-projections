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

## Excluding Players

## Filtering by Position

## Limiting Results

```
(fantasy-projections) ➜  fantasy-projections git:(main) ✗ python main.py kkupfl --count 10 --position SKT

Steve Laidlaw reader does not support position filtering
==========
KKUPFL ADP
==========
(10 players)
 Full MOCK ADP            Player   POS POS Rank  Count  Min  Max  Variance
           47.0   Mika Zibanejad     C      C21   54.0 33.0 63.0      30.0
           49.5   Travis Konecny LW,RW      W31   53.0 33.0 66.0      33.0
           53.1      Matt Barzal  C,RW      W32   54.0 38.0 70.0      32.0
           54.5 Carter Verhaeghe  C,LW      W33   53.0 45.0 65.0      20.0
           55.5   Josh Morrissey     D       D9   52.0 39.0 76.0      37.0
           57.0 Joel Eriksson Ek     C      C24   52.0 37.0 77.0      40.0
           57.5  Dougie Hamilton     D      D10   53.0 42.0 89.0      47.0
           58.1    Chris Kreider    LW      W34   53.0 37.0 78.0      41.0
           58.5      Kevin Fiala LW,RW      W35   53.0 43.0 83.0      40.0
           59.5   Wyatt Johnston  C,RW      W36   53.0 44.0 73.0      29.0
====================
Elite Prospects Rank
====================
(10 players)
 Rank                Name   Pos Team  Points  Games  Goals  Assists
   23       Robert Thomas  C/RW  STL      88     82     24       64
   34       Lucas Raymond LW/RW  DET      81     81     37       44
   35 Ryan Nugent-Hopkins  C/LW  EDM      80     82     28       52
   37      Wyatt Johnston  C/RW  DAL      79     80     38       41
   39         Seth Jarvis    RW  CAR      78     80     35       43
   40         Nick Suzuki  C/RW  MTL      78     78     28       50
   44    Vincent Trocheck     C  NYR      77     79     29       48
   47         Kevin Fiala LW/RW  LAK      75     78     29       46
   48      Mika Zibanejad     C  NYR      75     79     33       42
   49        Brock Boeser    RW  VAN      75     78     37       38
=============
Steve Laidlaw
=============
(10 players)
 Rank            Name  GP  G  A  P  PPP  SOG  Hits  Blks
   24    Aaron Ekblad  65 13 36 49   20  195    88    70
   25 Dougie Hamilton  70 14 37 51   23  222    67    85
   29    John Carlson  80 13 44 57   23  200    74   170
   33   Morgan Rielly  73  8 52 60   20  167    90   114
 

```


## Projection Sources

- KKUPFL ADP: (KKUPFL Discord channel)
- KKUPFL Scoring (KKUPFL Discord channel)
- Steve Laidlaw (he shared for free via Twitter @SteveLaidlaw)
- Dom Luszczyszyn (from the Athletic)

## TODOs

- Make the historic points reader display set of players matched by all other readers
- Refactor to move logic out of main.py and into controller
  - Consider service layer between controller and readers (DAOs)
- Scripts
  - Convert fantrax live drafted list into python list for pasting undeder KKUPFL_DRAFTED_PLAYERS
  - Translate positions 
