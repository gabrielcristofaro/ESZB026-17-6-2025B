#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import serial
import atexit
import time

def inicia_coleta():
    conexaoSerial.write(b'i')

def para_coleta():
    conexaoSerial.write(b'p')
def aumenta_taxa():
    conexaoSerial.write(b'd')
def diminui_taxa():
    conexaoSerial.write(b'a')
    
def mostra_intervalo():
    conexaoSerial.write(b'p')
    time.sleep(0.1)
    while  conexaoSerial.inWaiting() > 0:
        lixo = conexaoSerial.read()
        time.sleep(0.01)
    
    
    conexaoSerial.write(b't')
    time.sleep(0.1)
    while conexaoSerial.inWaiting() == 0:
        time.sleep(0.01)
        
    if conexaoSerial.inWaiting()>=1:
        low = conexaoSerial.read()
        intervalo = ord(low)
        texto_intervalo.setText(f"intervalo: {intervalo}ms")
def saindo():
    conexaoSerial.write(b'p')
    print('Saindo')

def update():
    
    global data1, curve1, ptr1, conexaoSerial, x_atual, npontos, previousTime
    if conexaoSerial.inWaiting() > 1:
        dado1 = conexaoSerial.read()
        dado2 = conexaoSerial.read()
        novodado = float( (ord(dado1) + ord(dado2)*256.0)*5.0/1023.0 )
        
        data1[x_atual] = novodado
        data1[(x_atual+1)%npontos] = np.nan
        x_atual = x_atual+1
        if x_atual >= npontos:
            x_atual = 0
        
        curve1.setData(data1, connect="finite")
        actualTime = time.time()*1000
        taxa = str(round(actualTime-previousTime))
        previousTime = actualTime
        texto.setText("taxa: "+taxa.zfill(3)+"ms" )

win = pg.GraphicsWindow()
win.setWindowTitle('Coletando dados do Arduino via Porta Serial')

npontos = 800
x_atual = 0
p1 = win.addPlot()
p1.setYRange(0,5,padding=0)
data1 = np.zeros(npontos)
curve1 = p1.plot(data1)

previousTime = time.time()*1000 # pega a hora atual, em milissegundos
texto = pg.TextItem(text="", color=(255,255,0), anchor=(0,1))
p1.addItem(texto)
texto.setPos(0,0) # adiciona o texto na posicao (0,0) do grafico

texto_intervalo = pg.TextItem(text="", color=(0,255,255), anchor=(1,1))
p1.addItem(texto_intervalo)
texto_intervalo.setPos(700, 0)
botoes_layout = win.addLayout(row=1, col=0)

def add_botao(titulo, func, row):
    proxy = QtGui.QGraphicsProxyWidget()
    botao = QtGui.QPushButton(titulo)
    proxy.setWidget(botao)
    botao.clicked.connect(func)
    botoes_layout.addItem(proxy, row=row, col=0)
        
add_botao('Inicia', inicia_coleta, 0)
add_botao('Para', para_coleta, 1)
add_botao('Intervalo Atual', mostra_intervalo, 2)
add_botao('Aumentar Taxa', aumenta_taxa, 3)
add_botao('Diminuir Taxa', diminui_taxa, 4)

conexaoSerial = serial.Serial('/dev/ttyACM0', 115200)
conexaoSerial.write(b'i')

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

atexit.register(saindo)

if __name__ == '__main__':
    QtGui.QApplication.instance().exec_()
