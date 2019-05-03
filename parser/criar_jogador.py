#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parser.parser_cbf import Masculino
from parser.parser_cbf import Feminino

from urllib import request
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # jogos = range(1, 200)
    JOGOS = [14, 13, 15]
    jogadores = []
    for jogo in JOGOS:
        # serie_path = 'serie-c'
        serie_path = 'feminino-a2'
        ano = 2019
        jog = 'jogadora'

        parser = Feminino('a2', ano, jogo, 'Série A2')
        # parser = Masculino('serie-c', 2018, jogo, 'Série C')
        content = request.urlopen(parser.url).read()
        SOUP = BeautifulSoup(content, 'html.parser')

        PLAYERS = SOUP.find(
            class_='jogo-escalacao').find_all(class_='col-xs-6')

        f_name = '../../pywikipedia/jogadores_out.txt'
        man_vis = [0, 1]
        for i in man_vis:
            for player in PLAYERS[i].find_all('li'):
                parser.html = player
                player_name = parser.player_name()
                player_f_name = parser.player_full_name()

                if player_f_name in jogadores:
                    continue

                jogadores.append(player_f_name)
                out = '\nxxxx'
                out += "\n'''{}'''\n".format(player_f_name)
                out += "\n{{Info/Jogador" + \
                    "\n | nome          = {}".format(player_name) + \
                    "\n | nomecompleto  = {{PAGENAME}}" + \
                    "\n | posicao =" + \
                    "\n}}" +\
                    "\n\n== Jogos por clube =="

                if jog == 'jogadora':
                    out += "\n{{JogosPorClubeFeminino"
                else:
                    out += "\n{{JogosPorClube"

                out += "\n | {} ".format(jog) + " = {{PAGENAME}}" + \
                    "\n}}" + \
                    "\n\n== Jogos por série =="

                if jog == 'jogadora':
                    out += "\n{{JogosPorSerieFeminino"
                else:
                    out += "\n{{JogosPorSerieMasculino"

                out += "\n | {} ".format(jog) + " = {{PAGENAME}}" + \
                    "\n}}"
                out += "\nyyyy"
                print("Done: {}".format(player_name))
                f = open(f_name, 'a+')
                f.write(out)
                f.close()
        print('Criado {}'.format(f_name))
