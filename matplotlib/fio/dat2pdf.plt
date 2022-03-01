#set terminal png

#set terminal postscript eps enhanced color
set terminal pdf color font ',10'
set output pdffile

set key left top
set logscale x 2
set xrange [1024:1048576]
set format x "10^{%L}"
set xlabel "block size"
set ylabel "band width (M/s)"


set xtics ( \
	"4K" 4096, "8K" 8192, "16K" 16384, "32K" 32768, "64K" 65536, \
	"128K" 131072, "256K" 262144, "512K" 524288, \
)

plot datfile every :::0::0 using 3:($4/1000000) title "host randread" with linespoints  lt 1, \
     datfile every :::1::1 using 3:($4/1000000) title "host randwrite" with linespoints lt 2, \
     datfile every :::2::2 using 3:($4/1000000) title "host read" with linespoints lt 3, \
     datfile every :::3::3 using 3:($4/1000000) title "host write" with linespoints lt 4

