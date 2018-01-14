#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

import numpy
from bs4 import BeautifulSoup
from selenium import webdriver

from utils.commons import try_parse


class OGolURL(object):
    def __init__(self):
        self.BASE_URL = 'https://www.ogol.com.br'
        self.EDITION_QUERY = '/competicao.php?id_comp={}'
        self.ID_COMPETITIONS = {
            'Brasileirão': 51,
            'La Liga': 5,
            'Premier League': 4,
            'Bundesliga': 11
        }

    def get_pontos_corridos_url(self, id_):
        return self.BASE_URL + self.EDITION_QUERY.format(id_)


class OGolTabelasCrawler(OGolURL):
    def __init__(self, n_of_years, store_data=True):
        super().__init__()
        self.n_of_years = n_of_years
        self._result = {}
        if not os.path.isfile('data.json'):
            self.driver = webdriver.Chrome('../chromedriver/chromedriver')
            self.parse_all_competitions(store_data)
        else:
            with open('data.json', 'r') as out_file:
                self._result = json.loads(out_file.read())

    def get_parameter_per_year(self, parameter, competition):
        response = {}
        for year, data in self._result[competition].items():
            if '/' in year:
                year = year.split('/')[0]
            year = int(year)
            response[year] = [int(d[parameter]) for d in data['table']]

        return response

    def get_champions_points(self, competition, participants=20):
        points = []
        years = []
        for y, data in self._result[competition].items():
            if len(data['table']) == participants:
                if '/' in y:
                    y = y.split('/')[0]
                points.append(int(data['table'][0][3]))
                years.append(int(y))

        return points, years

    def get_demoted_points(self, competition, participants=20):
        points = []
        years = []
        first_demoted = -2 if competition == 'Bundesliga' else -4
        for y, data in self._result[competition].items():
            if len(data['table']) == participants:
                if '/' in y:
                    y = y.split('/')[0]
                points.append(
                    numpy.mean([int(p[3]) for p in data['table'][first_demoted:-1]])
                )
                years.append(int(y))

        return points, years

    def get_parameter_per_club(self, parameter, competition, participants=20):
        response = {}
        used_years = []
        for year, data in self._result[competition].items():
            # club name =
            if '/' in year:
                year = int(year.split('/')[0])
            if len(data['table']) == participants \
                    and int(data['table'][0][4]) == participants * 2 - 2:
                for row in data['table']:
                    if len(row[1].strip()) and not try_parse(row[1]):
                        club_name = row[1]
                    else:
                        club_name = row[2]
                    if club_name == 'Man. United':
                        club_name = 'Manchester United'
                    if club_name == 'Alt. Madrid':
                        club_name = 'Atlético de Madrid'
                    if club_name not in response:
                        response[club_name] = []

                    response[club_name].append(
                        int(row[parameter])
                    )
                used_years.append(year)
        return response, used_years

    def get_and_avoid_ad(self, url):
        self.driver.get(url)
        try:
            self.driver.execute_script("""
                           return show_hidde_div('pub_frame', 'pub_bg');
                       """)
        except Exception as error:
            print('Ad not found keeping crawler '
                  'normally. ERROR: {}'.format(error))
        try:
            self.driver.switch_to.alert.accept()
        except Exception as error:
            print('Alert not found keeping crawler '
                  'normally. ERROR: {}'.format(error))

    def parse_all_competitions(self, store_data):
        for competition_name, id_ in self.ID_COMPETITIONS.items():
            url = self.get_pontos_corridos_url(id_)
            self.get_and_avoid_ad(url)
            # List all competitions in a range of n_of_years
            a_elements = self.driver.find_elements_by_tag_name('a')
            a_elements = [
                (a.text, a.get_attribute("href")) for a
                in a_elements if (
                        a.get_attribute("href")
                        and 'edition.php?id=' in a.get_attribute("href")
                        and a.text.strip()
                    )
                ]
            if 'Atual' in a_elements[0][0]:
                a_elements.pop(0)
            a_elements = a_elements[:self.n_of_years]
            for competition_year, comp_url in a_elements:
                print('Capturando temporada {}'.format(competition_year))
                self.get_and_avoid_ad(comp_url)
                # get the table
                edition_table = self.driver.find_element_by_id('edition_table')
                self.parse_edition_table(
                    edition_table.get_attribute('innerHTML'),
                    competition_year, competition_name
                )
        if store_data:
            with open('data.json', 'w') as outfile:
                json.dump(self._result, outfile)

    def parse_edition_table(self, raw_html, edition, competition):
        edition = edition.split('\n')[0]
        soup = BeautifulSoup(raw_html, 'lxml')
        header = soup.find('thead').find_all('th')
        columns = [h.text.strip() for h in header]
        rows = soup.find('tbody').find_all('tr')
        table = []
        for row in rows:
            cells = row.find_all('td')
            cells = [c.text.strip() for c in cells]
            table.append(cells)
        if competition not in self._result:
            self._result[competition] = {}
        self._result[competition][edition] = {
            'table': table,
            'columns': columns
        }

if __name__ == '__main__':
    crawler = OGolTabelasCrawler(15)
    c = crawler.get_parameter_per_year('P', 'Brasileirão')
    print(c)