
# Define os caminhos dos arquivos de entrada e saída
# É importante usar caminhos absolutos para que os scripts CGI funcionem corretamente
ARQUIVO_DADOS="/var/www/html/ecg_data.txt"
ARQUIVO_SAIDA="/var/www/html/ecg_grafico.png"

# Executa o gnuplot com os comandos abaixo
gnuplot << EOF
set title "Sinal de ECG Coletado"
set ylabel "Amplitude (unidade ADC)"
set xlabel "Tempo (s)"
set terminal png size 800,400
set output "$ARQUIVO_SAIDA"
set grid
plot "$ARQUIVO_DADOS" using 1:2 with lines title "ECG" linecolor rgb "#009933"
EOF
