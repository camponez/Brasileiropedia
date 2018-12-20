#!/bin/env python
from urllib import request
import os

"""
TODO:
    reservas
    cartoes
    arbitros
    gol timestamp
    download sumula
"""


def substring_indexes(substring, string):
    """
    Generate indices of where substring begins in string

    >>> list(find_substring('me', "The cat says meow, meow"))
    [13, 19]
    """
    last_found = -1  # Begin at -1 so the next position to search from is 0
    while True:
        # Find next index of substring, by starting after its last known
        # position
        last_found = string.find(substring, last_found + 1)
        if last_found == -1:
            break  # All occurrences have been found
        yield last_found


def extract_num_name(txt):
    mark_num = '<span class="list-number pull-left p-t-15 m-r-10 w-20">'
    indexes_num = substring_indexes(mark_num, txt)
    numbers = []
    for i in indexes_num:
        num = txt[i + len(mark_num):i + len(mark_num) + 2]
        num = num.replace('<', '')
        numbers.append(num)

    mark_name = '<span class="list-desc">'
    indexes_name = substring_indexes(mark_name, txt)
    names = []
    for i in indexes_name:
        name = txt[i + len(mark_name):i + len(mark_name) + 150]
        name = name.split('<')[0]
        names.append(name)
    mark_nick = '<strong class="block list-title p-b-5">'
    indexes_nick = substring_indexes(mark_nick, txt)
    nicks = []
    for i in indexes_nick:
        nick = txt[i + len(mark_nick):i + len(mark_name) + 80]
        nick = nick.split('<')[0]
        nick = nick.replace('\\r\\n', '').strip()
        nicks.append(nick)

    return numbers, names, nicks


def get_date_n_time2(full_txt):
    # GET THE DATE FROM THE <TITLE>
    mark = '<title>'
    title_loc = list(substring_indexes(mark, full_txt))
    title = full_txt[title_loc[0] + 7::]
    title_items = title.split('</title>')[0]
    title_items = title_items.split(' ')
    weekday = title_items[8][0:10]
    date = title_items[9].replace('/', '')
    time = title_items[10]
    return [date, weekday, time]


def get_date_n_time(full_txt):
    date_mark = 'class="glyphicon glyphicon-calendar"'
    time_mark = 'class="glyphicon glyphicon-time"'
    date_loc = next(substring_indexes(date_mark, full_txt))
    date = full_txt[date_loc + len(date_mark) + 6::].split('</span>')[0]
    weekday = date.split(',')[0]
    date = date.split(',')[1].strip()
    time_loc = next(substring_indexes(time_mark, full_txt))
    time = full_txt[time_loc + len(time_mark) + 6::].split('</span>')[0]
    return [date, weekday, time]


def get_date_filename(full_txt):
    # gets the date in the format ddmmyyyy
    mark = '<title>'
    title_loc = list(substring_indexes(mark, full_txt))
    title = full_txt[title_loc[0] + 7::]
    title_items = title.split('</title>')[0]
    title_items = title_items.split(' ')
    date = title_items[9].replace('/', '')
    return date


def get_match_result(txt):
    team_mark = '<h3 class="time-nome color-white">'
    lm = len(team_mark)
    team_loc = substring_indexes(team_mark, txt)
    team1 = text[next(team_loc) + lm::].split(' ')[0]
    team2 = text[next(team_loc) + lm::].split(' ')[0]
    goal_mark = '<strong class="time-gols block">'
    gm = len(goal_mark)
    goal_loc = substring_indexes(goal_mark, txt)
    g1_loc = next(goal_loc) + gm
    goal1 = text[g1_loc:g1_loc + 1]
    g2_loc = next(goal_loc) + gm
    goal2 = text[g2_loc:g2_loc + 1]
    return team1, goal1, team2, goal2


def download_sumula(txt, sumula_name):
    sum_mark = 'https://conteudo.cbf.com.br/sumulas/2018/'
    sum_loc = next(substring_indexes(sum_mark, txt))
    url_sum = txt[sum_loc:sum_loc + 60].split('.pdf')[0] + '.pdf'
    request.urlretrieve(url_sum, sumula_name)


def save_file(team1, team2, date, template, rodada, txt):
    file_name = rodada + '_' + team1[0:2] + team2[0:2] + date
    path = '/brasileiro/'
    file_path = os.getcwd() + path + file_name
    f = open(file_path, 'w')
    f.write(template)
    f.close()
    sumula_name = 'Brasileirao Serie A/' + rodada + \
        ' Rodada/' + team1[0:3] + team2[0:3] + date + '.pdf'
    download_sumula(txt, sumula_name)


matches = list(range(1, 380))
matches_list = []
# formats the match ids into a 3 digit number to generate the URLs
for item in matches:
    item = str(item)
    if len(item) == 1:
        item = "00" + item
    if len(item) == 2:
        item = "0" + item
    matches_list.append(item)

for match_id in matches_list:
    if int(match_id) % 10 == 0:
        print('Generating round ' + str(int(match_id) / 10) + '.')
    # loops the whole code through all the matches
    link = "https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/2018/" + match_id
    # ending = ['#escalacao', '#alteracao', '#arbitros', '#documentos',
    # '#resumo']

    f = request.urlopen(link)
    myfile = f.read()
    myfile = myfile.decode('UTF-8')
    text = str(myfile)
    id_escalacao_beg = text.find('<tab id="escalacao"')
    id_escalacao_end = text[id_escalacao_beg::].find(
        '</tab>') + id_escalacao_beg
    escalacao_text = text[id_escalacao_beg:id_escalacao_end]

    rodada = str(int(match_id[0:2]) + 1)
    date, weekday, time = get_date_n_time(text)
    ddmmyyyy = get_date_filename(text)
    team1, goal1, team2, goal2 = get_match_result(text)
    numbers, players, nicks = extract_num_name(escalacao_text)
    dummy = ''
    player_list_mandante_formated = ''
    nome_sumula = team1[0:3] + team2[0:3] + ddmmyyyy
    for i in range(0, 11):
        player = "[[" + players[i] + "|" + nicks[i] + "]]"
        j = "|n" + str(i + 1) + ".1 = " + numbers[i] + "\n"
        n = "|j" + str(i + 1) + ".1 = " + player + '\n'
        player_list_mandante_formated += j + n
    player_list_visitante_formated = ''
    for i in range(0, 11):
        player = "[[" + players[i + 20] + "|" + nicks[i + 20] + "]]"
        j = "|n" + str(i + 1) + ".2 = " + numbers[i] + "\n"
        n = "|j" + str(i + 1) + ".2 = " + player + '\n'
        player_list_visitante_formated += j + n
    player_formated = player_list_mandante_formated + player_list_visitante_formated
    player_list_mandante = ';\n'.join(players[0:11])
    reserves_list_mandante = ';\n'.join(players[11:21])
    player_list_visitante = ';\n'.join(players[21:32])
    reserves_list_visitante = ';\n'.join(players[32::])
    template = "{{Ficha \n" + \
    "\n| mandante = " + team1 + \
    "\n| golsmandante = " + goal1 + \
    "\n| visitante = " + team2 + \
    "\n| golsvisitante = " + goal2 + \
    "\n| motivo = " + rodada + \
        "ª rodada do [[Masculino Série A 2018|Campeonato Brasileiro 2018 - Série A]] " +\
    "\n| dia = " + date[0:-6] + \
    "\n| ano = " + date[-4::] + \
    "\n| hora = " + time + \
    "\n| bandeira_arbitragem = " + \
    "\n| arbitro = " + dummy + \
    "\n| auxiliar1 = " + dummy + \
    "\n| auxiliar2 = " + dummy + \
    "\n| cidade = " + dummy + \
    "\n| uf = " + dummy + \
    "\n| estadio = " + dummy + \
    "\n| pagante = " + dummy + \
    "\n| presente = " + dummy + \
    "\n| renda =  " + \
    "\n| sumula = {{cbf_sumula|arquivo=" + nome_sumula + "}}" + \
    "\n" + player_formated + \
    "\n}}"  + \
    "\n{{#set:  "+ \
    "\nTitularMandante= " + player_list_mandante + \
    "\n|+sep=;" +  \
    "\n|ReservaMandante= " + reserves_list_mandante + \
    "\n|+sep=;" +  \
    "\n|TitularVisitante= " + player_list_visitante + \
    "\n|+sep=;" +  \
    "\n|ReservaVisitante= " + reserves_list_visitante + \
    "\n|+sep=;" +  \
    "\n|AmareloMandante= " + dummy + \
    "\n|+sep=;" +  \
    "\n|AmareloVisitante= " + dummy + \
    "\n|+sep=;" +  \
    "\n|VermelhoMandante= " + dummy + \
    "\n|+sep=;" +  \
    "\n|VermelhoVisitante= " + dummy + \
    "\n|+sep=;" +  \
    "\n|Gol1Mandante= " + dummy + \
    "\n|+sep=;" +  \
    "\n|Gol2Mandante= " + dummy + \
    "\n|+sep=;" +  \
    "\n|Gol3Mandante= " + dummy + \
    "\n|+sep=;" +  \
    "\n|Gol4Mandante= " + dummy + \
    "\n|+sep=;" +  \
    "\n|Gol5Mandante= " + dummy + \
    "\n|+sep=;" +  \
    "\n|Gol1Visitante= " + dummy + \
    "\n|+sep=;" +  \
    "\n|Gol2Visitante= " + dummy + \
    "\n|+sep=;" +  \
    "\n|Gol3Visitante= " + dummy + \
    "\n|+sep=;" + \
    "\n|Gol4Visitante= " + dummy + \
    "\n|+sep=;" + \
    "\n}}" +  \
    "\n{{DEFAULTSORT: 2018-12-02}}" + \
    "\n{{Masculino Série A 2018}}"

    save_file(team1, team2, ddmmyyyy, template, rodada, text)
