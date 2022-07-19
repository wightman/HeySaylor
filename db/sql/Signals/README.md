# Signals Table signalId Explanations
**5 + crud + table + version**
5 - required to keep signalID in MySQL above 45000
## crud
| digit 2 |   action   |
| ------- | ---------- |
| 1 | create/add |
| 2 | read |
| 3 | update |
| 4 | delete |
## table
| digit 3 |   table   |
| ------- | ---------- |
| 1 | Ships |
| 2 | Voyages |
| 3 | Fleets |
| 4 | Crews |
| 5 | Saylors |
| 6 | Wills |
| 7 | Users |
## version
There maybe several versions of crud+table operation,(e.g. various read oeprations) so this is just an identifier. 