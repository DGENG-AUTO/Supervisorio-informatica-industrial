from biblioteca_tags import Biblioteca_tags
from datetime import datetime
from random import random
from pyModbusTCP.client import ModbusClient

from random import random

dic_cores = {}
_meas = {}
_meas['timestamp'] = None
_meas['values'] = {}

tags = Biblioteca_tags().get_tags()  
for tag in tags:
    nome = tag['nome']
    address = tag['address']
    
    if nome == 'bc.corrente_r':
        plot_color = (1, 0, 0, 1)
    else:
        plot_color = (random(), random(), random(), 1)

    dic_cores[nome] = {'address': address, 'color': plot_color}

#print(dic_cores)

for tag in dic_cores:
    endereço = dic_cores[tag]['address']
    print(endereço)
    
