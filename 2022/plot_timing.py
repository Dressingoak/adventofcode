import re
import pandas as pd
from matplotlib import pyplot as plt
import seaborn

pattern = re.compile(r"Dec (\d+), part (\d): [\S\s]+took (\d+\.\d+) (.*s)")

timing = []
with open("solutions.txt", "r") as f:
    lines = ""
    for line in f.readlines():
        lines += line
        m = pattern.match(lines)
        if m is not None:
            day, part, duration, unit = m.group(1, 2, 3, 4)
            match unit:
                case "s": row = (day, part, float(duration))
                case "s": row = (day, part, float(duration) / 1_000)
                case _: row = (day, part, float(duration) / 1_000_000)
            lines = ""
            timing.append(row)

df = pd.DataFrame(timing, columns=["day", "part", "duration"])
seaborn.catplot(data=df, x="day", y="duration", hue="part")
plt.xticks(rotation=90)
# plt.yscale("log")
plt.grid(b=True, which='major', linestyle='-')
plt.show(block=True)
