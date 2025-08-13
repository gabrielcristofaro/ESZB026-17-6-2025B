#!/usr/bin/env python3
import serial
import time
import collections
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import sys

# ==== CONFIGURAÇÕES ====
PORTA_SERIAL = '/dev/ttyACM0'  # ou /dev/ttyUSB0
BAUD_RATE = 115200
TAMANHO_JANELA = 500

# ==== ABRE PORTA SERIAL ====
try:
    ser = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
    time.sleep(2)
    print("Conexão com Arduino estabelecida.")
except serial.SerialException as e:
    print(f"Erro ao abrir porta serial: {e}")
    sys.exit()

# ==== BUFFER DE DADOS ====
dados = collections.deque([0] * TAMANHO_JANELA, maxlen=TAMANHO_JANELA)
intervalo_atual = "?? ms"  # texto inicial

# ==== INTERFACE GRÁFICA ====
app = QtWidgets.QApplication([])
win = pg.GraphicsLayoutWidget()
win.resize(900, 500)
win.setWindowTitle('ECG - Arduino + Raspberry')
win.show()

pg.setConfigOptions(antialias=True)

# Gráfico
plot = win.addPlot(row=0, col=0, colspan=3)
plot.setTitle("Sinal de ECG (AD8232)")
plot.setYRange(0, 1023)
plot.setLabel('left', 'Amplitude')
plot.setLabel('bottom', 'Amostras')

curve = plot.plot(dados, pen='g')

# Texto para mostrar intervalo no canto superior direito
intervalo_texto = pg.TextItem(f"Intervalo: {intervalo_atual}", anchor=(1, 0))
plot.addItem(intervalo_texto)
intervalo_texto.setPos(TAMANHO_JANELA, 1023)

# ==== BOTÕES ====
btn_ler_intervalo = QtWidgets.QPushButton("Ler Intervalo")
btn_aumentar = QtWidgets.QPushButton("Aumentar Taxa")
btn_diminuir = QtWidgets.QPushButton("Diminuir Taxa")

# Layout para botões
container = QtWidgets.QWidget()
layout = QtWidgets.QHBoxLayout()
layout.addWidget(btn_ler_intervalo)
layout.addWidget(btn_aumentar)
layout.addWidget(btn_diminuir)
container.setLayout(layout)

# Adiciona container de botões abaixo do gráfico
proxy = QtWidgets.QGraphicsProxyWidget()
proxy.setWidget(container)
plot.scene().addItem(proxy)
proxy.setPos(50, -150)  # ajusta posição dos botões

# ==== FUNÇÕES DOS BOTÕES ====
def ler_intervalo():
    global intervalo_atual
    ser.write(b"I")  # comando para Arduino
    time.sleep(0.1)
    if ser.in_waiting > 0:
        resposta = ser.readline().decode().strip()
        if resposta:
            intervalo_atual = resposta + " ms"
            intervalo_texto.setText(f"Intervalo: {intervalo_atual}")

def aumentar_taxa():
    ser.write(b"A")  # comando para Arduino

def diminuir_taxa():
    ser.write(b"D")  # comando para Arduino

btn_ler_intervalo.clicked.connect(ler_intervalo)
btn_aumentar.clicked.connect(aumentar_taxa)
btn_diminuir.clicked.connect(diminuir_taxa)

# ==== ATUALIZAÇÃO DO GRÁFICO ====
def atualizar():
    global dados
    while ser.in_waiting > 0:
        try:
            linha = ser.readline().decode('utf-8').strip()
            if linha.isdigit():
                valor = int(linha)
                dados.append(valor)
        except ValueError:
            pass
    curve.setData(dados)
    intervalo_texto.setPos(len(dados), max(dados) if dados else 1023)

# ==== TIMER ====
timer = pg.QtCore.QTimer()
timer.timeout.connect(atualizar)
timer.start(5)

# ==== EXECUÇÃO ====
if __name__ == '__main__':
    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("\nEncerrando...")
    finally:
        ser.close()


