#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parser.parser_cbf import ParserCBF
from parser.parser_cbf import URL

from urllib import request
from bs4 import BeautifulSoup

if __name__ == '__main__':
    jogos = range(1, 100)
    jogadores = []
    for jogo in jogos:
        serie_path = 'serie-c'
        # serie_path = 'feminino-a1'
        ano = 2017
        jog = 'jogador'

        url_final = URL.format(serie_path, ano, jogo)
        print(url_final)
        content = request.urlopen(url_final).read()
        SOUP = BeautifulSoup(content, 'html.parser')

        parser = ParserCBF()
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
                    "\n\n== Jogos por clube ==" + \
                    "\n{{JogosPorClube" + \
                    "\n | {} ".format(jog) + " = {{PAGENAME}}" + \
                    "\n}}" + \
                    "\n\n== Jogos por série ==" + \
                    "\n{{JogosPorSerieMasculino" + \
                    "\n | {} ".format(jog) + " = {{PAGENAME}}" + \
                    "\n}}"
                out += "\nyyyy"
                print("Done: {}".format(player_name))
                f = open(f_name, 'a+')
                f.write(out)
                f.close()
        print('Criado {}'.format(f_name))
