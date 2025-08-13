#!/usr/bin/env python3
import serial
import time
import collections
from PyQt5 import QtWidgets
import pyqtgraph as pg
import sys

# ==== CONFIGURAÇÕES ====
PORTA_SERIAL = '/dev/ttyACM0'  # ou /dev/ttyUSB0
BAUD_RATE = 115200
TAMANHO_JANELA = 500           # número de amostras no gráfico

# ==== ABRE PORTA SERIAL ====
try:
    ser = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
    time.sleep(2)  # tempo para o Arduino reiniciar
    print("Conexão com Arduino estabelecida.")
except serial.SerialException as e:
    print(f"Erro ao abrir porta serial: {e}")
    sys.exit()

# ==== BUFFER DE DADOS ====
dados = collections.deque([0] * TAMANHO_JANELA, maxlen=TAMANHO_JANELA)

# ==== CONFIGURA A JANELA DO PYQTGRAPH ====
app = QtWidgets.QApplication([])
win = pg.GraphicsLayoutWidget()  # sem argumentos extras
win.resize(800, 400)
win.setWindowTitle('ECG - Arduino + Raspberry')
win.show()

pg.setConfigOptions(antialias=True)  # linhas mais suaves

# Cria o plot e define o título aqui
plot = win.addPlot()
plot.setTitle("Sinal de ECG (AD8232)")
plot.setYRange(0, 1023)  # faixa inicial
plot.setLabel('left', 'Amplitude')
plot.setLabel('bottom', 'Amostras')

curve = plot.plot(dados, pen='g')  # linha verde

# ==== FUNÇÃO DE ATUALIZAÇÃO ====
def atualizar():
    global dados
    while ser.in_waiting > 0:
        try:
            linha = ser.readline().decode('utf-8').strip()
            if linha:
                valor = int(linha)
                dados.append(valor)
        except ValueError:
            pass  # ignora valores inválidos
    curve.setData(dados)

# ==== TIMER PARA ATUALIZAÇÃO ====
timer = pg.QtCore.QTimer()
timer.timeout.connect(atualizar)
timer.start(5)  # atualiza a cada 5ms

# ==== EXECUTA APLICAÇÃO ====
if __name__ == '__main__':
    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("\nEncerrando...")
    finally:
        ser.close()
