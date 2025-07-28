#!/bin/sh
ARQUIVODADOS=/home/pi/ESZB026-17-6-2025B/lab07/gnuplot/dados3.txt
ARQUIVOSAIDA=/home/pi/ESZB026-17-6-2025B/lab07/gnuplot/dados3.png

gnuplot << EOF
set title "Título"
set ylabel "Eixo Y"
set xlabel "Eixo X"
set terminal png
set output "$ARQUIVOSAIDA"
plot "$ARQUIVODADOS" \
     linecolor rgb '#0060FF' \
     linetype 1 \
     linewidth 1 \
     pointtype 2 \
     pointsize 1.0 \
     title "Dados 3" \
     with linespoints
EOF

