import requests, os, zipfile

dir_name = 'dados_parlamentares' 

urls = ('http://www.camara.leg.br/cotas/Ano-2021.csv.zip',
        'http://www.camara.leg.br/cotas/Ano-2020.csv.zip',
        'http://www.camara.leg.br/cotas/Ano-2019.csv.zip',
        'http://www.camara.leg.br/cotas/Ano-2018.csv.zip',
        'http://www.camara.leg.br/cotas/Ano-2017.csv.zip',
        'http://www.camara.leg.br/cotas/Ano-2016.csv.zip',
        'http://www.camara.leg.br/cotas/Ano-2015.csv.zip',
        'http://www.camara.leg.br/cotas/Ano-2014.csv.zip', 
        'http://www.camara.leg.br/cotas/Ano-2013.csv.zip', 
        'http://www.camara.leg.br/cotas/Ano-2012.csv.zip',
        'http://www.camara.leg.br/cotas/Ano-2011.csv.zip',
        'http://www.camara.leg.br/cotas/Ano-2010.csv.zip',
        'http://www.camara.leg.br/cotas/Ano-2009.csv.zip')

if not os.path.exists(dir_name):
    os.mkdir(dir_name)
#ESSA ETAPA DEVE DEMORAR ALGUNS MINUTOS , POIS ELE BAIXA TODOS OS ARQUIVOS ZIP DA INTERNET
#E DEPOIS LÊ OS ARQUIVOS CSV
for url in urls:
    r = requests.get(url, allow_redirects=True)
    file_name = url.split('/')[-1]
    with open(file_name, 'wb') as f:
        f.write(r.content)
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall(dir_name)
    if os.path.exists(file_name):
        os.remove(file_name)

def le_dados(filename):

    with open(filename, 'r', encoding='UTF-8') as file:
        dados = []

        for line in file:

            dados.append(line.rstrip().replace('","','";"').split('";"'))
            dados[-1][0]=dados[-1][0].replace('"','')
            dados[-1][-1]=dados[-1][-1].replace('"','')

    rotulos = dados.pop(0)
    
    return rotulos, dados

import matplotlib.pyplot as plt

def modificaAno(ano):
    texto = "dados_parlamentares/Ano-"+ str(ano) + ".csv"
    return texto

def calculaGastosAno(ano):
    x = 0.0
    texto = modificaAno(ano)
    dados = le_dados(texto)[1]
    for c in range(0,len(dados)):
        x = x + float(dados[c][19])
    return x   

def criaLista():
    gastos = list()
    for c in range(2009,2022):
        totalGastos = 0.0
        totalGastos = calculaGastosAno(c)
        gastos.append(totalGastos/1000000)
    return gastos

def criaGrafico1():
    xL = [2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]
    yL = [120.0,140.0,160.0,180.0,200.0,220.0]
    listaGastos = criaLista()
    plt.title("Total de gastos parlamentares entre 2009 e 2021")
    plt.ylabel("Gasto (em milhões de reais)")
    plt.xlabel("Ano")
    plt.plot(xL,listaGastos) 
    plt.xticks(xL,rotation=45)
    plt.yticks(yL)
    plt.grid(True)
    plt.show()

criaGrafico1()

def depMaisGastaram2021():
    listaGastos = list()
    texto = modificaAno(2021)
    dados = le_dados(texto)[1]
    gasto = 0.0
    deputado = dados[0][0]
    partido = dados[0][6]
    for c in range(0,len(dados)):
        if dados[c][6] != "" and dados[c][5] != "NA":
            if dados[c][0] != deputado:
                listaGastos.append((deputado,(gasto/1000000),partido))
                deputado = dados[c][0]
                partido = dados[c][6]
                gasto = float(dados[c][19])
            else:
                gasto = gasto + float(dados[c][19])
                if len(dados)-1 == c:
                    listaGastos.append((deputado,(gasto/1000000),partido))
    listaGastos.sort(key=lambda e:e[1],reverse=True)
    return listaGastos

def criaGrafico2():
    deputados = list()
    gastos = list()
    valores = [0.0,0.1,0.2,0.3,0.4,0.5]
    marcador = list(range(0,20,1))
    lGasto = depMaisGastaram2021()
    lGasto = lGasto[0:20]
    
    for c in range(0,len(lGasto)):
        deputados.append(lGasto[c][0])
        gastos.append(lGasto[c][1])

    plt.title("Parlamentares que mais gastaram em 2021")
    plt.ylabel("Gasto (em milhões de reais)")
    plt.bar(deputados,gastos)
    plt.xticks(marcador,deputados,rotation=90)
    plt.yticks(valores)
    plt.show()

criaGrafico2()

def partidosMaisGastaram():
    info = depMaisGastaram2021()
    info.sort(key=lambda e:e[2])
    listaGastoPartidos = list()
    quant_dep = 1

    for c in range(0,len(info)):

        if c == 0:
            quant_dep = 1
            deputado = info[0][0]
            gasto = info[0][1]
            partido = info[0][2]
        else:
            if info[c-1][2] == info[c][2]: #PARTIDO ATUAL É IGUAL AO ANTERIOR
                gasto = gasto + info[c][1]
                if info[c-1][0] != info[c][0]:
                    quant_dep = quant_dep + 1
                if c == len(info)-1:
                    listaGastoPartidos.append((partido,(gasto / quant_dep)))
            else:
                listaGastoPartidos.append((partido,(gasto / quant_dep)))
                quant_dep = 1
                deputado = info[c][0]
                gasto = info[c][1]
                partido = info[c][2]

    listaGastoPartidos.sort(key=lambda e:e[1],reverse=True)
    return listaGastoPartidos



def criaGrafico3():
    partidos = list()
    gastoMedio = list()
    valores = [0.00,0.05,0.10,0.15,0.20,0.25,0.30,0.35]
    listGastos = partidosMaisGastaram()
    marcador = range(0,len(listGastos),1)
    
    for c in range(0,len(listGastos)):
        partidos.append(listGastos[c][0])
        gastoMedio.append(listGastos[c][1])

    
    plt.title("Gasto Médio dos Partidos em 2021")
    plt.ylabel("Gasto (em milhões de reais)")
    plt.bar(partidos,gastoMedio)
    plt.xticks(marcador,partidos,rotation=90)
    plt.yticks(valores)
    plt.show()

criaGrafico3()

def depMaisGastaram2021Estado():
    listaGastos = list()
    texto = modificaAno(2021)
    dados = le_dados(texto)[1]
    gasto = 0.0
    deputado = dados[0][0]
    estado = dados[0][5]
    partido = dados[0][6]
    for c in range(0,len(dados)):
        if dados[c][6] != "" and dados[c][5] != "NA":
            if dados[c][0] != deputado:

                listaGastos.append((deputado,(gasto/1000000),partido,estado))
                deputado = dados[c][0]
                estado = dados[c][5]
                partido = dados[c][6]
                gasto = float(dados[c][19])
            else:
                gasto = gasto + float(dados[c][19])
                if len(dados)-1 == c:
                    listaGastos.append((deputado,(gasto/1000000),partido,estado))
    listaGastos.sort(key=lambda e:e[1],reverse=True)
    return listaGastos

def estMaisGastaram2021():
    info = depMaisGastaram2021Estado()
    info.sort(key=lambda e:e[3])
    listaGastoEstados = list()
    quant_dep = 1
    gasto = 0.0
    for c in range(0,len(info)):
        if info[c][3] != "NA":
            if c == 0:
                quant_dep = 1
                gasto = info[0][1]
                partido = info[0][2]
                estado = info[0][3]
            else:
                if info[c-1][3] == info[c][3]: #ESTADO ATUAL É IGUAL AO ANTERIOR
                    gasto = gasto + info[c][1]
                    if info[c-1][0] != info[c][0]:
                        quant_dep = quant_dep + 1
                    if c == len(info)-1:
                        listaGastoEstados.append((estado,(gasto / quant_dep)))
                else:
                    listaGastoEstados.append((estado,(gasto / quant_dep)))
                    quant_dep = 1
                    gasto = info[c][1]
                    partido = info[c][2]
                    estado= info[c][3]
    listaGastoEstados.sort(key=lambda e:e[1],reverse=True)
    return listaGastoEstados

def criaGrafico4():
    estados = list()
    gastoMedio = list()
    valores = [0.00,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40]
    listGastos = estMaisGastaram2021()
    marcador = range(0,len(listGastos),1)
    
    for c in range(0,len(listGastos)):
        estados.append(listGastos[c][0])
        gastoMedio.append(listGastos[c][1])

    
    plt.title("Gasto Médio dos Parlamentares por Estado em 2021")
    plt.ylabel("Gasto (em milhões de reais)")
    plt.bar(estados,gastoMedio)
    plt.xticks(marcador,estados,rotation=90)
    plt.yticks(valores)
    plt.show()

criaGrafico4()
