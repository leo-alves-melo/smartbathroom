import mraa
import random
import time
import sys
import math

trigPin = mraa.Gpio(2)
trigPin.dir(mraa.DIR_OUT)

echoPin = mraa.Gpio(3)
echoPin.dir(mraa.DIR_IN)

time.sleep(0.3)

pessoaEntra = 0
pessoaSai = 0
pessoaMax = 0
pessoaTotal = 0

distInicial = 0

treshold = 20

limiar = 5

def dist_rand():
        return random.uniform(1,70)

def dist():
        cent = 0
        pulseOn = 0
        pulseOff = 0

        trigPin.write(0)
        time.sleep(0.000002)
        trigPin.write(1)
        time.sleep(0.000002)
        trigPin.write(0)

        count = 0
        while echoPin.read() == 0 and count < 500:
                pulseOff = time.time()
                count = count + 1
        count = 0
        while echoPin.read() == 1 and count < 500:
                pulseOn = time.time()
                count = count + 1

        if(pulseOn and pulseOff):
                timeDiff = pulseOn - pulseOff
                cent = timeDiff * 17000

        time.sleep(0.05)
        f = open('usound', 'w')
        f.write(str(cent) + '\n')
        f.close()
        return cent



def subtraiPessoa():
        global pessoaSai
        estabilizou() #espera reestabilizar
        pessoaSai = pessoaSai + 1

def somaPessoa():
        global pessoaEntra
        estabilizou() #espera reestabilizar
        pessoaEntra = pessoaEntra + 1

def estabilizou():
        estavel = 0
        leituras = []
        for i in range(50):
                leitura = dist()
                leituras.append(leitura)
        global limiar
        while(not estavel):
                soma = 0
                variancia = 0
                desvio = 0
                media = 0
                for i in range(50):
                        leitura = dist()
                        print leitura
                        leituras[i] = leitura
                        soma = soma + leitura
                media = soma / 50.0
                for i in range(50):
                        variancia = variancia + math.pow(media -
leituras[i], 2)
                variancia = variancia / (50 - 1)
                desvio = math.sqrt(variancia)
                if(desvio < limiar):
                        distancia = dist()
                        if((distancia > distInicial - treshold) and
(distancia < distInicial + treshold)):
                                estavel = 1

while(not distInicial):
        distInicial = dist()

f = open('currnum', 'w')
f.write('0' + '\n')
f.close()

f = open('maxnum', 'w')
f.write('0' + '\n')
f.close()

f = open('totalnum', 'w')
f.write('0' + '\n')
f.close()

while(1):

        distancia = dist()
        time.sleep(0.05) #era 0.001

        if(distancia < distInicial - treshold):
                somaPessoa()
                print 'entra: ' + str(pessoaEntra)
                pessoaAtual = pessoaEntra - pessoaSai
                pessoaTotal = pessoaTotal + 1
                if(pessoaAtual > pessoaMax):
                        pessoaMax = pessoaAtual
                        f = open('maxnum', 'w')
                        f.write(str(pessoaMax) + '\n')
                        f.close()
                f = open('currnum', 'w')
                f.write(str(pessoaAtual) + '\n')
                f.close()
                f = open('totalnum', 'w')
                f.write(str(pessoaTotal) + '\n')
                f.close()

        elif(distancia > distInicial + treshold):
                subtraiPessoa()
                print 'sai: ' + str(pessoaSai)
                f = open('currnum', 'w')
                f.write(str(pessoaEntra - pessoaSai) + '\n')
                f.close()
        time.sleep(0.001)
