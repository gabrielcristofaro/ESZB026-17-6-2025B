#!/usr/bin/env python3
import subprocess
import os
import time # Adicionado para usar time.time() no final

# --- IMPORTANTE ---
# O diretório onde este script CGI está localizado.
# O servidor web precisa ter permissão de escrita neste diretório
# para que o script de coleta possa criar o arquivo de dados.
# Geralmente, é /usr/lib/cgi-bin/
DIRETORIO_CGI = os.path.dirname(os.path.abspath(__file__))

# Caminhos para os scripts e arquivos de dados
# Ajuste se você colocar os arquivos em locais diferentes
SCRIPT_COLETA = "/usr/local/bin/coleta_ecg.py"
SCRIPT_GRAFICO = "/usr/local/bin/gera_grafico.sh"
ARQUIVO_DADOS = "/var/www/html/ecg_data.txt"
URL_GRAFICO = "/ecg_grafico.png" # URL relativa para a imagem

# --- Cabeçalho HTTP ---
print("Content-Type: text/html;charset=utf-8")
print() # Linha em branco obrigatória

# --- Corpo do HTML ---
print("<!DOCTYPE html>")
print("<html lang='pt-br'>")
print("<head>")
print("<meta charset='UTF-8'>")
print("<title>Gráfico de ECG</title>")
# Adiciona um refresh automático a cada 10 segundos
print("<meta http-equiv='refresh' content='10'>")
print("""
<style>
    body { font-family: sans-serif; background-color: #f0f0f0; margin: 20px; }
    .container { max-width: 850px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    h1 { color: #333; }
    img { max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; }
    .status { background: #e7e7e7; padding: 10px; border-radius: 4px; font-family: monospace; white-space: pre-wrap; }
    button { padding: 10px 15px; font-size: 16px; cursor: pointer; border: none; background-color: #28a745; color: white; border-radius: 5px; }
    button:hover { background-color: #218838; }
</style>
""")
print("</head>")
print("<body>")
print("<div class='container'>")
print("<h1>Monitor de Sinal de ECG</h1>")
print("<p>Esta página é atualizada automaticamente a cada 10 segundos, coletando novos dados e gerando um novo gráfico.</p>")

# --- Executa os scripts ---
print("<h2>Status da Execução:</h2>")
print("<div class='status'>")

# 1. Executa a coleta de dados
print("1. Executando script de coleta de dados...")
# O script de coleta precisa ser executado em um diretório com permissão de escrita
# Usamos o diretório /var/www/html que é acessível pelo servidor web
try:
    # O 'cwd' (current working directory) garante que o ecg_data.txt seja salvo no lugar certo
    # Onde o gera_grafico.sh espera encontrá-lo.
    coleta_process = subprocess.run(
        [SCRIPT_COLETA],
        capture_output=True, text=True, timeout=30, cwd="/var/www/html"
    )
    print("Saída do script de coleta:")
    print(coleta_process.stdout)
    if coleta_process.stderr:
        print("Erros do script de coleta:")
        print(coleta_process.stderr)
except subprocess.TimeoutExpired:
    print("ERRO: O script de coleta demorou demais para responder.")
except Exception as e:
    print(f"ERRO ao executar o script de coleta: {e}")

print("\n2. Gerando o gráfico...")
# 2. Executa a geração do gráfico
try:
    # --- ALTERAÇÃO AQUI ---
    # Chamamos o bash explicitamente para executar o script, o que resolve o "Exec format error".
    grafico_process = subprocess.run(
        ['/bin/bash', SCRIPT_GRAFICO],
        capture_output=True, text=True, timeout=10
    )
    print("Saída do script de gráfico:")
    print(grafico_process.stdout)
    if grafico_process.stderr:
        print("Erros do script de gráfico:")
        print(grafico_process.stderr)
except Exception as e:
    print(f"ERRO ao gerar o gráfico: {e}")

print("</div>")

# --- Exibe a imagem ---
print("<h2>Gráfico Gerado:</h2>")
# Adicionamos um timestamp para evitar problemas de cache do navegador
print(f"<img src='{URL_GRAFICO}?t={time.time()}' alt='Gráfico de ECG'>")

print("</div>")
print("</body>")
print("</html>")
