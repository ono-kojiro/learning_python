#set terminal png

#set terminal postscript eps enhanced color
set terminal pdf color font ',10'
set output pdffile

set key left top
set xlabel "number of threads"
set ylabel "events per second"
set xrange [0:5]

plot datfile using 1:2 title "events per second"

