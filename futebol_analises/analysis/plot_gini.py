import operator

import matplotlib.pyplot as plt
import numpy
from scipy import stats

from crawlers.ogol_crawler import OGolTabelasCrawler
from utils.math import gini

crawler = OGolTabelasCrawler(30)

colors = {
    'Brasileirão': (44, 160, 44),
    'La Liga': (255, 127, 14),
    'Bundesliga': (214, 39, 40),
    'Premier League': (31, 119, 180)
}

for k, v in colors.items():
    r, g, b = v
    colors[k] = (r / 255., g / 255., b / 255.)

fig, ax = plt.subplots()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

oldest_record = 9999
newest_record = 0
for color_id, competition in enumerate(crawler.ID_COMPETITIONS.keys()):
    pontos_corridos_sample = crawler.get_parameter_per_year(3, competition)

    gini_year = {}
    for y, p in pontos_corridos_sample.items():
        oldest_record = int(y) if int(y) < oldest_record else oldest_record
        newest_record = int(y) if int(y) > newest_record else newest_record
        gini_year[int(y)] = gini(p)

    gini_year = sorted(gini_year.items(), key=operator.itemgetter(0))
    x = [numpy.float64(k[0]) for k in gini_year]
    y = [k[1] for k in gini_year]
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        x, y)

    line = [slope * i + intercept for i in x]
    ax.plot(x, y, '.', x, line, label=competition,  color=colors[competition])
    ax.text(x[-1] + 0.15, line[-1] - 0.002, competition
            , fontsize=10, color=colors[competition])

for y in range(75, 250, 25):
    plt.plot(range(oldest_record, newest_record),
             [y*0.001] * len(range(oldest_record, newest_record)), "--"
             , lw=0.5, color="black", alpha=0.3)

plt.xlim(oldest_record - 0.25, newest_record + 0.25)
ax.set_title('Coeficiente de Gini por Competição de Futebol (1988 - 2017)')
plt.show()


