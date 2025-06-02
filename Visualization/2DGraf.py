###############################
# Graph generation for thesis #
###############################

import matplotlib.pyplot as plt
import json
import numpy as np
import statsmodels.api as sm

VISTYPE = "Comments"
# VISTYPE = "Followers"
# VISTYPE = "Following"

colors = {
    "Comments" : "green",
    "Followers": "orange",
    "Following": "blue"
}

text = {
    "Comments" : {
        "x": "Celkový počet komentárov",
        "y": "Počet zozbieraných komentárov",
        "title": "Pomer celkového a zozbieraného počtu komentárov"
    },
    "Followers": {
        "x": "Celkový počet sledovateľov",
        "y": "Počet zozbieraných sledovateľov",
        "title": "Pomer celkového a zozbieraného počtu sledovateľov"
    },
    "Following": {
        "x": "Celkový počet sledovaných",
        "y": "Počet zozbieraných sledovaných používateľov",
        "title": "Pomer celkového a zozbieraného počtu sledovaných používateľov"
    }
}

with open("../Data/Information/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

counts = []

for user, info in data.items():
    if VISTYPE == "Comments":
        total = info["totalCommentsCount"]
        shown = info["shownCommentsCount"]

        if total != 0 and shown != 0:
            counts.append([total, shown])

    if VISTYPE == "Followers":
        total = info["totalFollowersCount"]
        shown = info["shownFollowersCount"]

        if total != 0 and shown != 0:

            counts.append([total, shown])

    if VISTYPE == "Following":
        total = info["totalFollowingCount"]
        shown = info["shownFollowingCount"]

        if total != 0 and shown != 0:
            counts.append([total, shown])


counts = sorted(counts, key=lambda x: x[0])

print(counts)

x,y = zip(*counts)

plt.figure(figsize=(12,6))

if VISTYPE == "Followers":
    lowess = sm.nonparametric.lowess
    y_smooth = lowess(y, np.log10(x), frac=0.2)

    plt.plot(10**y_smooth[:, 0], y_smooth[:, 1], color='orange')
else:
    plt.plot(x, y, marker='', linestyle='-', color=colors[VISTYPE])


plt.title(text[VISTYPE]["title"], fontsize=14)
plt.xscale("log")
plt.xlabel(text[VISTYPE]["x"], fontsize=12)
plt.ylabel(text[VISTYPE]["y"], fontsize=12)
plt.grid(True)

plt.savefig(f"graph{VISTYPE}.png", dpi=300, bbox_inches='tight')
plt.show()
