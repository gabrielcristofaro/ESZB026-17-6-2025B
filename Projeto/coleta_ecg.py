#!/usr/bin/env python3
import serial
import time
import sys

# ==== CONFIGURAÇÕES ====
PORTA_SERIAL = '/dev/ttyACM0'  # Pode ser /dev/ttyUSB0 dependendo da sua Raspberry Pi
BAUD_RATE = 115200
ARQUIVO_SAIDA = 'ecg_data.txt' # Nome do arquivo para salvar os dados
NUMERO_DE_AMOSTRAS = 600 # Quantidade de pontos a serem coletados (ex: 5 segundos a 120Hz)

# ==== ABRE PORTA SERIAL ====
try:
    ser = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=2)
    time.sleep(2)  # Tempo para o Arduino reiniciar
    print("Conexão com Arduino estabelecida.")
except serial.SerialException as e:
    print(f"Erro ao abrir porta serial: {e}")
    sys.exit()

# ==== COLETA E SALVA OS DADOS ====
print(f"Iniciando a coleta de {NUMERO_DE_AMOSTRAS} amostras...")

dados_coletados = []
try:
    # Limpa qualquer dado residual no buffer da serial
    ser.flushInput()

    while len(dados_coletados) < NUMERO_DE_AMOSTRAS:
        if ser.in_waiting > 0:
            try:
                linha = ser.readline().decode('utf-8').strip()
                if linha:
                    valor = int(linha)
                    dados_coletados.append(valor)
                    # Imprime o progresso no console
                    print(f"Coletado: {len(dados_coletados)}/{NUMERO_DE_AMOSTRAS}", end='\r')
            except (ValueError, UnicodeDecodeError):
                # Ignora linhas que não são números ou que têm erro de decodificação
                pass

    print("\nColeta finalizada.")

    # Salva os dados no arquivo de texto
    with open(ARQUIVO_SAIDA, 'w') as f:
        for i, ponto in enumerate(dados_coletados):
            # Formato: tempo_em_segundos valor
            # A frequência é de 120Hz, então o tempo é o índice da amostra / 120.0
            tempo = i / 120.0
            f.write(f"{tempo:.4f} {ponto}\n")
    
    print(f"Dados salvos com sucesso em '{ARQUIVO_SAIDA}'.")

except KeyboardInterrupt:
    print("\nColeta interrompida pelo usuário.")
finally:
    ser.close()
    print("Conexão serial fechada.")
