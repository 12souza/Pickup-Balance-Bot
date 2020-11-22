import itertools

playerList = ["mightymouse", "hf", "Souz", "proonz", "m3d", "zed", "eDub", "lb"]

combos = list(itertools.combinations(playerList, 4))

for i in range(len(combos)):
    comboList = list(combos[i])
    print(comboList)