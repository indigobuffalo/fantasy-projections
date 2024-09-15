#!/usr/bin/env bash

: '
Copy Fantrax live draft picks from the UI before running this script to extract, quote and comma delimit each player name.
Gets rid of the unwanted metadata (e.g. position, manager name, etc.) so that the player names can be pasted directly to the drafted players list in "input/drafted_kkupfl.py".

Example, converts this:

```
19	Elias PetterssonVAN- C,LW	 Dima	22
18	Quinn HughesVAN- D	 Colby	17
17	William NylanderTOR- RW	 Southpark	10
16	Brady TkachukOTT- C,LW	 usnoozeulose	15
15	Alex TuchBUF- RW	 jordan	98
14	Jack HughesNJ- C,LW	 Quinten	14
13	Kirill KaprizovMIN- LW	 Curtis	13
Round 1
12	Cale MakarCOL- D	 Curtis	9
11	Matthew TkachukFLA- LW,RW	 Quinten	12
10	Cole CaufieldMTL- LW,RW	 jordan	90
9	J.T. MillerVAN- C,RW	 usnoozeulose	11
8	Mikko RantanenCOL- RW	 Southpark	8
7	Leon DraisaitlEDM- C,LW	 Colby	7
6	Artemi PanarinNYR- LW	 Dima	6
5	Nikita KucherovTB- RW	 James	3
4	David PastrnakBOS- RW	 Vince	5
3	Auston MatthewsTOR- C	 Stephen	4
2	Nathan MacKinnonCOL- C	 Dan	2
1	Connor McDavidEDM- C
```

to this:

```
Elias Pettersson
Quinn Hughes
William Nylander
Brady Tkachuk
Alex Tuch
Jack Hughes
Kirill Kaprizov
Cale Makar
Matthew Tkachuk
Cole Caufield
J.T. Miller
Mikko Rantanen
Leon Draisaitl
Artemi Panarin
Nikita Kucherov
David Pastrnak
Auston Matthews
Nathan MacKinnon
Connor McDavid
```

'

#NOTE: Team abbrv can be 2 OR 3 letters, e.g. EDM, NJ

pbpaste | egrep '^[A-Za-z-]+\s[A-Za-z-]+(\s[A-Za-z-]+)?$' | sed 's/.*/"&",/'
