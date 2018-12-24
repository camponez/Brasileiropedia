#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import locale
from time import strptime

from urllib import request
from bs4 import BeautifulSoup

SERIE = "serie-a/{}/{}"
COMPETICAO = "campeonato-brasileiro-{}".format(SERIE)

URL = "https://www.cbf.com.br"
URL += "/futebol-brasileiro/competicoes/{}".format(COMPETICAO)

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class ParserCBF(object):

    """Parser para site CBF"""

    def __init__(self):
        """Initialize """
        self.__html = None

    @property
    def html(self):
        return self.__html

    @html.setter
    def html(self, value):
        self.__html = value

    def player_name(self):
        return self.__html.find(class_='block').text.strip().title()

    def player_number(self):
        try:
            return self.__html.find(class_='list-number').text
        except BaseException:
            __import__('pdb').set_trace()

    def player_full_name(self):
        full_name = self.__html.find(class_='list-desc').text.strip().title()
        full_name = full_name.replace(' De ', ' de ')
        full_name = full_name.replace(' Da ', ' da ')
        full_name = full_name.replace(' E ', ' e ')
        full_name = full_name.replace(' Dos ', ' dos ')
        full_name = full_name.replace(' Do ', ' do ')
        return full_name

    def titular(self):
        return not self.reserva()

    def reserva(self):
        return self.__html.has_attr('class')

    def gols(self):
        return len(self.__html.find_all('ellipse'))

    def amarelo(self):
        if not self.__html.i:
            return False
        return 'icon-yellow-card' in self.__html.i.get('class')

    def vermelho(self):
        if not self.__html.i:
            return False
        return 'icon-red-card' in self.__html.i.get('class')

    def parse_page(self):
        """
        TODO: move all the parsing
        """
        pass


if __name__ == '__main__':
    jogos = range(21, 31)
    ano = 2018
    for jogo in jogos:
        URL_FINAL = URL.format(2018, jogo)
        CONTENT = request.urlopen(URL_FINAL).read()
        SOUP = BeautifulSoup(CONTENT, 'html.parser')

        PARSER = ParserCBF()
        PLAYERS = SOUP.find(
            class_='jogo-escalacao').find_all(class_='col-xs-6')

        arbitragem = SOUP.find('table').find_all('td')

        arbitros = {'arbitro': arbitragem[0].text.strip(),
                    'aux1': arbitragem[3].text.strip(),
                    'aux2': arbitragem[6].text.strip()}

        placar = SOUP.find(class_='section-placar')

        dia = placar.find_all('span', class_='text-2')[1].text.strip()
        dt = strptime(dia, '%A, %d de %B de %Y')

        dia = re.search(r'(\d\d de \w+) de', dia).group(1).lower()
        hora = placar.find_all('span', class_='text-2')[2].text.strip()

        e_c_e = placar.find(class_='col-sm-8').span.text.strip()
        if 'Beira-Rio' in e_c_e:
            estadio = 'Beira-Rio'
            cidade = 'Porto Alegre'
            estado = "RS"
        elif 'Ceara-Mirim'.lower() in e_c_e.lower():
            estadio = 'Manoel Barreto'
            cidade = 'Ceará-Mirim'
            estado = 'RN'
        else:
            estadio, cidade, estado = e_c_e.split('-')

        times = placar.find_all('h3', class_='time-nome')
        mandante_nome = times[0].text.split('-')[0].strip()
        if 'Atlético - MG' in times[0]:
            mandante_nome = 'Atlético-MG'
        elif 'Atlético - PR' in times[0]:
            mandante_nome = 'Atlético-PR'
        elif 'Atlético - GO' in times[0]:
            mandante_nome = 'Atlético-GO'
        elif 'América - MG' in times[0]:
            mandante_nome = 'América-MG'

        visitante_nome = times[1].text.split('-')[0].strip()
        if 'Atlético - MG' in times[1]:
            visitante_nome = 'Atlético-MG'
        elif 'Atlétic_o - PR' in times[1]:
            visitante_nome = 'Atlético-PR'
        elif 'Atlétic_o - GO' in times[1]:
            visitante_nome = 'Atlético-GO'
        elif 'América_ - MG' in times[1]:
            visitante_nome = 'América-MG'

        gols = placar.find_all('strong', class_='time-gols')

        def players(l_players):
            time = {'titular': [], 'reserva': [], 'banco': [], 'amarelo': [],
                    'vermelho': [], 'gols': []}
            parser = ParserCBF()

            for player in l_players.find_all('li'):
                parser.html = player
                info = {'num': parser.player_number(),
                        'nome': parser.player_name(),
                        'nome_completo': parser.player_full_name(),
                        'amarelo': None,
                        'vermelho': None,
                        'gols': parser.gols(),
                        'reserva': None}
                time['gols'] += [parser.player_full_name()] * parser.gols()

                if parser.amarelo():
                    info['amarelo'] = True
                    time['amarelo'].append(info)

                if parser.vermelho():
                    info['vermelho'] = True
                    time['vermelho'].append(info)

                if parser.titular():
                    time['titular'].append(info)

                if parser.reserva():
                    time['reserva'].append(info)
                    time['titular'][-1]['reserva'] = info

            return time

        mandante = players(PLAYERS[0])
        visitante = players(PLAYERS[1])

        for i_player in PLAYERS[2].find_all('li'):
            PARSER.html = i_player
            info = {'num': PARSER.player_number(),
                    'nome': PARSER.player_name(),
                    'nome_completo': PARSER.player_full_name(),
                    'reserva': None}
            mandante['banco'].append(info)

        for i_player in PLAYERS[3].find_all('li'):
            PARSER.html = i_player
            info = {'num': PARSER.player_number(),
                    'nome': PARSER.player_name(),
                    'nome_completo': PARSER.player_full_name(),
                    'reserva': None}
            visitante['banco'].append(info)

        rodada = int(jogo / 10)
        rodada += 1 if jogo % 10 != 0 else 0

        arquivo_sum_bor = mandante_nome[:3].lower() + \
            visitante_nome[:3].lower() + \
            str(dt.tm_mday) + str(dt.tm_mon) + str(dt.tm_year)

        out = "{{Ficha" + \
            "\n| mandante = {} ".format(mandante_nome) + \
            "\n| golsmandante = {}".format(gols[1].text) + \
            "\n| visitante = {}".format(visitante_nome) + \
            "\n| golsvisitante = {}".format(gols[2].text) + \
            "\n| rodada = {}ª rodada".format(int(jogo / 10) + 1) + \
            "\n| motivo = [[Masculino Série A {}|".format(ano) + \
            "Campeonato Brasileiro {} - Série A]]".format(ano) + \
            "\n| dia = {}".format(dia) + \
            "\n| ano = {}".format(ano) + \
            "\n| hora = {}".format(hora).replace(':00', 'h') + \
            "\n| bandeira_arbitragem =" + \
            "\n| arbitro = {}".format(arbitros['arbitro']) + \
            "\n| auxiliar1 = {}".format(arbitros['aux1']) + \
            "\n| auxiliar2 = {}".format(arbitros['aux2']) + \
            "\n| cidade = {}".format(cidade.strip()) + \
            "\n| uf = {}".format(estado.strip()) + \
            "\n| estadio = {}".format(estadio) + \
            "\n| pagante =" + \
            "\n| presente =" + \
            "\n| renda = " + \
            "\n| sumula = {{" + \
            "cbf_sumula|arquivo={}".format(arquivo_sum_bor) + \
            "}}"
        i = 1
        for player in mandante['titular']:
            out += "\n| n{}.1 = {}".format(i, player['num'])
            out += "\n| j{}.1 = [[{}|{}]]".format(
                i, player['nome_completo'], player['nome'])
            out += " {{gol|}}" * player['gols']

            if player['amarelo']:
                out += " {{amar|}}"

            if player['vermelho']:
                out += " {{vermelho|}}"

            if player['reserva']:
                out += " {{subs|" + "{}. [[{}|{}]]".format(
                    player['reserva']['num'],
                    player['reserva']['nome_completo'],
                    player['reserva']['nome'])
                out += " {{gol|}}" * player['reserva']['gols']

                if player['reserva']['amarelo']:
                    out += " {{amar|}}"
                if player['reserva']['vermelho']:
                    out += " {{verm|}}"

                out += "| }}"
            i += 1

        out += "\n| tec1 = \n"

        i = 1
        for player in visitante['titular']:
            out += "\n| n{}.2 = {}".format(i, player['num'])
            out += "\n| j{}.2 = [[{}|{}]]".format(
                i, player['nome_completo'], player['nome'])

            out += " {{gol|}}" * player['gols']

            if player['amarelo']:
                out += " {{amar}}"

            if player['vermelho']:
                out += " {{vermelho}}"

            if player['reserva']:
                out += " {{subs|" + "{}. [[{}|{}]]".format(
                    player['reserva']['num'],
                    player['reserva']['nome_completo'],
                    player['reserva']['nome'])

                out += " {{gol|}}" * player['reserva']['gols']
                if player['reserva']['amarelo']:
                    out += " {{amar}}"
                if player['reserva']['vermelho']:
                    out += " {{verm}}"

                out += "| }}"
            i += 1

        out += "\n| tec2 = \n"

        i = 12
        for player in mandante['banco']:
            out += "\n| n{}.1 ={}".format(i, player['num'])
            out += "\n| j{}.1 =[[{}|{}]]".format(i, player['nome_completo'],
                                                 player['nome'])
            i += 1

        out += "\n"

        i = 12
        for player in visitante['banco']:
            out += "\n| n{}.2 ={}".format(i, player['num'])
            out += "\n| j{}.2 =[[{}|{}]]".format(i, player['nome_completo'],
                                                 player['nome'])
            i += 1

        out += "\n}}\n\n\n{{#set:\nTitularMandante="
        for i in mandante['titular']:
            out += "\n{};".format(i['nome_completo'])
        out += "\n|+sep=;"

        out += "\n\n|ReservaMandante="
        for i in mandante['reserva']:
            out += "\n{};".format(i['nome_completo'])
        out += "\n|+sep=;"

        out += "\n\n|TitularVisitante="
        for i in visitante['titular']:
            out += "\n{};".format(i['nome_completo'])
        out += "\n|+sep=;"

        out += "\n\n|ReservaVisitante="
        for i in visitante['reserva']:
            out += "\n{};".format(i['nome_completo'])
        out += "\n|+sep=;"

        if mandante['amarelo']:
            out += "\n\n|Amarelo1Mandante="
            for i in mandante['amarelo']:
                out += "\n{};".format(i['nome_completo'])
            out += "\n|+sep=;\n"

        if visitante['amarelo']:
            out += "\n\n|Amarelo1Visitante="
            for i in visitante['amarelo']:
                out += "\n{};".format(i['nome_completo'])
            out += "\n|+sep=;\n"

        if mandante['vermelho']:
            out += "\n\n|VermelhoMandante="
            for i in mandante['vermelho']:
                out += "\n{};".format(i['nome_completo'])
            out += "\n|+sep=;"

        if visitante['vermelho']:
            out += "\n\n|VermelhoVisitante="
            for i in visitante['vermelho']:
                out += "\n{};".format(i['nome_completo'])
            out += "\n|+sep=;\n"

        gols_man = {i: mandante['gols'].count(i) for i in mandante['gols']}
        gols_vis = {i: visitante['gols'].count(i) for i in visitante['gols']}

        def mostrar_gols(gols_j, num, m_v):
            r_out = "\n|Gol{}{}=".format(num, m_v)
            r_pl = ''
            for key in gols_j:
                if gols_j[key] >= num:
                    r_pl += '\n{};'.format(key)

            if not r_pl:
                return ''

            r_out += "{}\n|+sep=;\n".format(r_pl)
            return r_out

        for x in range(1, 5):
            out += mostrar_gols(gols_man, x, 'Mandante')

        for x in range(1, 5):
            out += mostrar_gols(gols_vis, x, 'Visitante')

        out += "}}\n\n{{DEFAULTSORT: " + " {}".format(
            '-'.join([str(dt.tm_year), str(dt.tm_mon), str(dt.tm_mday)])) + \
            "}}\n{{" + "Masculino Série A {}".format(2018) + "}}"

        file_name = str(rodada) + "_" + mandante_nome[:3] + \
            visitante_nome[:3]

        print('Done jogo {}: {} {}x{} {}'.format(jogo, mandante_nome,
                                                 gols[1].text,
                                                 gols[2].text,
                                                 visitante_nome))
        out = "{}\n\n\n".format(URL_FINAL) + out
        file_path = "./{}_{}.txt".format(file_name, jogo)
        f = open(file_path, 'w')
        f.write(out)
        f.close()

        link_sum_b = 'https://conteudo.cbf.com.br/sumulas/2018/142{}.pdf\n'

        f_sum_b = open('sum_bor.list', 'a+')
        f_sum_b.write(link_sum_b.format(str(jogo) + "se"))
        f_sum_b.write(link_sum_b.format(str(jogo) + "b"))
        f_sum_b.close()

        print('Salvo em: {}'.format(file_path))
