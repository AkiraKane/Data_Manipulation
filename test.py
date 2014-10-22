import csv

cmn_games = []
with open('cmn_games.csv', 'r') as op:
    cmn_gms = csv.reader(op)
    for row in cmn_gms:
        cmn_games.extend(row)

cmn_games = sorted(cmn_games)
print cmn_games[:10]