import numpy

from crawlers.ogol_crawler import OGolTabelasCrawler
import matplotlib.pyplot as plt


crawler = OGolTabelasCrawler(30)


for color_id, competition in enumerate(crawler.ID_COMPETITIONS.keys()):
    plt.subplot(2, 2, color_id + 1)
    axes = plt.gca()
    participants_cut = 18 if 'Bundesliga' in competition else 20

    pontos_corridos_sample, years_used = crawler.get_parameter_per_club(
        3, competition, participants_cut)

    participation_cut = 10
    names_list = []
    points_list = []
    pontos_corridos_sample = sorted(
        pontos_corridos_sample.items(),
        key=lambda x: -numpy.mean(x[1])
    )
    for club, points in pontos_corridos_sample:
        if len(points) >= participation_cut:
            names_list.append(club.replace(' ', '\n'))
            points_list.append([p for p in points])

    champion_points, _ = crawler.get_champions_points(
        competition, participants_cut)

    champion_mean_points = numpy.mean(champion_points)

    demoted_points, _ = crawler.get_demoted_points(
        competition, participants_cut)

    demoted_mean_points = numpy.mean(demoted_points)

    plt.plot(range(0, len(names_list) + 2),
             [champion_mean_points for _ in range(0, len(names_list) + 2)],
             "--", lw=0.5, color="black")

    plt.plot(range(0, len(names_list) + 2),
             [demoted_mean_points for _ in range(0, len(names_list) + 2)],
             "--", lw=0.5, color="black")

    flierprops = dict(marker='.', markersize=4, linestyle='none')
    plt.boxplot(points_list, flierprops=flierprops)

    y_limits = [axes.get_ylim()[0], axes.get_ylim()[1] + 1]
    axes.set_ylim(y_limits)

    plt.fill_between(range(0, len(names_list) + 2), y1=y_limits[1],
                     y2=champion_mean_points,
                     facecolor='green', interpolate=True, alpha=0.3)

    plt.fill_between(range(0, len(names_list) + 2), y2=y_limits[0],
                     y1=demoted_mean_points,
                     facecolor='red', interpolate=True, alpha=0.3)

    plt.xticks(range(len(names_list) + 1), [''] + names_list,
               size=6)

    plt.yticks([champion_mean_points, demoted_mean_points], fontsize=10)

    axes.set_title('Performance por clubes - {}'.format(competition))

    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)
    shift_text = 5 if competition == 'Brasileirão' else 10
    years_used = sorted(years_used)
    axes.text(axes.get_xlim()[1]/2, axes.get_ylim()[0] - shift_text,
              'Usando dados dos pontos corridos das temporadas {} a {}'.format(
        years_used[0], years_used[-1]),
              horizontalalignment='center')

plt.tight_layout()
plt.show()
