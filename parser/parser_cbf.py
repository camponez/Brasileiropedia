#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import locale
from time import strptime

from urllib import request
from bs4 import BeautifulSoup

SERIE = "serie-a/{}/{}"
# SERIE = "feminino-a1/{}/{}"
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

    def arbitragem(self):

        band = self.__html[2].text.strip()
        band2 = self.__html[5].text.strip()
        band3 = self.__html[8].text.strip()

        arbitros = {
            'bandeira': "{{Bandeira|" + band + "}}",
            'arbitro': {
                'nome': self.__html[0].text.strip(),
                'bandeira': None},
            'aux1': {
                'nome': self.__html[3].text.strip(),
                'bandeira': None if band2 == band
                else "{{Bandeira|" + band2 + "}}"},
            'aux2': {
                'nome': self.__html[6].text.strip(),
                'bandeira': None if band3 == band else
                "{{Bandeira|" + band3 + "}}"}
        }

        return arbitros

    def parse_page(self):
        """
        TODO: move all the parsing
        """
        pass


if __name__ == '__main__':
    serie_name = 'Série B'
    genero = 'Masculino '
    grupo = ''
    ano = 2018
    start = 131
    jogos = range(start, start + 30)
    for jogo in jogos:
        URL_FINAL = URL.format(ano, jogo)
        try:
            CONTENT = request.urlopen(URL_FINAL).read()
        except BaseException:
            print("Pulou {}".format(jogo))
            continue
        SOUP = BeautifulSoup(CONTENT, 'html.parser')

        PARSER = ParserCBF()
        PLAYERS = SOUP.find(
            class_='jogo-escalacao').find_all(class_='col-xs-6')

        PARSER.html = SOUP.find('table').find_all('td')
        arbitragem = PARSER.arbitragem()

        placar = SOUP.find(class_='section-placar')

        dia_mes = placar.find_all('span', class_='text-2')[1].text.strip()
        dt = strptime(dia_mes, '%A, %d de %B de %Y')

        dia_mes = re.search(r'(\d\d de \w+) de', dia_mes).group(1).lower()
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
        elif 'Eco-Estádio'.lower() in e_c_e.lower():
            estadio = 'Eco-Estádio'
            cidade = 'Curitiba'
            estado = 'PR'
        elif 'Ismael Benigno'.lower() in e_c_e.lower():
            estadio = 'Ismael Benigno'
            cidade = 'Colina'
            estado = 'AM'
        elif 'Bezerrão'.lower() in e_c_e.lower():
            estadio = 'Bezerrão'
            cidade = 'Valmir Campelo Bezerro'
            estado = 'DF'
        else:
            estadio, cidade, estado = e_c_e.split('-')

        times = placar.find_all('h3', class_='time-nome')

        def fix_nome(nome):
            r_out = nome.split('-')[0].strip()
            if 'Atlético - MG' in nome:
                r_out = 'Atlético-MG'
            elif 'Atlético - PR' in nome:
                r_out = 'Atlético-PR'
            elif 'Atletico - PR' in nome:
                r_out = 'Atlético-PR'
            elif 'Atlético - GO' in nome:
                r_out = 'Atlético-GO'
            elif 'Botafogo - PB' in nome:
                r_out = 'Botafogo-PB'
            elif 'América - MG' in nome:
                r_out = 'América-MG'
            elif 'Vitória - PE' in nome:
                r_out = 'Vitória-PE'
            elif 'Paran' in nome:
                r_out = 'Paraná Clube'
            elif 'Vasco da Gama' in nome:
                r_out = 'Vasco'
            elif 'Correa' in nome:
                r_out = 'Sampaio Corrêa'
            elif 'Csa' in nome:
                r_out = 'CSA'
            elif 'crb' in nome.lower():
                r_out = 'CRB'
            elif 'Brasil' in nome:
                r_out = 'Brasil de Pelotas'
            elif 'Boa' in nome:
                r_out = 'Boa Esporte'

            return r_out

        mandante_nome = fix_nome(times[0].text)
        visitante_nome = fix_nome(times[1].text)

        gols = placar.find_all('strong', class_='time-gols')

        def players(l_players):
            time = {
                'titular': [],
                'reserva': [],
                'banco': [],
                'amarelo': [],
                'vermelho': [],
                'gols': []}
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

        mes = str(dt.tm_mon)
        mes = "0{}".format(mes) if dt.tm_mon < 10 else mes

        dia = str(dt.tm_mday)
        dia = "0{}".format(dia) if dt.tm_mday < 10 else dia

        arquivo_sum_bor = mandante_nome[:3].lower() + \
            visitante_nome[:3].lower() + \
            dia + mes + str(dt.tm_year)

        out = "{{Ficha" + \
            "\n| mandante = {}".format(mandante_nome) + \
            "\n| golsmandante = {}".format(gols[1].text) + \
            "\n| visitante = {}".format(visitante_nome) + \
            "\n| golsvisitante = {}".format(gols[2].text) + \
            "\n| rodada = {}ª rodada{}".format(rodada, grupo) + \
            "\n| motivo = {}".format(serie_name) + \
            "\n| dia = {}".format(dia_mes) + \
            "\n| ano = {}".format(ano) + \
            "\n| hora = {}".format(hora).replace(':00', 'h') + \
            "\n| bandeira_arbitragem ={}".format(arbitragem['bandeira']) + \
            "\n| arbitro = {}".format(arbitragem['arbitro']['nome'])

        if arbitragem['aux1']['bandeira']:
            out += "\n| bandeira_auxiliar1 = {}".format(
                arbitragem['aux1']['bandeira'])

        out += "\n| auxiliar1 = {}".format(arbitragem['aux1']['nome'])

        if arbitragem['aux2']['bandeira']:
            out += "\n| bandeira_auxiliar2 = {}".format(
                arbitragem['aux2']['bandeira'])

        out += "\n| auxiliar2 = {}".format(arbitragem['aux2']['nome']) + \
            "\n| cidade = {}".format(cidade.strip()) + \
            "\n| uf = {}".format(estado.strip()) + \
            "\n| estadio = {}".format(estadio.strip()) + \
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
                out += " {{verm|}}"

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
                out += " {{verm}}"

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
        gols_vis = {i: visitante['gols'].count(
            i) for i in visitante['gols']}

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
            '-'.join([str(dt.tm_year), mes, dia])) + \
            "}}\n{{" + "{} {} {}".format(genero, serie_name, ano) + "}}"

        file_name = str(rodada) + "_" + mandante_nome[:3] + \
            visitante_nome[:3]

        print('Done jogo {}: {} {}x{} {}'.format(jogo, mandante_nome,
                                                 gols[1].text,
                                                 gols[2].text,
                                                 visitante_nome))
        link = 'https://brasileiropedia.com/{}_{}x{}_{}_-_{}/{}/{}'.format(
            mandante_nome.replace(' ', '_'), gols[1].text.strip(),
            gols[2].text.strip(), visitante_nome.replace(' ', '_'),
            dia, mes, dt.tm_year)
        out = "{}\n\n\n{}\n\n\n".format(URL_FINAL, link) + out
        file_path = "./{}/{}_{}.txt".format(ano, jogo, file_name)
        f = open(file_path, 'w')
        f.write(out)
        f.close()

        link_sum_b = 'https://conteudo.cbf.com.br/sumulas/{}/142{}.pdf\n'

        f_sum_b = open('sum_bor.list', 'a+')
        f_sum_b.write(link_sum_b.format(ano, str(jogo) + "se"))
        f_sum_b.write(link_sum_b.format(ano, str(jogo) + "b"))
        f_sum_b.close()

        print('Salvo em: {}'.format(file_path))
        print(link)
