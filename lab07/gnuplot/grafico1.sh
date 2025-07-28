#!/bin/sh
ARQUIVODADOS=/home/pi/ESZB026-17-6-2025B/lab07/gnuplot/dados1.txt
ARQUIVOSAIDA=/home/pi/ESZB026-17-6-2025B/lab07/gnuplot/dados1.png

gnuplot << EOF
set title "Título"
set ylabel "Eixo Y"
set xlabel "Eixo X"
set terminal png
set output "$ARQUIVOSAIDA"
plot "$ARQUIVODADOS" \
     linecolor rgb '#FF60ad' \
     linetype 2 \
     linewidth 2 \
     pointtype 3 \
     pointsize 2.0 \
     title "Dados 1" \
     with linespoints
EOF

