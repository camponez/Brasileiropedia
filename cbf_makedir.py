import os

path = os.getcwd()
os.mkdir(path+'Brasileirao Serie A')
os.chdir(path+'/Brasileirao Serie A')
rodadas = range(1,39)
for i in rodadas:
    path_name = str(i) +' Rodada'
    os.mkdir(path_name)
