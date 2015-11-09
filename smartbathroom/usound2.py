import mraa
import random
import time
import sys
import math

#definition of input and output pins
trigPin = mraa.Gpio(2)
trigPin.dir(mraa.DIR_OUT)

echoPin = mraa.Gpio(3)
echoPin.dir(mraa.DIR_IN)

#a delay to initialize
time.sleep(0.3)

#the bathroom informations
pessoaEntra = 0
pessoaSai = 0
pessoaMax = 0
pessoaTotal = 0

#distance value of the closed door, it will be modified 
distInicial = 0

#possible error of the ultrassonic sensor, its used when someone leave the bathroom 
treshold = 20

# a limiar of error to enter int the
limiar = 5

#returns the distance of the ultrassonic sensor in centimeters
def dist():

        #the distance in centimeters
        cent = 0

        pulseOn = 0
        pulseOff = 0

        #send the signal
        trigPin.write(0)
        time.sleep(0.000002)
        trigPin.write(1)
        time.sleep(0.000002)
        trigPin.write(0)

        #read the signal
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

        #write the sensor value in a file to webserver reads
        time.sleep(0.05)
        f = open('usound', 'w')
        f.write(str(cent) + '\n')
        f.close()

        return cent


#decrese the number of people in the bathroom
def subtraiPessoa():
        global pessoaSai
        estabilizou() #wait the stabilization
        pessoaSai = pessoaSai + 1

#increse the number of people in the bathroom
def somaPessoa():
        global pessoaEntra
        estabilizou() #wait the stabilization
        pessoaEntra = pessoaEntra + 1

#the function only ends when the sensor stabilizates in the default distance
def estabilizou():

        #this variable is set 1 when the sensor stabilize
        estavel = 0
        leituras = [] # a vector of consecutives ultrasonic values

        #Creates a vector of 50 ultrasonic readings 
        for i in range(50):
                leitura = dist()
                leituras.append(leitura)

        global limiar #the global variable 

        #repeats until the sensor stabilize in the default distance
        #calculates the vector standard deviation 
        while(not estavel):
                soma = 0
                variancia = 0
                desvio = 0
                media = 0

                #calculates the sum
                for i in range(50):
                        leitura = dist()
                        print leitura
                        leituras[i] = leitura
                        soma = soma + leitura

                #calculates the media
                media = soma / 50.0

                #calculates the variance
                for i in range(50):
                        variancia = variancia + math.pow(media - leituras[i], 2)
                variancia = variancia / (50 - 1)

                #calculates the standard deviation
                desvio = math.sqrt(variableariancia)

                #the deviation has to be less than a limiar
                if(desvio < limiar):
                        distancia = dist()
                        #the last distance has to be close to the default, then it will be stable
                        if((distancia > distInicial - treshold) and (distancia < distInicial + treshold)):
                                estavel = 1

#calculates the default distance
while(not distInicial):
        distInicial = dist()

#set the files with the data of people with default values 
f = open('currnum', 'w')
f.write('0' + '\n')
f.close()

f = open('maxnum', 'w')
f.write('0' + '\n')
f.close()

f = open('totalnum', 'w')
f.write('0' + '\n')
f.close()

#main
while(1):

        distancia = dist() #take a ultrasonic value
        time.sleep(0.05) #wait a litle

        #someone passed in front of the sensor: this person will enter in the bathroom
        if(distancia < distInicial - treshold):
                somaPessoa() #counts a new person in the bath
                
                pessoaAtual = pessoaEntra - pessoaSai #sets a new number of people inside
                pessoaTotal = pessoaTotal + 1 #sets a new number of total people in all time
                if(pessoaAtual > pessoaMax): #sets a new number of max person in a way
                        pessoaMax = pessoaAtual
                        f = open('maxnum', 'w')
                        f.write(str(pessoaMax) + '\n')
                        f.close()
                #write in the files the bathroom datas
                f = open('currnum', 'w')
                f.write(str(pessoaAtual) + '\n')
                f.close()
                f = open('totalnum', 'w')
                f.write(str(pessoaTotal) + '\n')
                f.close()

        #someone open the door, the sensor capts a large distance, this person left the bathroom
        elif(distancia > distInicial + treshold):
                subtraiPessoa() #discount a person
                
                #update the files datas
                f = open('currnum', 'w')
                f.write(str(pessoaEntra - pessoaSai) + '\n')
                f.close()
        time.sleep(0.001)
