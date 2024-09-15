#!/usr/bin/env bash

: '
Copy Fantrax live draft picks from the UI before running this script to extract, quote and comma delimit each player name.
Gets rid of the unwanted metadata (e.g. position, manager name, etc.) so that the player names can be pasted directly to the drafted players list in "input/drafted_kkupfl.py".

Example, converts this:

```
srk908 drafted - 4-7 [49]
Steven Stamkos
C,LW,Skt
-NSH
K_Dev drafted - 4-8 [50]
Carter Verhaeghe
C,LW,Skt
-FLA
dk drafted - 4-9 [51]
Mika Zibanejad
```

to this:

```
"Steven Stamkos",
"Carter Verhaeghe",
"Mika Zibanejad",
```

'

pbpaste | egrep '^[A-Z.a-z-]+\s[A-Z.a-z-]+(\s[A-Za-z-]+)?$' | sed 's/.*/"&",/'
